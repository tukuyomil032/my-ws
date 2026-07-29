---
name: daily-knowledge
description: >
  毎日の情報収集ルーティーンを実行する。技術トレンド・技術深層・世界情勢・経済・文化・科学の
  6軸を6体の担当エージェントで staging-only に収集し、親コントローラーだけが週次ファイルへ安全に追記する。
  日曜日は週次 HTML レポートを、月末は月次 HTML マガジンと
  NotebookLM ポッドキャストを条件に応じて生成する。
version: "1.0.1"
metadata:
  author: tukuyomil032
---

# Daily Knowledge

個人情報プラットフォームの中核スキル。3軸の目的を毎日自動で推進する:

1. **開発応用** — 技術スタックの最新動向を蓄積し、ClaudeとCodex両方との開発相談精度を向上させる
2. **自己記録** — いつ何に興味を持ったかを週次ファイルにアーカイブする
3. **世界情勢把握** — テック以外のグローバルニュース・文化・科学をカバーする

---

## Prerequisites

このスキルを実行する前に以下が整っていること:

- **作業ディレクトリ**: `~/documents/my-ws`
- **Jina API Key**: `~/documents/my-ws/.env` に `JINA_API_KEY=<your_key>` を設定済み
  - 取得先: https://jina.ai（メール登録のみ・無料枠 1,000 万トークン）
  - 確認時はキー値を出力しない。`rg` で `.env` を読む場合も `JINA_API_KEY` の存在確認だけに留め、値が端末・ログ・最終報告に出ない方法を使う。
  - 禁止例: `rg -n "JINA_API_KEY=" .env` は値まで出力するため使わない。
  - 安全な確認例:
    ```bash
    .venv/bin/python - <<'PY'
    from dotenv import dotenv_values
    key = dotenv_values(".env").get("JINA_API_KEY")
    print("JINA_API_KEY configured" if key and key != "your_api_key_here" else "JINA_API_KEY missing")
    PY
    ```
- **必須スキル**: `/interest-profile`
- **任意スキル**: `/deep-research`（未導入時は各 SA の WebSearch フォールバックを使う）、`/nlm-skill`（月末の STEP 7 でのみ必要。未導入時は STEP 7 をスキップしてログへ記録する）
- **Python 依存パッケージ**: `uv add requests python-dotenv`（初回のみ）。実行時はプロジェクトの `.venv/bin/python` を使う

---

## File Naming Convention

週次ファイルは以下の命名規則に従う:

```
WN(月-日_月-日)   例: W4(6-22_6-28)
```

- **W番号**: その月の第何週か（1日始まりで7日ごとに繰り上がる）
- **月-日_月-日**: 週の開始日と終了日（終了日が翌月になる場合も月-日のまま記述）
- **Techファイル**: `data/knowledge/Technology/YYYY/MM/WN(月-日_月-日).md`
- **Otherファイル**: `data/knowledge/Other/YYYY/MM/WN(月-日_月-日).md`

ファイルが存在しない場合のヘッダー:

```markdown
# 技術トレンド・深層記事 WN (月/日〜月/日)
```

```markdown
# ワールドニュース・文化・科学 WN (月/日〜月/日)
```

---

## Workflow

### STEP 1: 興味関心の同期

```
/interest-profile sync
```

これにより `INTERESTS.md`（プロジェクトルート）が最新の状態に更新される。
SA2 はこのファイルを読んで深層記事の収集対象を決定する。

`data/interests/last-sync.json.pending` が生成された場合は、JSONを検証してから本番の `last-sync.json` へ昇格する。検証失敗や破損がある場合は昇格せず、既存の確定状態を維持してログへ記録する。

---

### STEP 2: 週次ファイルパスの計算

今日の日付から以下を導出し、ファイルが存在しない場合は上記ヘッダーで新規作成する:

1. 年・月を取得する
2. W番号を計算する: `W = ceil(day / 7)`（例: 22日 → W4）
3. 週の開始日を算出: `(W-1) * 7 + 1` 日
4. 週の終了日を算出: `W * 7` 日（月末を超える場合は月末日）
5. ファイルパスを構築して存在確認 → なければ新規作成

---

### STEP 3: 6体情報収集

`/superpowers:subagent-driven-development` を使い、以下の 6 体を起動する。
各 SA の詳細指示は `agents/` 配下の対応ファイルを読んでから渡すこと。

**使用モデル（実行環境に合わせて選択）**:
- Claude で実行する場合: **Claude Haiku 4.5**
- Codex で実行する場合: **gpt-5.4-mini**

