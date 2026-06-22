---
template-id: 3
name: Minimal Apple
theme: Editorial
genre: minimal
light-dark: light
fonts: system-only
macrostructure: Long Document (1-column scroll)
nav: Sticky anchor nav (N8)
references: apple.com/newsroom, Stripe, Linear (light)
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-paper: oklch(100% 0 0);
  --color-ink: oklch(13% 0 0);
  --color-ink-2: oklch(55% 0 0);
  --color-accent: oklch(50% 0.22 250);
  --color-surface: oklch(97% 0 0);
  --color-border: oklch(90% 0 0);
  --font-display: -apple-system, "SF Pro Display", "Helvetica Neue", sans-serif;
  --font-body: -apple-system, "SF Pro Text", "Helvetica Neue", sans-serif;
  --space-sm: 1rem;
  --space-md: 2rem;
  --space-lg: 5rem;
  --space-xl: 9rem;
}
```

## Layout Rule

- 1カラム縦スクロール。max-width: 720px センタリング
- Sticky anchor nav: 上部に固定、アンカーリンクで各セクションへスクロール
- セクション間: 大きな余白 (space-xl) で区切り
- Tech先、Other後の順で表示
- セクションヘッダーは極小のUI文字、大きな余白

## Typography Scale

- Nav label: system-ui 500, 0.75rem, letter-spacing 0.04em
- Section header: system-ui 700, 0.7rem, letter-spacing 0.14em, uppercase, ink-2
- Article headline: SF Pro Display 700, 1.5rem, letter-spacing -0.02em
- Body: SF Pro Text 400, 1rem, line-height 1.75
- Meta: system-ui 400, 0.78rem, ink-2

## Anti-patterns (BANNED)

- No colored sidebar
- No category badge rainbow
- No card hover backgrounds
- No border-left color coding
- No gradient backgrounds
- No drop shadows
- No rounded cards
- No Inter/Roboto/Arial/any Google Font (system fonts only)
