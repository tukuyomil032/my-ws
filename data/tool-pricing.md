# ツール料金・制限調査レポート

> 調査日: 2026-06-22（WebSearch による最新情報）
> 対象: 毎日情報収集ルーティーンで使用するAPI・ツール

---

## サマリーテーブル

| ツール | 無料利用可否 | 制限 | 推奨度 | 備考 |
|--------|-------------|------|--------|------|
| HackerNews Algolia API | ✅ 完全無料 | 10,000 req/hr (IP別) | ⭐⭐⭐ 最優先 | 認証不要 |
| Jina Reader (r.jina.ai) | ✅ 無料枠あり | 無料APIキー: 100 RPM / 1M tokens | ⭐⭐⭐ 推奨 | APIキー登録推奨 |
| GitHub REST API | ✅ 無料 | 認証なし: 60/hr, 認証あり: 5000/hr | ⭐⭐⭐ 推奨 | `gh` CLI で認証推奨 |
| Reddit API | ⚠️ 要登録 | OAuth必須, 100 req/min (非商用) | ⭐⭐ 要設定 | 匿名アクセス廃止済み |
| Brave Search API | ❌ 有料化 | $5/月クレジット (CC必須) | ⭐ 不要 | 2026/02に無料枠廃止 |
| RSS Feed Fetcher Skill | ✅ 完全無料 | MCPMarket 経由インストール | ⭐⭐⭐ 推奨 | APIキー不要 |
| OSINT Skill (smixs) | ✅ MIT無料 | Apify/検索API要登録 | ⭐⭐ 参考 | 外部APIキーが必要 |

---

## 1. HackerNews Algolia API

**URL**: https://hn.algolia.com/api  
**料金**: 完全無料・認証不要  
**レート制限**: IP別 約10,000 req/hr（公式明記なし、実運用上の上限）  
**最大ヒット数**: 1リクエストあたり最大1000件  

### 推奨使用方法
```
# 毎日のフロントページ取得（SA1で使用）
GET https://hn.algolia.com/api/v1/search_by_date?tags=front_page&hitsPerPage=10
```

### 注意事項
- 公式ドキュメントにレート制限の明記なし（フェアユース前提）
- 大量リクエストを短時間に送らないこと

---

## 2. Jina Reader API (r.jina.ai)

**URL**: https://jina.ai/reader/  
**料金モデル**:
- APIキーなし: IP別レート制限あり（上限不明確、控えめ）
- 無料APIキー: 1,000,000 トークン付与（非商用）、100 RPM / 100K TPM
- 有料プラン: ~$20/月〜（500 RPM / 2M TPM）

### 推奨設定
1. https://jina.ai で無料APIキーを取得（メール登録のみ）
2. ヘッダーに追加: `Authorization: Bearer YOUR_KEY`
3. 使用形式: `WebFetch https://r.jina.ai/[対象URL]`

### 注意事項
- 2025年5月に料金体系を変更（詳細は非公開・要確認）
- 非商用利用であれば無料枠で十分
- SA2で深層記事フルテキスト取得に使用

---

## 3. GitHub REST API

**URL**: https://docs.github.com/en/rest  
**料金**: 完全無料（認証あり・なし両方）  
**レート制限**:
- 認証なし（IP別）: **60 req/hr**
- 認証あり（Personal Access Token）: **5,000 req/hr**
- 2025年5月に更新あり（GitHub Changelog参照）

### 推奨設定
`gh` CLI（Claude Code標準搭載）を使い認証済みリクエストで5,000/hrを確保する。

```bash
# GitHub Trendingの代替（公式Trending APIなし）
gh api search/repositories \
  --method GET \
  -f q="stars:>1000 pushed:>2026-06-15" \
  -f sort="stars" \
  -f per_page=10
```

### 注意事項
- GitHub公式にはTrendingの専用APIエンドポイントなし
- `/trending` ページはWebFetch/agent-browserで取得する
- 認証なしだと60/hrは1日に何度もアクセスすると枯渇するため要注意

---

## 4. Reddit API