| SA | ファイル | 担当 | 最終統合先（親が書き込む） |
|----|---------|------|-----------|
| SA1 | `agents/SA1.md` | 技術トレンド | Techファイル |
| SA2 | `agents/SA2.md` | 技術深層記事 | Techファイル |
| SA3 | `agents/SA3.md` | 地政学・世界情勢 | Otherファイル |
| SA4 | `agents/SA4.md` | 経済・スタートアップ | Otherファイル |
| SA5 | `agents/SA5.md` | 文化・エンタメ・音楽 | Otherファイル |
| SA6 | `agents/SA6.md` | 科学・宇宙・医療 | Otherファイル |

#### 並列実行と単一ライター

- 6体を同時起動できない環境では、利用可能な子エージェント枠に合わせて波状実行する（例: 3枠なら SA1〜SA3、続いて SA4〜SA6）。全6担当を省略しない。
- SAは共有するTech・Other週次ファイルへ直接書き込まず、`/tmp/daily-knowledge/YYYY-MM-DD/SA{N}.md` へ保存し、正常終了時だけ同名の `.done` を作成する。コントローラーは `.done` がある成果物だけを統合する。
- 各SAを起動するとき、親は対象日 `TARGET_DATE=YYYY-MM-DD`、`OUTPUT_PATH=/tmp/daily-knowledge/YYYY-MM-DD/SA{N}.md`、`DONE_PATH=/tmp/daily-knowledge/YYYY-MM-DD/SA{N}.md.done` を明示して渡す。SAは実時計や検索結果の相対日付で対象日を上書きせず、見出し・取得日・採否判断を親の `TARGET_DATE` に固定する。SAは `DONE_PATH` 以外の完了マーカーを作らず、別名マーカーだけが存在する成果物は未完了扱いにしてログへ記録する。
- SAの成果物末尾には、本文確認不能・Jina失敗・same-topic疑い・集約ページのみの候補など、親の再採用判定に必要な注意点を明記する。`OUTPUT_PATH` / `DONE_PATH` 以外のプロジェクト内ファイルは変更しない。
- 全SA終了後、コントローラーだけが `SA1 → SA2` をTech、`SA3 → SA4 → SA5 → SA6` をOtherへ直列統合する。対象ファイルごとに完成ブロックを先に組み立て、1回だけ末尾追記して直後に検証する。これを唯一の書き込み経路とする。
- timeout・接続失敗・HTTP 5xx のような過渡障害だけ最大1回再試行する。認証・入力・仕様違反は再試行しない。
- SAが失敗した場合は他のSAを継続し、`data/logs/daily-knowledge/YYYY-MM-DD.md` に時刻・SA名・失敗段階・要約を追記する。

#### 統合前の採用判定

- 既存の当週ファイルと全SA成果物からURLを抽出し、fragment、`utm_*`、`fbclid`、`gclid` を除いたURLで照合する。同一URLは内容が更新されていても再追記しない。重要な新事実は、その事実を確認できる別の一次ソースURLがある場合だけ別項目として採用する。
- 既存の当週ファイルに同じ企業・プロジェクト・作品・論文・事件が既にある場合、別URLでも単なる再掲は採用しない。新しい日付の発表、追加資金、修正リリース、政策変更、査読/撤回など、前回項目から差分として説明できる新事実がある場合だけ採用する。
- 通常の日次実行でも、既出トピックの差分確認とURL照合は当週ファイルに限定せず、既存の全 `data/knowledge` / `data/suggestions` アーカイブを参照する。過去月に同じURL・同じトピックがあれば、差分として説明できる新事実がない限り採用しない。
- SA の「採用件数」は参考値に留め、コントローラーが必ず再採用判定を行う。GitHub Trending の同一リポジトリ、作品名だけを含む映画カレンダー、既出ニュースの別媒体要約のような same-topic 再掲は、URL が違っても落とす。
- 一覧・検索・タグ・カテゴリ・カレンダー・ランキング・アーカイブなど個別項目の本文責任を持たない集約ページは候補発見の入口に限り、そのページ自体を採用根拠にしない。採用には個別記事本文または一次ソースURLを別途必須とする。
- 出典URLのない項目は採用しない。速報、未確定情報、プレリリースは状態を本文に明記する。
- stars、順位、価格などの揮発値はISO 8601相当の取得日時とタイムゾーンを明記する。取得時点が不明なら数値を省く。
- 統合後に、日付見出しが既存セクションを分断せずファイル末尾へ追加されていることを確認する。
- URL重複検証では、追加候補同士の重複と、追加候補 vs 追記前の当週ファイルの重複を分けて確認する。追記後ファイル全体だけを対象にすると、過去日の既存重複を今回追加分の問題として誤検出しやすい。
- 未実行期間をまとめて backfill する場合は、対象期間全体の追加候補を最後にもう一度正規化 URL で検証する。`added vs added` と `added vs pre-backfill HEAD` を分け、当週ファイルだけでなく backfill 前の全 `data/knowledge` / `data/suggestions` を既存集合として扱う。

