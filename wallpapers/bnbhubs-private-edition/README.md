# BNBHubs — Private Edition Wallpaper Pack

A custom wallpaper collection for the **Samsung Galaxy Z Fold 7** (inner display,
native **1968 × 2184**), designed in the BNBHubs Red Sea coastal brand palette
— deep navy-black, Red Sea teal, brand gold, with warm sand/ivory and a touch of
coral. Each skin ships as a **dark** and a **light** variant, like the wallpaper
packs Apple/Samsung bundle, with status-bar and nav-bar legibility zones baked in
so the system UI stays readable in both system themes.

Personalized as a numbered **Private Edition · Nº 007 / 100**, crafted for
MUHAMMAD.

## The 5 skins

| # | Skin | Vibe |
|---|------|------|
| 01 | **Red Sea Horizon** | Sunset/sunrise glow over a teal sea with a luminous gold horizon and shimmer. |
| 02 | **Marina Depths** | Topographic depth-contour lines — gold glow (dark) / teal + gold (light). |
| 03 | **Gouna Dunes** | Layered dune/wave bands with crest highlights. |
| 04 | **Aurora Mesh** | Fluid blurred mesh gradient, iOS-style. |
| 05 | **Signature** | Hero emblem: BNBHUBS monogram, sunburst, serial number + owner tag. |

Each file: `bnbhubs-fold7-<skin>-<dark|light>.png`
Preview: `_preview-contact-sheet.png`

## How to apply (One UI)
1. Save the PNG to the phone (Gallery / Files).
2. Long-press home screen → **Wallpaper and style** → **Change wallpaper** →
   pick the image from Gallery.
3. Use the **dark** variant when your system theme is Dark, the **light** variant
   for Light — or set each on Lock vs Home.

## Regenerating / tweaking
`generate.py` (Pillow + numpy) is fully procedural — colors, serial number, and
owner name are constants at the top. Re-run:

```bash
pip install Pillow numpy
python generate.py   # writes to /tmp/wp
```
