# make-ppt

HTML slide authoring + PDF export pipeline, driven by Claude Code.

Write a slide in `slides/`, run one command, get a PDF.

---

## How it works

1. Write your slides as a single HTML file in `slides/`
2. Run `./run.sh` to convert to PDF via headless Chromium
3. Pick up the result from `output/`

```
slides/my-talk.html  →  output/my-talk.pdf
```

---

## Quick start

```bash
# install deps (first time only)
python3 -m venv venv
source venv/bin/activate
pip install playwright
playwright install chromium

# convert a single file
./run.sh slides/my-talk.html

# convert everything in slides/
./run.sh
```

---

## Project layout

```
make-ppt/
├── slides/          # put your HTML slides here
├── assets/          # background & decoration images
├── fonts/           # local font files (Tossface, Freesentation, Wanted Sans)
├── output/          # generated PDFs (git-ignored)
├── convert.py       # Playwright-based converter (don't touch)
├── run.sh           # entry point
├── CLAUDE.md        # authoring rules for Claude Code
└── DESIGN.md        # design system reference
```

---

## Slide format

Each `.html` file in `slides/` is a standalone deck. One `<div class="slide">` = one PDF page.

```html
<div class="slide slide-title">
  <!-- title page -->
</div>

<div class="slide slide-content">
  <!-- content page -->
</div>
```

Fixed canvas: **1920 × 1080px** (16:9).

---

## Assets

Background images and right-side decorations live in `assets/`.

| prefix | description |
|--------|-------------|
| `bg-dark-*.png` | dark abstract backgrounds (for title / section slides) |
| `bg-light-*.png` | light holographic backgrounds |
| `deco-right-*.png` | right-edge glow orbs (white background only) |

See `slides/asset-test.html` for a visual reference of every asset.

---

## Fonts

All fonts are bundled locally so PDF export works offline.

| font | use |
|------|-----|
| Tossface | emoji (always applied first) |
| Freesentation | Korean body text (presentation style) |
| Wanted Sans Variable | Korean body text (modern sans-serif) |

Pick one body font per deck — don't mix.

---

## License

MIT
