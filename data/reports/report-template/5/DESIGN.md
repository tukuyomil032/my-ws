---
template-id: 5
name: Linear
theme: Workbench
genre: developer-tool
light-dark: dark
fonts: google+system
macrostructure: Workbench (dense rows, monospace meta)
nav: Slim top bar (N7)
references: Linear.app, Vercel Dashboard, Raycast, Supabase
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-bg: oklch(8% 0.01 260);
  --color-bg-2: oklch(12% 0.012 260);
  --color-ink: oklch(90% 0.005 260);
  --color-ink-2: oklch(55% 0.008 260);
  --color-accent: oklch(65% 0.22 250);
  --color-border: oklch(22% 0.012 260);
  --font-body: system-ui, "SF Pro Text", sans-serif;
  --font-mono: "JetBrains Mono", "SF Mono", "Cascadia Code", monospace;
  --space-sm: 0.75rem;
  --space-md: 1.5rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
}
```

## Layout Rule

- Slim top bar: ブランド左、週次ラベル右
- メインコンテンツ: 1カラム、max-width: 860px
- セクション区切り: `border-top: 1px solid var(--color-border)` + 薄いセクションラベル行
- 記事アイテム: 水平ロー形式。見出し左、ソース+日付右（JetBrains Mono）
- 記事本文: 折り畳み可能（詳細はデフォルト展開）

## Typography Scale

- Top bar: system-ui 500, 0.78rem
- Section label: system-ui 600, 0.68rem, letter-spacing 0.12em, uppercase, ink-2
- Article headline: system-ui 500, 0.95rem
- Article body: system-ui 400, 0.88rem, ink-2, line-height 1.6
- Meta (source/date): JetBrains Mono 400, 0.72rem, ink-2

## Anti-patterns (BANNED)

- No colored sidebar
- No category badge rainbow (accent blue only)
- No card hover background (only row border change)
- No border-left color coding
- No gradient backgrounds
- No rounded corners on content items
- No Inter/Roboto/Arial
