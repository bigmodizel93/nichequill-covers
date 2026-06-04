# BNBHubs — ONE OF ONE · Unicorn-Rare Wallpaper Pack

A one-of-one wallpaper collection for the **Samsung Galaxy Z Fold 7** (inner
display, native **1968 × 2184**), in the BNBHubs Red Sea coastal palette — deep
navy-black, Red Sea teal, brand gold, warm sand/ivory, a touch of coral. Each
skin ships as a **dark** and a **light** variant, with status-bar / nav-bar
legibility zones baked in so the system UI stays readable in either theme.

## What makes it *yours* (the unicorn-rare layer)
- **Edition: `ONE OF ONE`** — not 1-of-100, the only one in existence.
- **Wax-seal monogram `M`** — your initial as an engraved, scalloped seal.
- **Hero certificate** that spells out **MUHAMMAD** in fine serif.
- **Guilloché engraving** — the hypotrochoid rosette used on banknotes,
  passports and luxury watch dials; effectively impossible to copy by eye.
- **Holographic iridescence** — an oil-slick "unicorn" sheen across every skin.
- **Authenticity fingerprint** — `C0CE·2FCA·1EB1·8A92`, deterministically derived
  from your name (`SHA-256("MUHAMMAD·BNBHUBS·ONE-OF-ONE·RED-SEA")`). Change the
  name and the fingerprint, sparkle layout, and shimmer all change with it.
- **Minted MMXXVI · El Gouna · Red Sea.**

## The 5 skins

| # | Skin | Vibe |
|---|------|------|
| 01 | **Red Sea Horizon** | Sun/moon glow over a teal sea, luminous gold horizon + shimmer. |
| 02 | **Marina Depths** | Topographic depth-contour engraving — gold glow (dark) / teal+gold (light). |
| 03 | **Gouna Dunes** | Layered dune/wave bands with lit crests. |
| 04 | **Unicorn Aurora** | Full holographic iridescent flow with scattered gem sparkles. |
| 05 | **One of One** | Hero certificate: wax-seal `M`, guilloché rosette, your name, fingerprint. |

Files: `bnbhubs-fold7-<skin>-<dark|light>.png` · Preview: `_preview-contact-sheet.png`

## How to apply (One UI)
1. Save the PNG to the phone (Gallery / Files).
2. Long-press home screen → **Wallpaper and style** → **Change wallpaper** →
   pick the image from Gallery.
3. Use the **dark** variant in Dark mode, **light** in Light mode — or split them
   across Lock vs Home.

## Regenerating / re-skinning
`generate.py` (Pillow + numpy) is fully procedural. `OWNER`, `INITIAL`,
`EDITION` and the palette are constants at the top; the fingerprint and sparkle
seed are derived from `OWNER`, so the artwork is reproducible and uniquely tied
to the name.

```bash
pip install Pillow numpy
python generate.py   # writes to /tmp/wp
```
