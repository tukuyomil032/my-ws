---
last_updated: "2026-06-22"
signals_total: 4
---

# 興味プロファイル

## この人について

AIエージェントと自動化を使い、技術・社会・文化・科学の情報を継続的に蓄積する個人情報プラットフォームを構築している。単なるニュース収集ではなく、過去と現在の関心を構造化し、開発相談や意思決定の解像度を高めることを重視している。

## 今の関心（直近14日）

**個人情報プラットフォームと知識管理。** `interest-profile`、週次Markdown、週次・月次HTML、NotebookLMポッドキャストを接続し、毎日の収集から振り返りまでを一貫して自動化しようとしている。TechnologyとOtherを分け、興味の外側も意図的に収集する設計への関心が強い。

**エージェント委任とモデルルーティング。** 複数の専門サブエージェントへ調査を分担し、HTML生成だけ高性能モデルへ任せるなど、品質・速度・コストを役割ごとに最適化したいと考えている。Codex、Claude、スキル、定期実行を組み合わせたオーケストレーションを深掘りしている。

**Web情報取得と安全な認証管理。** Jina AI Readerを調査基盤へ組み込み、APIキーを安全に管理しながら記事本文を精度高く取得する方法に関心がある。

## 継続的な関心

現時点では初回同期のため、14日を超える継続シグナルはまだない。

## 新規探索のヒント

**情報の信頼度スコアリング。** 出典の一次性、複数ソース一致、更新時刻を指標化すると、蓄積した知識を開発判断へ再利用しやすくなる。

**全文検索と意味検索の併用。** Markdown資産に対してキーワード検索と埋め込み検索を組み合わせると、過去の関心や判断根拠を短時間で取り出せる。

**情報の陳腐化管理。** 技術仕様や世界情勢に有効期限と再検証日を持たせることで、古い知識を現在の事実として扱うリスクを下げられる。

---

## 技術スタック（Claude Code 会話履歴より抽出・2026-06-22）

> Claude Code の全プロジェクト会話履歴（21プロジェクト、約 360MB）を ai-title レコードから分析した結果。

### 主要言語

- **Swift** — macOS ネイティブアプリ開発（perch: Dynamic Notch アプリ、codexbar: AI 使用量バー）
- **TypeScript / JavaScript** — CLI・デスクトップアプリ・Web アプリ全般（全 JS-TS プロジェクト共通）
- **Rust** — Tauri v2 のバックエンドとして複数プロジェクトで使用（MC-Vector、Yomu、portal-gate）
- **Python** — スクリプト・自動化・Claude Code スキル開発（video-frame-reader スキルなど）

### フレームワーク・ライブラリ

- **Tauri v2** — 主力デスクトップフレームワーク。Electron・Wails から移行済み（Yomu、MC-Vector、portal-gate）
- **React** — Tauri v2 のフロントエンド。複数プロジェクトで標準採用
- **SwiftUI / AppKit** — perch の UI 実装（ノッチ UI・波形アニメーション）
- **Vite / Vite 8** — フロントエンドバンドラー（vite-plus-migration 実施済み）
- **Tailwind CSS v4** — フロントエンドスタイリング（v4 マイグレーション実施済み）
- **Lottie** — perch の AI プロバイダーロゴアニメーション

### テスト

- **Playwright** — E2E テスト（MC-Vector で Mocha/Selenium から移行）
- **Vitest** — ユニットテスト（MC-Vector、portal-gate で採用）

### ツール・インフラ

- **GitHub Actions** — ビルド・CI/CD・DMG 生成・npm OIDC 公開・Homebrew tap 配布
- **Bun** — CLI ツールおよび CI スクリプトのランタイム
- **Homebrew tap** — perch の macOS アプリ配布
- **Biome** — ESLint/Prettier の代替として MC-Vector で導入
- **FFmpeg** — 動画フレーム抽出（video-frame-reader スキル）
- **NotebookLM** — CLI ツール（nlm-custom-prompt-viewer）・知識基盤（my-ws）・大学志望理由書生成

### 開発ドメイン

- **macOS Dynamic Notch / メニューバーアプリ** — perch（Now Playing・AI 使用量ウィジェット・歌詞表示）、codexbar
- **クロスプラットフォームデスクトップアプリ** — Tauri v2 ベース（Yomu・MC-Vector・portal-gate）
- **CLI ツール** — stela（GitHub リポジトリ検索・npm 公開済み）、nlm-custom-prompt-viewer（NotebookLM 連携）
- **Minecraft 関連ツール** — MC-Vector（サーバー管理アプリ）
- **個人用知識基盤** — my-ws（現在構築中の情報プラットフォーム）
