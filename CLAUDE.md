# my-ws — ナレッジベース 運用ルール

## プロジェクト概要

個人情報プラットフォーム。技術トレンド・世界情勢・文化・科学を毎日自動収集し、
週次 Markdown ファイルに蓄積する。日曜日に週次 HTML レポート、月末に月次 HTML マガジン
および NotebookLM ポッドキャストを自動生成する。

**3 つの目的軸:**
1. **開発応用** — 技術スタックの最新動向を蓄積し、Claude との開発相談精度を向上させる
2. **自己記録** — いつ何に興味を持ったかを週次ファイルにアーカイブする
3. **世界情勢把握** — テック以外のグローバルニュース・文化・科学をカバーする

---

## スキルの使い方

毎日の情報収集は `/daily-knowledge` スキルで実行する。

```
/daily-knowledge
```

Claude Desktop のルーティーン機能に設定済み（毎朝 6〜9 時）。
Codex からも実行可能（モデル: gpt-5.4-mini）。

---

## ディレクトリ構造

```
data/
├── knowledge/
│   ├── Technology/YYYY/MM/   — 技術系週次ファイル（SA1・SA2 が追記）
│   └── Other/YYYY/MM/        — その他週次ファイル（SA3〜SA6 が追記）
├── reports/
│   ├── weekly/YYYY/          — 週次 HTML レポート（日曜生成）
│   └── monthly/YYYY/         — 月次 HTML マガジン・ポッドキャスト（月末生成）
└── suggestions/YYYY/MM/      — 新興味トピック提案（毎日追記）

.claude/skills/daily-knowledge/  — /daily-knowledge スキル本体
data/scripts/jina-fetch.py       — Jina Reader 認証スクリプト
```

---

## 週次ファイル命名規則

```
WN(月-日_月-日)   例: W4(6-22_6-28)
```

- **W番号**: `ceil(day / 7)` で算出（例: 22 日 → W4）
- **開始日**: `(W-1) * 7 + 1` 日
- **終了日**: `W * 7` 日（月末を超える場合は月末日）
- 週をまたぐ場合も月-日_月-日のまま記述する

---

## 書き込みルール

- 既存ファイルへの書き込みは必ず **追記モード**（上書き・削除は禁止）
- 情報は必ず **出典 URL 付き** で記録する
- 日本語要約は原意を損なわず **1〜3 文** で簡潔に
- 英語原文の重要引用はそのまま残す

---

## セキュリティ

- **`.env` は絶対にコミットしない**（`.gitignore` 済み）
- `JINA_API_KEY` は `~/documents/my-ws/.env` でのみ管理する
- `data/config/` も `.gitignore` 済み

---

## コミット規則

| プレフィックス | 用途 |
|------------|-----|
| `feat:` | 新機能・新スキル |
| `fix:` | バグ修正 |
| `ref:` | リファクタリング |
| `docs:` | ドキュメント・CLAUDE.md 更新 |
| `chore:` | 設定・依存関係 |

- **1 コミット 1 タスク**（スキル更新とドキュメント更新は別コミット）
- Claude 共同作業時は必ず `Co-Authored-By` を `-m ""` で独立した `-m` フラグとして追記する

```bash
git commit -m "feat: ..." \
           -m "詳細説明" \
           -m "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

---

## Python 環境

依存パッケージ（`pyproject.toml` 管理）:
- `requests` — Jina Reader API へのリクエスト
- `python-dotenv` — `.env` からのキー読み込み

初回セットアップ:
```bash
uv sync
```

スクリプト実行:
```bash
.venv/bin/python data/scripts/jina-fetch.py "https://example.com"
```
