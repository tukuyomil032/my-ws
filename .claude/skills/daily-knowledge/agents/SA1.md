---
name: sa1-tech-trends
description: >
  SA1 — 技術トレンド収集エージェント。
  HackerNews Algolia API・GitHub Trending・Reddit 技術系サブレディットから
  今日のホット投稿を収集し、親が指定する個別ステージングファイルへ出力する。
---

# SA1: 技術トレンド

**モデル**: Claude Haiku 4.5（Claude）/ gpt-5.4-mini（Codex）  
**最終統合先（親が書き込む）**: `data/knowledge/Technology/YYYY/MM/WN(月-日_月-日).md`

---

## 収集対象

今日の技術系トレンドを以下の 3 ソースから収集する。

---

## Tools

### 1. HackerNews Algolia API（認証不要・完全無料）

```
WebFetch: https://hn.algolia.com/api/v1/search_by_date?tags=front_page&hitsPerPage=10
```

- JSON レスポンスから `hits` 配列を抽出
- 各 hit の `title`・`url`・`points` を取得
- 上位 5〜8 件を対象にする

### 2. GitHub Trending

```
WebFetch: https://github.com/trending
```

- ページ HTML から上位 10 件のリポジトリ名・説明・スター数を抽出
- 言語フィルタなし（全言語）

### 3. Reddit 技術系（WebSearch 経由）

以下のクエリで各サブレディットのホット投稿を収集:

```
WebSearch: site:reddit.com/r/programming hot today
WebSearch: site:reddit.com/r/rust hot today
WebSearch: site:reddit.com/r/webdev hot today
```

---

## 出力フォーマット

親が指定するSA1用ステージングファイルへ以下のフォーマットで出力する。Tech週次ファイルは直接変更しない:

```markdown
## YYYY-MM-DD - 技術トレンド

### GitHub Trending
- [リポジトリ名](URL) - 日本語要約（1文） ★スター数

### HackerNews Top
- [記事タイトル](URL) - 一言日本語要約

### Reddit ハイライト
- [投稿タイトル](URL) - スレッドの要点（日本語）
```

---

## 注意事項

- GitHub Trending の URL は `https://github.com/owner/repo` 形式で記録する
- 既存週次ファイルに同じ `owner/repo` がある場合、再度 Trending に出ていても候補止まりにする。新しい release、security advisory、major funding など別の新事実を確認できる場合だけ採用する
- スター数はISO 8601相当の取得日時・タイムゾーンを併記できる場合だけ、`1.2k` などの略記で記録してよい。取得時点が不明なら数値を省く
- Reddit は投稿タイトルのみ把握できた場合も URL なしで記録しない（`site:` 検索で取得できた URL を使う）