**URL**: https://www.reddit.com/dev/api/  
**⚠️ 重要な変更（2023年以降）**:
- 匿名/未認証アクセスは**廃止・ブロック**済み
- 2025年: 全アプリで**事前承認必須**（Responsible Builder Policy）
- 全アクセスにOAuth認証が必要

**無料枠**: OAuth認証後、100 req/min（非商用・10分窓平均）

### セットアップ手順（無料）
1. https://www.reddit.com/prefs/apps でアプリ登録（script タイプ）
2. Client ID・Secret を取得
3. OAuth2でアクセストークン取得（期限あり、自動更新）

### ルーティーンでの代替手段
Reddit APIが面倒な場合は WebSearch で代替:
```
WebSearch: "site:reddit.com/r/programming hot today"
```

---

## 5. Brave Search API

**⚠️ 2026年2月に無料枠廃止**  
**現在の料金**:
- $5/月のクレジット付き（要クレジットカード登録）
- $0.003〜$0.005 per query
- ~1,000クエリ/$5クレジット
- レート制限: 50 req/sec

### 結論
**使用しない**ことを推奨。WebSearch（Claude Code標準）で代替する。
もしどうしても使う場合は月の使用量を管理すること。

---

## 6. RSS Feed Fetcher Skill（MCPMarket）

**URL**: https://mcpmarket.com/tools/skills/rss-feed-fetcher  
**料金**: 完全無料  
**APIキー不要**: 標準CLIツール（curl等）を使用  

### インストール方法
MCPMarket の Skills Sync 経由でインストール:
```
/find-skills "RSS Feed Fetcher" でMCPMarketから同期
```

または類似の無料スキル:
- **RSS Feed Fetcher**: 外部APIキー不要、HNフィード等に最適
- **BlogWatcher**: RSS購読管理（blogwatcher CLI使用）
- **RSS Feed Operations**: URLからフィードを自動検出

### SA1での使用例
```
RSS Feed Fetcher でURL https://hn.algolia.com/api/v1/search_by_date?tags=front_page&hitsPerPage=10 を取得
```

---

## 7. OSINT Skill（smixs/osint-skill）

**GitHub**: https://github.com/smixs/osint-skill  
**ライセンス**: MIT（無料）  
**ステータス**: Early Beta  

### 機能
- 55+ Apify Actors 使用
- 7つの検索API統合
- 個人・組織の詳細調査（スコア付きレポート生成）
- Swarm Mode（並列エージェント）対応

### インストール
```bash
git clone https://github.com/smixs/osint-skill.git /tmp/osint-skill
cp -r /tmp/osint-skill/osint ~/.claude/skills/osint-skill
bash ~/.claude/skills/osint-skill/scripts/diagnose.sh
```

### 必要ツール
- curl, python3, jq（必須）
- Node.js 18+（Apify runner用）
- Apify APIキー（55+ actors使用時）
- 検索API（最低1つ: Brave/SerpApi等）

### ⚠️ 注意
- Apify + 検索APIが必要なため、**完全無料にはならない**
- SA3（地政学）・SA4（経済）では外部APIキーなしで動作しない可能性あり
- **代替案**: WebSearch + WebFetch で十分な場合はスキップ可

---

## 推奨ツール構成（完全無料・最小設定）

```
SA1 (技術トレンド):
  Primary: HackerNews Algolia API (完全無料)
  Secondary: WebFetch https://github.com/trending (JS不要版)
  Tertiary: WebSearch for Reddit

SA2 (技術深層):
  Primary: WebSearch + Jina Reader (無料APIキー取得)

SA3 (地政学):
  Primary: WebSearch + WebFetch (BBC/Reuters/AP)
  Optional: OSINT Skill (Apify APIあれば)

SA4 (経済):
  Primary: WebSearch + WebFetch

SA5 (文化・エンタメ):
  Primary: WebSearch

SA6 (科学):
  Primary: WebSearch + Jina Reader
```

**合計コスト: $0/月（Jina無料APIキー取得のみ必要）**
