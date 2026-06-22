---
template-id: 2
name: Magazine
theme: Monocle
genre: editorial
light-dark: light
fonts: google
macrostructure: Marquee Hero (fullwidth + tabbed sections)
nav: Top floating (N5)
references: Monocle Magazine, Wallpaper*, It's Nice That
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-paper: oklch(100% 0 0);
  --color-ink: oklch(15% 0.005 240);
  --color-ink-2: oklch(45% 0.005 240);
  --color-accent: oklch(28% 0.06 245);
  --color-border: oklch(88% 0.005 240);
  --color-hero-bg: oklch(15% 0.005 240);
  --font-display: "DM Serif Display", Georgia, serif;
  --font-body: "DM Sans", system-ui, sans-serif;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 4rem;
  --space-xl: 7rem;
}
```

## Layout Rule

- **Hero zone** (fullwidth): ダーク背景 (color-hero-bg)、巨大見出し、白テキスト。週次ラベルとチャプター数を表示
- **Tab nav**: Hero下のカテゴリータブ (Technology / World / Economy / Science / Culture)
- **Content area**: 選択タブのコンテンツを3カラムカードグリッドで表示
- Tab switching: Vanilla JS — `.tab-content` の display 切り替え
- カラムはモバイル1→タブレット2→デスクトップ3

## Typography Scale

- Hero headline: DM Serif Display 400, clamp(3rem, 7vw, 6rem), white
- Hero sub: DM Sans 400, 1rem, opacity 0.6
- Tab label: DM Sans 500, 0.8rem, letter-spacing 0.1em
- Card title: DM Serif Display 400, 1.3rem
- Card body: DM Sans 400, 0.9rem, line-height 1.6
- Meta: DM Sans 400, 0.75rem, color ink-2

## Anti-patterns (BANNED)

- No colored sidebar
- No 5-color rainbow (accent is navy only)
- No card hover background
- No border-left coloring
- No gradient backgrounds (hero is flat dark, not gradient)
- No Inter/Roboto/Arial
