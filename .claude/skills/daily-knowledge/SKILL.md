---
name: daily-knowledge
description: >
  毎日の情報収集ルーティーンを実行する。技術トレンド・世界情勢・経済・文化・科学の
  6軸を Haiku 4.5 × 6体並列で収集し、週次ファイルに追記する。
  日曜日は週次 HTML レポートを、月末は月次 HTML マガジンと
  NotebookLM ポッドキャストを自動生成する。
version: "1.0.0"
metadata:
  author: tukuyomil032
---

# Daily Knowledge

個人情報プラットフォームの中核スキル。3軸の目的を毎日自動で推進する:

1. **開発応用** — 技術スタックの最新動向を蓄積し、Claude との開発相談精度を向上させる
2. **自己記録** — いつ何に興味を持ったかを週次ファイルにアーカイブする
3. **世界情勢把握** — テック以外のグローバルニュース・文化・科学をカバーする

---

## Prerequisites

このスキルを実行する前に以下が整っていること:

- **作業ディレクトリ**: `~/documents/my-ws`
- **Jina API Key**: `~/documents/my-ws/.env` に `JINA_API_KEY=<your_key>` を設定済み
  - 取得先: https://jina.ai（メール登録のみ・無料枠 1,000 万トークン）
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

---

### STEP 2: 週次ファイルパスの計算

今日の日付から以下を導出し、ファイルが存在しない場合は上記ヘッダーで新規作成する:

1. 年・月を取得する
2. W番号を計算する: `W = ceil(day / 7)`（例: 22日 → W4）
3. 週の開始日を算出: `(W-1) * 7 + 1` 日
4. 週の終了日を算出: `W * 7` 日（月末を超える場合は月末日）
5. ファイルパスを構築して存在確認 → なければ新規作成

---

### STEP 3: 6体並列情報収集

`/superpowers:subagent-driven-development` を使い、以下の 6 体を並列起動する。
各 SA の詳細指示は `agents/` 配下の対応ファイルを読んでから渡すこと。

**使用モデル（実行環境に合わせて選択）**:
- Claude で実行する場合: **Claude Haiku 4.5**
- Codex で実行する場合: **gpt-5.4-mini**

| SA | ファイル | 担当 | 書き込み先 |
|----|---------|------|-----------|
| SA1 | `agents/SA1.md` | 技術トレンド | Techファイル |
| SA2 | `agents/SA2.md` | 技術深層記事 | Techファイル |
| SA3 | `agents/SA3.md` | 地政学・世界情勢 | Otherファイル |
| SA4 | `agents/SA4.md` | 経済・スタートアップ | Otherファイル |
| SA5 | `agents/SA5.md` | 文化・エンタメ・音楽 | Otherファイル |
| SA6 | `agents/SA6.md` | 科学・宇宙・医療 | Otherファイル |

**Jina Reader の呼び出し方**（SA2・SA4・SA6 で使用）:
```bash
.venv/bin/python ~/documents/my-ws/data/scripts/jina-fetch.py "https://example.com/article"
```

---

### STEP 4: 新興味サジェストの書き込み

全 SA の収集結果を横断分析し、`INTERESTS.md` に未記載の潜在的興味トピックを抽出する。

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

## Safety Boundaries

- 各週次ファイルへの書き込みは必ず **追記モード**（既存内容を絶対に消さない）
- エラーが発生した SA は処理をスキップしてログに記録し、他の SA は継続する
- 情報は必ず **出典 URL 付き** で記録する
- 日本語要約は原意を損なわず簡潔に（1〜3 文）
- 英語原文の重要引用はそのまま残す
