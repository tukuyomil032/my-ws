#!/usr/bin/env python3
"""
会話ログ (.jsonl) から未処理のユーザーメッセージを差分抽出するスクリプト。

抽出と状態コミットを「単一実行＋成功後コミット」の2フェーズで行う:

  フェーズ1（抽出）: メッセージを stdout に出し、進めるべき状態を pending ファイルに書く。
    python3 extract_interests.py \
        --state-file data/interests/last-sync.json \
        --state-out data/interests/last-sync.json.pending \
        --max-messages 500

    --logs-dir を省略するとカレントディレクトリから
    ~/.claude/projects/<エンコード済みパス> を自動推定する。

  フェーズ2（コミット）: 全処理が正常完了した後に pending を本ファイルへ原子的に昇格する。
    python3 extract_interests.py \
        --state-file data/interests/last-sync.json \
        --commit data/interests/last-sync.json.pending

Output (フェーズ1): JSON array of extracted user messages to stdout.

動作要件: Python 3.7+（型注釈は from __future__ import annotations で遅延評価）
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

NOISE_PREFIXES = (
    "<scheduled-task",
    "<local-command",
    "<command-message",
    "<task-notification",
    "<command-name>",
    "<bash-input>",
    "<bash-stdout>",
    "<turn_aborted>",
    "Base directory for this skill:",  # スキル読込時に注入される SKILL.md 本文
)

# Codex の response_item に自動注入されるシステムコンテキストブロック
CODEX_NOISE_PREFIXES = (
    "<recommended_plugins>",
    "# AGENTS.md instructions",
    "<environment_context>",
    "<system_information>",
    "<filesystem>",
)

MIN_LENGTH = 20


def normalize_content(content) -> str | None:
    """user メッセージの content を平文テキストに正規化する（Claude Code 用）。

    content は次の形式を取りうる:
      - str                       … ユーザーが打った素のテキスト
      - list[{"type":"text", ...}] … 添付つき送信等で配列化されたユーザー発言
      - list[{"type":"tool_result", ...}] … ツール実行結果（ユーザー発言ではない）

    text ブロックを連結して返す。tool_result しか含まない（=ユーザー発言でない）場合は None。
    """
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = []
        for block in content:
            if not isinstance(block, dict):
                continue
            if block.get("type") == "text" and isinstance(block.get("text"), str):
                texts.append(block["text"])
        return "\n".join(texts) if texts else None
    return None


def normalize_codex_content(payload) -> str | None:
    """Codex の response_item payload からユーザー入力テキストを抽出する。

    各 response_item.payload には複数の input_text ブロックが含まれ、
    先頭のほとんどはシステム注入コンテキスト（AGENTS.md, environment など）。
    CODEX_NOISE_PREFIXES に合致するブロックを除外し残りを連結して返す。
    """
    if payload.get("role") != "user":
        return None
    texts = []
    for block in payload.get("content", []):
        if not isinstance(block, dict):
            continue
        if block.get("type") != "input_text":
            continue
        text = block.get("text", "")
        if any(text.lstrip().startswith(p) for p in CODEX_NOISE_PREFIXES):
            continue
        texts.append(text)
    return "\n".join(texts) if texts else None


def default_logs_dir() -> Path:
    """カレントディレクトリに対応する Claude Code のログディレクトリを推定する。

    Claude Code はプロジェクトの絶対パスの '/' を '-' に置換して
    ~/.claude/projects/ 配下のディレクトリ名にしている。
    """
    encoded = os.getcwd().replace("/", "-")
    return Path.home() / ".claude" / "projects" / encoded


def default_codex_base_dir() -> Path:
    """Codex のログベースディレクトリ（~/.codex）を返す。"""
    return Path.home() / ".codex"


def find_codex_files(codex_base: Path) -> list:
    """Codex セッション JSONL を mtime 昇順で返す。

    - ~/.codex/sessions/YYYY/MM/DD/*.jsonl（日付ディレクトリ）
    - ~/.codex/archived_sessions/*.jsonl（アーカイブ）
    """
    files = []
    sessions_dir = codex_base / "sessions"
    if sessions_dir.exists():
        files.extend(sessions_dir.rglob("*.jsonl"))
    archived_dir = codex_base / "archived_sessions"
    if archived_dir.exists():
        files.extend(archived_dir.glob("*.jsonl"))
    return sorted(files, key=lambda p: p.stat().st_mtime)


def load_state(state_file: Path) -> dict:
    if state_file.exists():
        try:
            with open(state_file, encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, OSError) as e:
            # 破損していても止めない（自律実行ルール: エラーは記録して継続）。
            # 空状態にフォールバックすると全再読込になり安全側（取りこぼしより重複を許容）。
            print(f"WARNING: state file unreadable, starting fresh: {e}", file=sys.stderr)
    return {"last_sync_at": None, "sessions": {}}


def save_state(state_file: Path, state: dict):
    """一時ファイルへ書き込んでから os.replace で原子的に差し替える。"""
    state_file.parent.mkdir(parents=True, exist_ok=True)
    tmp = state_file.with_suffix(state_file.suffix + ".tmp")
    with open(tmp, "w", encoding="utf-8") as f:
        json.dump(state, f, indent=2, ensure_ascii=False)
    os.replace(tmp, state_file)


def extract_from_codex_session(filepath: Path, skip_lines: int = 0):
    """Codex セッションを skip_lines の続きから読み、(抽出メッセージ, 走査した総行数) を返す。

    session_meta（行0）は session_id 取得のため skip_lines に関わらず常に読む。
    """
    messages = []
    lines_total = 0
    session_id = filepath.stem  # fallback: ファイル名そのまま

    with open(filepath, encoding="utf-8") as f:
        for i, line in enumerate(f):
            lines_total = i + 1
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            # session_meta は常にパースして session_id を取得する
            if obj.get("type") == "session_meta":
                sid = obj.get("payload", {}).get("id")
                if sid:
                    session_id = sid
                continue  # session_meta 自体はシグナルにしない

            if i < skip_lines:
                continue

            if obj.get("type") != "response_item":
                continue

            payload = obj.get("payload", {})
            content = normalize_codex_content(payload)
            if content is None:
                continue
            if len(content) <= MIN_LENGTH:
                continue
            if any(content.lstrip().startswith(p) for p in NOISE_PREFIXES):
                continue

            ts = obj.get("timestamp", "")
            messages.append({
                "ts": ts,
                "session_id": session_id,
                "source": "codex",
                "content": content[:2000],
            })

    return messages, lines_total


def extract_from_session(filepath: Path, skip_lines: int = 0):
    """セッションを skip_lines の続きから読み、(抽出メッセージ, 走査した総行数) を返す。

    総行数は「この open で実際に EOF まで読んだ行数」なので、これを lines_read に
    使えば出力範囲としおりが必ず同一 open 内で整合する（読了後に別 open で数え直す
    と、その隙の追記分までしおりが進み恒久的に取りこぼす TOCTOU を生むため避ける）。
    """
    messages = []
    lines_total = 0
    with open(filepath, encoding="utf-8") as f:
        for i, line in enumerate(f):
            lines_total = i + 1
            if i < skip_lines:
                continue
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue

            if obj.get("type") != "user":
                continue

            msg = obj.get("message", {})
            content = normalize_content(msg.get("content", ""))
            if content is None:
                continue
            if len(content) <= MIN_LENGTH:
                continue
            if any(content.lstrip().startswith(p) for p in NOISE_PREFIXES):
                continue

            ts = obj.get("timestamp", "")
            messages.append({
                "ts": ts,
                "session_id": filepath.stem,
                "content": content[:2000],
            })
    return messages, lines_total


def read_recent_log(log_file: Path, days: int):
    """interest-log.jsonl のうち直近 days 日分の行だけを stdout へ出す。

    生ログ全体ではなく直近分だけを Claude に渡すことで、ログが何万行に
    増えても INTERESTS.md 生成時のコンテキスト量を頭打ちにする（案A）。
    ts がパースできない行は安全側に倒して出力する（取りこぼし防止）。
    """
    if not log_file.exists():
        return  # ログ未作成なら何も出さない（初回sync等）

    from datetime import datetime, timedelta, timezone

    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    kept = 0
    with open(log_file, encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")
            if not line.strip():
                continue
            try:
                ts = json.loads(line).get("ts", "")
                dt = datetime.fromisoformat(ts.replace("Z", "+00:00"))
                if dt.tzinfo is None:
                    dt = dt.replace(tzinfo=timezone.utc)
                if dt < cutoff:
                    continue
            except (json.JSONDecodeError, ValueError, AttributeError):
                pass  # 壊れた行・ts欠損は念のため残す
            print(line)
            kept += 1
    print(f"--- Loaded {kept} signals from last {days} days ---", file=sys.stderr)


def commit_state(state_file: Path, pending_file: Path):
    """pending ファイルを本ファイルへ原子的に昇格する。"""
    if not pending_file.exists():
        print(f"ERROR: pending file not found: {pending_file}", file=sys.stderr)
        sys.exit(1)

    with open(pending_file, encoding="utf-8") as f:
        state = json.load(f)

    save_state(state_file, state)
    pending_file.unlink()
    print(f"--- Committed state to {state_file} ---", file=sys.stderr)


def _process_sessions(
    files: list,
    sessions_state: dict,
    extract_fn,
    all_messages: list,
    new_state: dict,
    max_messages: int,
    reached_cap: bool,
) -> bool:
    """セッションファイルリストを処理し、メッセージを all_messages に追記する。

    reached_cap が True の場合は処理をスキップする（上限到達後の続き）。
    戻り値: cap に達したかどうか（True なら以降の処理を省略してよい）。
    """
    for filepath in files:
        if reached_cap:
            break
        file_key = filepath.stem
        current_mtime = filepath.stat().st_mtime
        prev = sessions_state.get(file_key, {})
        prev_mtime = prev.get("mtime", 0)
        prev_lines = prev.get("lines_read", 0)

        if current_mtime <= prev_mtime:
            new_state[file_key] = prev
            continue

        messages, total_lines = extract_fn(filepath, skip_lines=prev_lines)
        if total_lines < prev_lines:
            messages, total_lines = extract_fn(filepath, skip_lines=0)
        all_messages.extend(messages)

        new_state[file_key] = {
            "mtime": current_mtime,
            "lines_read": total_lines,
        }

        if max_messages > 0 and len(all_messages) >= max_messages:
            reached_cap = True

    return reached_cap


def main():
    parser = argparse.ArgumentParser(description="Extract user messages from Claude Code / Codex conversation logs")
    parser.add_argument("--logs-dir", help="Claude Code のログディレクトリ（省略時はカレントディレクトリから自動推定）")
    parser.add_argument("--codex-logs-dir", help="Codex のログベースディレクトリ（省略時は ~/.codex を自動検出、--no-codex で無効化）")
    parser.add_argument("--no-codex", action="store_true", help="Codex ログの読み込みを無効化する")
    parser.add_argument("--state-file", help="Path to last-sync.json state file（抽出/コミット時に必須）")
    parser.add_argument("--state-out", help="抽出フェーズで算出した状態を書き出す pending ファイル（本ファイルは触らない）")
    parser.add_argument("--commit", help="pending ファイルを --state-file へ原子的に昇格する（コミットフェーズ）")
    parser.add_argument("--recent-log", help="interest-log.jsonl のうち直近分だけを出力する（INTERESTS.md生成用）")
    parser.add_argument("--recent-days", type=int, default=90, help="--recent-log で出力する日数（既定: 90）")
    parser.add_argument("--max-messages", type=int, default=500, help="1実行あたりの抽出上限（0以下で無制限）")
    args = parser.parse_args()

    # 日本語を含む JSON を stdout へ出すため、出力を UTF-8 に固定する
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")

    # 読み込みモード: 直近 N 日分のシグナルだけを出力して終了する
    if args.recent_log:
        read_recent_log(Path(args.recent_log), args.recent_days)
        return

    if not args.state_file:
        parser.error("--state-file is required unless --recent-log is given")
    state_file = Path(args.state_file)

    # コミットフェーズ: 抽出は行わず pending を昇格して終了する
    if args.commit:
        commit_state(state_file, Path(args.commit))
        return

    # 抽出フェーズ: Claude Code ログ
    logs_dir = Path(args.logs_dir) if args.logs_dir else default_logs_dir()
    if not logs_dir.exists():
        print(f"ERROR: Claude logs dir not found: {logs_dir}\n"
              f"  --logs-dir で明示指定してください。", file=sys.stderr)
        sys.exit(1)

    state = load_state(state_file)
    sessions_state = state.get("sessions", {})
    codex_sessions_state = state.get("codex_sessions", {})

    all_messages = []
    new_sessions = dict(sessions_state)
    new_codex_sessions = dict(codex_sessions_state)

    claude_files = sorted(logs_dir.glob("*.jsonl"), key=lambda p: p.stat().st_mtime)
    reached_cap = _process_sessions(
        claude_files, sessions_state, extract_from_session,
        all_messages, new_sessions, args.max_messages, False,
    )

    # 抽出フェーズ: Codex ログ（~/.codex が存在する場合に自動処理）
    codex_file_count = 0
    if not args.no_codex:
        codex_base = Path(args.codex_logs_dir) if args.codex_logs_dir else default_codex_base_dir()
        if codex_base.exists():
            codex_files = find_codex_files(codex_base)
            codex_file_count = len(codex_files)
            reached_cap = _process_sessions(
                codex_files, codex_sessions_state, extract_from_codex_session,
                all_messages, new_codex_sessions, args.max_messages, reached_cap,
            )
        else:
            print(f"INFO: Codex logs dir not found ({codex_base}), skipping.", file=sys.stderr)

    json.dump(all_messages, sys.stdout, ensure_ascii=False, indent=2)

    if args.state_out:
        from datetime import datetime

        state["last_sync_at"] = datetime.now().astimezone().isoformat()
        state["sessions"] = new_sessions
        state["codex_sessions"] = new_codex_sessions
        save_state(Path(args.state_out), state)

    updated_claude = len([s for s in new_sessions if new_sessions[s] != sessions_state.get(s)])
    updated_codex = len([s for s in new_codex_sessions if new_codex_sessions[s] != codex_sessions_state.get(s)])
    print(
        f"\n--- Extracted {len(all_messages)} messages "
        f"(claude: {updated_claude} sessions updated, codex: {updated_codex}/{codex_file_count} files updated) ---",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()