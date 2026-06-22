---
template-id: 6
name: Night Study
theme: Notebook
genre: reading
light-dark: dark
fonts: system-only
macrostructure: Bento Grid (notebook cards, left-edge accent)
nav: Minimal
references: Bear Notes dark, Things 3 dark, Craft Docs dark
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-bg: oklch(10% 0.015 50);
  --color-bg-2: oklch(14% 0.018 50);
  --color-ink: oklch(88% 0.012 75);
  --color-ink-2: oklch(58% 0.012 75);
  --color-accent: oklch(72% 0.15 75);
  --color-border: oklch(22% 0.015 50);
  --color-indicator-tech: oklch(62% 0.18 250);
  --color-indicator-world: oklch(62% 0.15 160);
  --font-body: -apple-system, "SF Pro Text", "Helvetica Neue", sans-serif;
  --font-reading: Georgia, "Times New Roman", serif;
  --space-sm: 0.75rem;
  --space-md: 1.5rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
}
```

## Layout Rule

- ヘッダー: シンプルなテキストヘッダーのみ
- コンテンツ: 2カラム Bento グリッド（モバイルは1カラム）
- 各記事カード: 左端3px のカラーインジケーター（Tech=ブルー、Other=グリーン系）
- カードは `background: var(--color-bg-2)` + 内側パディング
- セクションラベルはグリッド全幅にまたがる区切り行

## Typography Scale

- Header: system-ui 300, 0.9rem, letter-spacing 0.06em, ink-2
- Section label: system-ui 600, 0.65rem, letter-spacing 0.16em, uppercase, ink-2
- Card headline: system-ui 600, 0.95rem, line-height 1.3
- Card quote/body: Georgia 400 italic (引用のみ), system-ui 400 それ以外, 0.85rem
- Meta: system-ui 400, 0.7rem, ink-2

## Anti-patterns (BANNED)

- No nav (header label only)
- No category badge rainbow (indicator = 2 colors only: tech-blue, world-green)
- Left-edge indicator は許可 (T6 専用、border-leftではなくbox-shadow使用)
- No gradient backgrounds
- No hover card scale/shadow effects
- No Inter/Roboto/Arial
