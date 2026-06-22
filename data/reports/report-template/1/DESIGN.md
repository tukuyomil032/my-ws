---
template-id: 1
name: Broadsheet
theme: Newsprint
genre: editorial
light-dark: light
fonts: google
macrostructure: Newsprint (2-column masonry)
nav: Horizontal category bar (N6)
references: New York Times, Financial Times, Le Monde
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-paper: oklch(97% 0.015 80);
  --color-ink: oklch(12% 0.01 220);
  --color-ink-2: oklch(35% 0.01 220);
  --color-accent: oklch(42% 0.18 25);
  --color-border: oklch(82% 0.01 80);
  --font-display: "Playfair Display", Georgia, serif;
  --font-body: "Source Serif 4", Georgia, serif;
  --font-ui: system-ui, sans-serif;
  --space-sm: 0.75rem;
  --space-md: 1.5rem;
  --space-lg: 3rem;
  --space-xl: 5rem;
  --radius: 0px;
}
```

## Layout Rule

2カラムグリッド: `grid-template-columns: 3fr 2fr`
- 左列 (60%): TECH_ARTICLES — Technology セクション
- 右列 (40%): OTHER_ARTICLES — World / Economy / Science / Culture を縦積み
- カラム間: 1px solid var(--color-border) の縦罫線
- セクション間: 水平罫線で区切り（border-top: 2px solid）
- Dateline スタイル: 小文字スモールキャプス、インクカラー

## Typography Scale

- Masthead: Playfair Display 700, 2.5rem
- Section header: Playfair Display 700 italic, 1rem, letter-spacing 0.15em, uppercase
- Article headline: Playfair Display 600, 1.3rem〜1.6rem
- Body copy: Source Serif 4 400, 0.95rem, line-height 1.65
- Meta / dateline: system-ui 400, 0.75rem, color: var(--color-ink-2)
- Source link: system-ui 400, 0.8rem

## Anti-patterns (BANNED)

- No colored sidebar
- No category badge rainbow (max 2 accent colors across whole page)
- No card hover background change
- No border-left color coding on items
- No gradient backgrounds
- No rounded corners (radius: 0px — newspaper aesthetic)
- No box-shadow on cards
- No Inter/Roboto/Arial