**Jina Reader の呼び出し方**（SA2・SA4・SA6 で使用）:
```bash
.venv/bin/python ~/documents/my-ws/data/scripts/jina-fetch.py "https://example.com/article"
```

Jina Reader が DNS・接続・HTTP 5xx で失敗した場合は最大1回だけ再試行する。再試行後も失敗する場合、検索結果や直接取得できたページだけで断定調の要約を作らず、成果物の注意点に「Jina失敗・確認範囲」を明記する。本文確認が弱い候補は、コントローラー統合時に原則不採用とし、公開本文または一次ソースで同日中に再確認できたものだけ採用する。
- Jina失敗時の検索フォールバックは、公開本文・一次発表・公式統計などで裏取りできる事実だけ採用する。検索スニペットだけで確認した数値、投資家名、破壊的変更、移行手順、順位などは候補止まりにして、原則採用しない。

---

### STEP 4: 新興味サジェストの書き込み

統合前の採用判定を通過して週次ファイルへ追記した収集結果だけを横断分析し、`INTERESTS.md` に未記載の潜在的興味トピックを抽出する。失敗・重複・出典なしで不採用となった結果は提案元にしない。

**保存先**: `data/suggestions/YYYY/MM/WN(月-日_月-日).md`

ファイルが存在しない場合は新規作成:

```markdown
# 興味提案 WN (月/日〜月/日)

## 技術系
- [トピック名] - 検出: SA名 | 理由: なぜ興味があるかもしれないか

## 非技術系
- [トピック名] - 検出: SA名 | 理由: なぜ興味があるかもしれないか
```

既存ファイルがある場合は適切なセクションに追記する。

---

### STEP 5: 週次 HTML レポート（日曜日のみ）

> ⚠️ **このステップは Claude Sonnet 4.6 extended thinking (high) を使用すること。**

今日が **日曜日** の場合のみ実行する:

#### テンプレート選択

1. `.hallmark/last-weekly-template` を読み込み、前回のテンプレート番号を確認する（存在しない場合はスキップ）
2. 1〜6 からランダムに選択（前回番号と同じにならないよう除外する）
3. 選択したテンプレート番号を `.hallmark/last-weekly-template` に書き込む

#### コンテンツ生成

4. 今週の Tech・Other 両週次ファイルを読み込む
5. `data/reports/report-template/{N}/DESIGN.md` を読み込んでデザイントークン・Anti-pattern を把握する
6. `data/reports/report-template/{N}/template.html` を読み込む
7. 週次ファイルの内容を読み、各プレースホルダーを HTML 形式で置換する:
   - `{{WEEK_LABEL}}` → 例: `W4 · 2026年6月22日〜28日`
   - `{{GENERATED_DATE}}` → 今日の日付（YYYY-MM-DD）
   - `{{TECH_ARTICLES}}` → Tech 週次ファイルの記事を DESIGN.md のスタイルに合った HTML に変換
   - `{{OTHER_ARTICLES}}` → Other 週次ファイルの記事を HTML に変換
   - テンプレート 2（Magazine）のみ別途: `{{OTHER_ARTICLES_WORLD}}`, `{{OTHER_ARTICLES_ECONOMY}}`, `{{OTHER_ARTICLES_SCIENCE}}`, `{{OTHER_ARTICLES_CULTURE}}` をカテゴリー別に分割して注入
8. `data/reports/weekly/YYYY/WN.html` として保存する

#### 記事 HTML の変換ルール（テンプレート共通基本構造）

各テンプレートが `.article` / `.card` などの要素を持つ。変換時はテンプレートのクラス名に合わせること:

- テンプレート 1 (Broadsheet): `<article class="article"><h3 class="article__headline"><a href="URL">タイトル</a></h3><div class="article__meta">SOURCE · DATE</div><p class="article__body">要約</p></article>`
- テンプレート 2 (Magazine): `<article class="article"><div class="article__meta">SOURCE</div><h3 class="article__headline"><a href="URL">タイトル</a></h3><p class="article__body">要約</p></article>`
- テンプレート 3 (Apple): `<article class="article"><h3 class="article__headline"><a href="URL">タイトル</a></h3><div class="article__meta">SOURCE · DATE</div><p class="article__body">要約</p></article>`
- テンプレート 4 (Wabi): `<article class="article"><h3 class="article__headline"><a href="URL">タイトル</a></h3><div class="article__meta">SOURCE · DATE</div><p class="article__body">要約</p></article>`
- テンプレート 5 (Linear): `<article class="article"><div class="article__main"><h3 class="article__headline"><a href="URL">タイトル</a></h3><p class="article__body">要約</p></div><div class="article__aside"><span class="article__source">SOURCE</span><span class="article__date">DATE</span></div></article>`
- テンプレート 6 (Night Study): `<article class="card card--tech"><h3 class="card__headline"><a href="URL">タイトル</a></h3><div class="card__meta">SOURCE · DATE</div><p class="card__body">要約</p></article>` (Other は `card--other`)

