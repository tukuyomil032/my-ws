---
template-id: 4
name: Wabi
theme: Sabi
genre: minimal-jp
light-dark: light
fonts: google+system
macrostructure: Manifesto (long scroll, typographic dividers)
nav: Anchor-only (minimal)
references: MUJI, 侘寂(wabi-sabi), 余白(ma), MARK magazine JP
---

/* Hallmark · pre-emit critique: P5 H5 E5 S5 R5 V5 */

## Tokens

```css
:root {
  --color-paper: oklch(96% 0.008 90);
  --color-ink: oklch(14% 0.01 200);
  --color-ink-2: oklch(48% 0.008 200);
  --color-accent: oklch(42% 0.2 28);
  --color-border: oklch(78% 0.008 90);
  --font-display: "Noto Serif JP", "Hiragino Mincho ProN", Georgia, serif;
  --font-body: system-ui, "Hiragino Kaku Gothic ProN", sans-serif;
  --space-sm: 1rem;
  --space-md: 2.5rem;
  --space-lg: 6rem;
  --space-xl: 10rem;
}
```

## Layout Rule

- 1カラム、max-width: 640px、左右に大きな余白
- セクション間: 大きな余白 (space-xl)
- 区切り: テキスト区切り線 (`───`) または細い罫線のみ
- アクセント朱赤は記事ソースリンクのみに使用 (極度にスパリング)
- 見出しは控えめに — 新聞スタイルではなく、書道の余白感

## Typography Scale

- Section header: Noto Serif JP 700, 0.75rem, letter-spacing 0.2em, vertical feeling
- Article headline: Noto Serif JP 400, 1.25rem, line-height 1.4, letter-spacing 0.02em
- Body: system-ui 400, 0.9rem, line-height 1.85
- Meta: system-ui 400, 0.72rem, ink-2
- Source link: system-ui 400, 0.72rem, accent (朱赤)

## Anti-patterns (BANNED)

- No colored sidebar, no nav (minimal/no nav only)
- No category badge rainbow (accent in 1 place only)
- No card borders or box-shadow
- No border-left color coding
- No gradient backgrounds
- No rounded corners
- No hover effects on articles (only on links)
- No Inter/Roboto/Arial