#### Hallmark Anti-Slop チェック（保存前に必ず確認）

- サイドバーなし ✓
- グラデーション背景なし ✓
- 全カード border-left 色分けなし（T6 の box-shadow インジケーターは許可） ✓
- CSS spacing 変数 5 種以内 ✓
- カード hover 背景変更なし ✓

---

### STEP 6: 月次 HTML マガジン（月末のみ）

> ⚠️ **このステップは Claude Sonnet 4.6 extended thinking (high) を使用すること。**

今日が **その月の最終日** の場合のみ実行する:

#### テンプレート選択

1. `.hallmark/last-monthly-template` を読み込み、前月のテンプレート番号を確認する
2. 当月に使用した週次テンプレート番号 (`.hallmark/last-weekly-template`) も除外対象に加える
3. 1〜6 からランダムに選択（除外番号と被らないよう選ぶ）
4. 選択したテンプレート番号を `.hallmark/last-monthly-template` に書き込む

#### コンテンツ生成

5. `data/reports/report-template/{N}/DESIGN.md` と `template.html` を読み込む
6. 当月の全週次ファイル（Technology/ + Other/ 両方）を読み込む
7. 月次マガジン向けに内容を整形:
   - 各カテゴリのベスト 3 記事を選定して前半に掲載
   - 月間を通じた技術トレンドと興味の変化をサマリーとして追加
   - 全記事を週別に整理して後半に掲載
8. `data/reports/monthly/YYYY/MM.html` として保存する

---

### STEP 7: NotebookLM ポッドキャスト（月末のみ）

今日が月末の場合のみ、STEP 6 完了後に実行する:

1. `/nlm-skill` を使い、当月の知識ファイルを NotebookLM のソースとして追加する:
   - `data/knowledge/Technology/YYYY/MM/` 以下の全週次ファイル
   - `data/knowledge/Other/YYYY/MM/` 以下の全週次ファイル
2. ノートブック名: `YYYY年MM月 知識まとめ` で新規作成（または既存に追加）
3. Audio Overview（ポッドキャスト）を生成・ダウンロードする
4. 保存先: `data/reports/monthly/YYYY/MM-podcast.mp3`

---

### STEP 8: コミット & Push（毎回必須）

ルーティンで更新したファイルをタスク単位に分けてコミットし、リモートへ Push する。

未実行期間を複数日 backfill する場合は、通常の日次収集を日付ごとに分割してコミットする。週をまたぐ場合は週次ファイルの新規作成をその日付のコミットに含め、後から重複除去が必要になった場合は `chore: dedupe ...` の小さな独立コミットに閉じる。

#### コミット分類ルール

| グループ | 対象ファイル | コミットプレフィックス |
|---------|------------|---------------------|
| **日次収集** | `INTERESTS.md`, `data/interests/*`, `data/knowledge/**/*.md`, `data/suggestions/**/*.md` | `chore:` |
| **週次レポート**（日曜のみ） | `data/reports/weekly/YYYY/WN.html`, `.hallmark/last-weekly-template` | `chore:` |
| **月次マガジン**（月末のみ） | `data/reports/monthly/YYYY/MM.html`, `.hallmark/last-monthly-template` | `chore:` |

#### コミットメッセージ形式

```bash
# 日次収集
git commit -m "chore: daily-knowledge routine output for WN (YYYY-MM-DD)" \
           -m "対象週・更新SA数・追記件数の概要" \
           -m "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

# 週次レポート（別コミット）
git commit -m "chore: generate weekly report WN with template N" \
           -m "Template: <テンプレート名> — 記事数X件" \
           -m "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"

# 月次マガジン（別コミット）
git commit -m "chore: generate monthly magazine YYYY/MM with template N" \
           -m "Co-Authored-By: Claude Sonnet 4.6 <noreply@anthropic.com>"
```

#### Push

全コミット完了後、必ず Push する:

```bash
git push origin main
```

---

## Safety Boundaries

- 各週次ファイルへの書き込みは必ず **追記モード**（既存内容を絶対に消さない）
- エラーが発生した SA は処理をスキップしてログに記録し、他の SA は継続する
- 情報は必ず **出典 URL 付き** で記録する
- 日本語要約は原意を損なわず簡潔に（1〜3 文）
- 英語原文の重要引用はそのまま残す
