#!/usr/bin/env python3
"""BNBHubs 'Private Edition' wallpaper pack for the Galaxy Z Fold 7 inner display.
5 skins, each in a dark + light variant, native 1968x2184."""
import os, math, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1968, 2184
OUT = "/tmp/wp"
os.makedirs(OUT, exist_ok=True)
OWNER = "MUHAMMAD"
SERIAL = "Nº 007 / 100"

# ---------- BNBHubs Red Sea coastal palette ----------
NAVY   = np.array([6, 11, 16]) / 255      # deep navy-black base
TEAL   = np.array([15, 181, 174]) / 255   # red sea teal
TEAL_D = np.array([8, 70, 74]) / 255       # deep teal
GOLD   = np.array([232, 176, 75]) / 255    # brand gold
GOLD_B = np.array([244, 205, 110]) / 255   # bright gold
CORAL  = np.array([232, 122, 96]) / 255    # red sea coral accent
IVORY  = np.array([244, 236, 221]) / 255   # warm ivory
SAND   = np.array([225, 207, 173]) / 255   # sand
CREAM  = np.array([243, 244, 242]) / 255   # airy light base

FONT_DIR = "/usr/share/fonts/truetype"
def font(path, size):
    return ImageFont.truetype(os.path.join(FONT_DIR, path), size)
F_SERIF      = "dejavu/DejaVuSerif.ttf"
F_SERIF_B    = "dejavu/DejaVuSerif-Bold.ttf"
F_SANS       = "liberation/LiberationSans-Regular.ttf"
F_SANS_B     = "liberation/LiberationSans-Bold.ttf"
F_MONO       = "liberation/LiberationMono-Regular.ttf"

# ---------- numpy helpers (work in float 0..1, HxWx3) ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
nx = xx / W            # 0..1
ny = yy / H

def to_img(arr):
    return Image.fromarray((np.clip(arr, 0, 1) * 255).astype(np.uint8), "RGB")

def vgrad(stops):
    """stops: list of (pos, rgb). vertical gradient."""
    pos = [s[0] for s in stops]
    cols = np.array([s[1] for s in stops])
    out = np.empty((H, W, 3), np.float32)
    col = ny[:, 0]
    for c in range(3):
        out[:, :, c] = np.interp(col, pos, cols[:, c])[:, None]
    return out

def screen(base, layer):
    return 1 - (1 - base) * (1 - layer)

def blob(cx, cy, rx, ry, color, strength=1.0, power=2.0):
    """soft radial field -> colored glow array (additive/screen friendly)."""
    d = ((xx - cx * W) / (rx * W)) ** 2 + ((yy - cy * H) / (ry * H)) ** 2
    a = np.exp(-(d ** (power / 2.0)) * 3.0) * strength
    return color[None, None, :] * a[:, :, None]

def grain(amount=0.015, mono=True):
    if mono:
        n = np.random.normal(0, amount, (H, W, 1)).astype(np.float32)
        return np.repeat(n, 3, axis=2)
    return np.random.normal(0, amount, (H, W, 3)).astype(np.float32)

def legibility(arr, mode):
    """darken extreme top (status bar) & bottom (nav) so white system UI stays
    legible in both light and dark mode; keep it gentle."""
    top = np.clip(1 - ny / 0.075, 0, 1) ** 1.5
    bot = np.clip(1 - (1 - ny) / 0.085, 0, 1) ** 1.5
    scrim = (top + bot)[:, :, None]
    strength = 0.30 if mode == "light" else 0.38
    return arr * (1 - scrim * strength)

def vignette(arr, strength=0.22):
    d = ((nx - 0.5) ** 2 + (ny - 0.5) ** 2)
    v = 1 - np.clip(d * 2.1, 0, 1) * strength
    return arr * v[:, :, None]

# ---------- personalization emblem (PIL overlay) ----------
def draw_text_spaced(draw, xy, text, fnt, fill, tracking=0, anchor_center=True):
    widths = [draw.textlength(ch, font=fnt) for ch in text]
    total = sum(widths) + tracking * (len(text) - 1)
    x = xy[0] - total / 2 if anchor_center else xy[0]
    asc, desc = fnt.getmetrics()
    y = xy[1] - (asc) / 2 if anchor_center else xy[1]
    for ch, w in zip(text, widths):
        draw.text((x, y), ch, font=fnt, fill=fill)
        x += w + tracking
    return total

def emblem_overlay(cx, cy, scale, ink, accent, hero=False, ring=True):
    """Returns an RGBA overlay with the BNBHUBS private-edition mark."""
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ic = (int(ink[0]*255), int(ink[1]*255), int(ink[2]*255))
    ac = (int(accent[0]*255), int(accent[1]*255), int(accent[2]*255))
    px, py = int(cx * W), int(cy * H)

    if ring:
        r = int(150 * scale)
        d.ellipse([px - r, py - r, px + r, py + r], outline=ac + (235,),
                  width=max(2, int(3 * scale)))
        r2 = int(176 * scale)
        d.ellipse([px - r2, py - r2, px + r2, py + r2], outline=ic + (90,),
                  width=max(1, int(1 * scale)))
        # tick marks around ring
        n = 60
        for i in range(n):
            a = i / n * 2 * math.pi
            long = (i % 5 == 0)
            r0 = r2 + int(6 * scale)
            r1 = r2 + int((20 if long else 11) * scale)
            d.line([px + r0*math.cos(a), py + r0*math.sin(a),
                    px + r1*math.cos(a), py + r1*math.sin(a)],
                   fill=ac + (170 if long else 90,), width=max(1, int(1.5*scale)))

    # monogram "B"
    fb = font(F_SERIF_B, int(150 * scale))
    bw = d.textlength("B", font=fb)
    asc, desc = fb.getmetrics()
    d.text((px - bw/2, py - (asc+desc)/2 - int(8*scale)), "B", font=fb, fill=ac + (255,))

    # wordmark + serial
    fw = font(F_SANS_B, int(34 * scale))
    draw_text_spaced(d, (px, py + int(120 * scale)), "B N B H U B S", fw,
                     ic + (240,), tracking=int(7 * scale))
    fs = font(F_MONO, int(20 * scale))
    draw_text_spaced(d, (px, py + int(160 * scale)), "PRIVATE  EDITION", fs,
                     ac + (210,), tracking=int(5 * scale))

    if hero:
        fserial = font(F_MONO, int(24 * scale))
        draw_text_spaced(d, (px, py + int(225 * scale)), SERIAL, fserial,
                         ic + (200,), tracking=int(4 * scale))
        fown = font(F_SANS, int(19 * scale))
        draw_text_spaced(d, (px, py + int(262 * scale)),
                         "CRAFTED EXCLUSIVELY FOR " + OWNER, fown,
                         ic + (150,), tracking=int(3 * scale))
    return ov

def small_serial_overlay(cx, cy, ink, accent, scale=1.0):
    ov = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d = ImageDraw.Draw(ov)
    ic = (int(ink[0]*255), int(ink[1]*255), int(ink[2]*255))
    ac = (int(accent[0]*255), int(accent[1]*255), int(accent[2]*255))
    px, py = int(cx * W), int(cy * H)
    fw = font(F_SANS_B, int(30 * scale))
    draw_text_spaced(d, (px, py), "B N B H U B S", fw, ic + (200,), tracking=int(8*scale))
    fs = font(F_MONO, int(18 * scale))
    draw_text_spaced(d, (px, py + int(34*scale)), "PRIVATE EDITION  ·  " + SERIAL,
                     fs, ac + (190,), tracking=int(3*scale))
    fo = font(F_SANS, int(16*scale))
    draw_text_spaced(d, (px, py + int(62*scale)), "FOR " + OWNER, fo, ic + (120,),
                     tracking=int(3*scale))
    return ov

def composite_overlay(arr, ov, blur=0):
    if blur:
        ov = ov.filter(ImageFilter.GaussianBlur(blur))
    base = to_img(arr).convert("RGBA")
    base.alpha_composite(ov)
    return np.asarray(base.convert("RGB")).astype(np.float32) / 255

# =====================================================================
# SKIN 1 — RED SEA HORIZON
# =====================================================================
def skin_horizon(mode):
    if mode == "dark":
        arr = vgrad([(0.0, NAVY), (0.32, TEAL_D*0.7), (0.55, TEAL_D),
                     (0.70, GOLD*0.55), (0.80, GOLD_B*0.9), (0.86, GOLD*0.5),
                     (1.0, NAVY*1.6)])
        sun_y, sun_col, sky_glow = 0.80, GOLD_B, TEAL
        ink, acc = IVORY, GOLD_B
    else:
        arr = vgrad([(0.0, np.array([0.95,0.93,0.88])), (0.35, SAND*1.05),
                     (0.58, np.array([0.97,0.85,0.66])), (0.74, GOLD_B),
                     (0.82, GOLD*0.95), (1.0, np.array([0.88,0.80,0.66]))])
        sun_y, sun_col, sky_glow = 0.80, np.array([1,1,0.96]), TEAL*0.5+SAND*0.5
        ink, acc = np.array([0.20,0.16,0.10]), np.array([0.60,0.42,0.12])

    glow = blob(0.5, sun_y, 0.55, 0.16, sky_glow, 0.5, 1.6)
    arr = screen(arr, glow)
    sun = blob(0.5, sun_y, 0.16, 0.075, sun_col, 0.95, 1.8)
    arr = screen(arr, sun)
    # thin luminous horizon line
    line = np.exp(-((ny - sun_y) ** 2) / (2 * 0.0009 ** 2))
    arr = screen(arr, (sun_col)[None,None,:] * line[:,:,None] * (0.6 if mode=="dark" else 0.4))
    # faint reflection shimmer below
    for k in range(1, 6):
        yk = sun_y + 0.03 * k
        sh = np.exp(-((ny - yk) ** 2) / (2 * 0.0016 ** 2)) * (0.18 / k)
        sh = sh * (0.6 + 0.4*np.sin(nx*40 + k))
        arr = screen(arr, sun_col[None,None,:] * sh[:,:,None])
    arr = arr + grain(0.012)
    ov = small_serial_overlay(0.5, 0.135, ink, acc, 1.05)
    arr = composite_overlay(arr, ov)
    return finalize(arr, mode)

# =====================================================================
# SKIN 2 — MARINA DEPTHS (topographic contours)
# =====================================================================
def skin_depths(mode):
    if mode == "dark":
        base = vgrad([(0.0, NAVY*1.3), (0.5, TEAL_D*0.85), (1.0, NAVY)])
        linecol, ink, acc = GOLD_B, IVORY, GOLD_B
        lstr = 0.9
    else:
        base = vgrad([(0.0, np.array([0.93,0.95,0.94])), (0.5, np.array([0.86,0.90,0.89])),
                      (1.0, SAND*1.0)])
        linecol, ink, acc = TEAL_D*0.85, np.array([0.16,0.20,0.20]), np.array([0.55,0.40,0.12])
        lstr = 0.95
    # smooth scalar field = sum of gaussian "islands"
    field = np.zeros((H, W), np.float32)
    centers = [(0.30, 0.40, 0.34, 1.0), (0.72, 0.66, 0.40, 0.9),
               (0.55, 0.18, 0.26, 0.6), (0.18, 0.85, 0.30, 0.7)]
    for cx, cy, r, w in centers:
        field += w * np.exp(-(((nx-cx)**2 + ((ny-cy)*0.92)**2) / (2*r*r)))
    field += 0.10 * np.sin(nx*6.0) + 0.10 * np.cos(ny*5.0)
    field = (field - field.min()) / (field.max() - field.min())
    N = 26
    fN = field * N
    dist = np.abs(fN - np.round(fN))
    grad = np.abs(np.gradient(field)[0]) + np.abs(np.gradient(field)[1]) + 1e-4
    width = 0.10 / (grad * N + 0.6)
    lines = np.clip(1 - dist / np.clip(width, 0.02, 0.5), 0, 1) ** 1.4
    arr = base.copy()
    a = (lines * lstr)[:, :, None]
    if mode == "dark":
        arr = screen(arr, linecol[None, None, :] * a)          # glowing gold lines
    else:
        arr = arr * (1 - a) + arr * linecol[None, None, :] * a  # multiply: dark teal lines
        # warm gold every 4th contour for richness
        gold_lines = (np.round(fN) % 4 == 0).astype(np.float32) * lines * 0.5
        ag = gold_lines[:, :, None]
        arr = arr * (1 - ag) + arr * acc[None, None, :] * 1.4 * ag
    # accent gold peak glow on highest island
    arr = screen(arr, blob(0.30, 0.40, 0.22, 0.20, acc, 0.18 if mode=='dark' else 0.10, 1.6))
    arr = arr + grain(0.010)
    ov = small_serial_overlay(0.5, 0.135, ink, acc, 1.05)
    arr = composite_overlay(arr, ov)
    return finalize(arr, mode)

# =====================================================================
# SKIN 3 — GOUNA DUNES (layered wave/dune bands)
# =====================================================================
def skin_dunes(mode):
    if mode == "dark":
        arr = vgrad([(0.0, NAVY*1.2), (1.0, TEAL_D*0.6)])
        layers = [
            (0.42, GOLD*0.30, 0.045, 3.0, 0.0),
            (0.55, TEAL_D*1.1, 0.05, 2.3, 1.1),
            (0.66, GOLD*0.45, 0.04, 2.8, 2.0),
            (0.77, TEAL*0.5,  0.05, 1.9, 0.4),
            (0.88, GOLD_B*0.8,0.035, 3.4, 3.0),
        ]
        ink, acc, hl = IVORY, GOLD_B, GOLD_B
    else:
        arr = vgrad([(0.0, CREAM), (1.0, SAND*1.0)])
        layers = [
            (0.42, np.array([0.92,0.88,0.80]), 0.045, 3.0, 0.0),
            (0.55, np.array([0.85,0.90,0.86]), 0.05, 2.3, 1.1),
            (0.66, GOLD_B*0.85, 0.04, 2.8, 2.0),
            (0.77, np.array([0.80,0.86,0.84]), 0.05, 1.9, 0.4),
            (0.88, GOLD*0.9, 0.035, 3.4, 3.0),
        ]
        ink, acc, hl = np.array([0.20,0.16,0.10]), np.array([0.60,0.42,0.12]), np.array([1,1,0.95])
    xrow = nx[0]  # 1D x coordinate (W,)
    for base_y, col, amp, freq, ph in layers:
        curve = base_y + amp * np.sin(xrow * freq * math.pi * 2 + ph) \
                       + amp*0.4 * np.sin(xrow * freq * 4.3 * math.pi + ph*1.7)
        mask = np.clip((ny - curve[None, :]) / 0.010, 0, 1)
        # vertical shading within the band
        shade = 0.75 + 0.25 * np.clip((ny - curve[None,:]) / 0.12, 0, 1)
        layer_col = col[None,None,:] * shade[:,:,None]
        m = mask[:, :, None]
        arr = arr * (1 - m) + layer_col * m
        # crest highlight
        crest = np.clip(1 - np.abs(ny - curve[None,:]) / 0.004, 0, 1) ** 2
        arr = screen(arr, hl[None,None,:] * crest[:,:,None] * (0.5 if mode=='dark' else 0.3))
    arr = arr + grain(0.010)
    ov = small_serial_overlay(0.5, 0.135, ink, acc, 1.05)
    arr = composite_overlay(arr, ov)
    return finalize(arr, mode)

# =====================================================================
# SKIN 4 — AURORA MESH (fluid gradient)
# =====================================================================
def skin_mesh(mode):
    if mode == "dark":
        pts = [(0.18,0.14,TEAL_D*1.1,0.42),(0.85,0.20,GOLD*0.8,0.40),
               (0.50,0.45,TEAL*0.9,0.5),(0.15,0.72,CORAL*0.7,0.38),
               (0.88,0.80,GOLD_B*0.9,0.42),(0.5,0.97,NAVY,0.5),(0.5,0.02,NAVY,0.4)]
        bg = NAVY
        ink, acc = IVORY, GOLD_B
    else:
        pts = [(0.18,0.14,np.array([0.80,0.92,0.90]),0.42),
               (0.85,0.20,GOLD_B,0.40),(0.50,0.45,np.array([0.86,0.94,0.92]),0.5),
               (0.15,0.72,np.array([0.97,0.86,0.80]),0.40),
               (0.88,0.80,SAND*1.05,0.42),(0.5,0.97,CREAM,0.5),(0.5,0.02,CREAM,0.45)]
        bg = CREAM
        ink, acc = np.array([0.20,0.18,0.14]), np.array([0.58,0.42,0.14])
    wsum = np.zeros((H, W), np.float32)
    acc_c = np.zeros((H, W, 3), np.float32)
    for cx, cy, col, r in pts:
        w = np.exp(-(((nx-cx)**2 + (ny-cy)**2) / (2*r*r)))
        wsum += w
        acc_c += col[None,None,:] * w[:,:,None]
    arr = acc_c / (wsum[:,:,None] + 1e-5)
    arr = 0.85*arr + 0.15*bg[None,None,:]
    arr = to_img(arr).filter(ImageFilter.GaussianBlur(40))
    arr = np.asarray(arr).astype(np.float32)/255
    arr = arr + grain(0.012)
    ov = small_serial_overlay(0.5, 0.135, ink, acc, 1.05)
    arr = composite_overlay(arr, ov)
    return finalize(arr, mode)

# =====================================================================
# SKIN 5 — SIGNATURE EMBLEM (hero, 1-in-100)
# =====================================================================
def skin_signature(mode):
    if mode == "dark":
        arr = vgrad([(0.0, NAVY*1.4),(0.45, TEAL_D*0.7),(0.5, TEAL_D*0.75),
                     (0.55, TEAL_D*0.7),(1.0, NAVY*1.1)])
        ink, acc = IVORY, GOLD_B
        ray_col = GOLD
    else:
        arr = vgrad([(0.0, CREAM),(0.5, np.array([0.92,0.94,0.92])),(1.0, SAND*1.0)])
        ink, acc = np.array([0.15,0.18,0.18]), np.array([0.55,0.40,0.12])
        ray_col = GOLD*0.7
    cx, cy = 0.5, 0.43
    # radiant sunburst behind emblem
    ang = np.arctan2((yy - cy*H), (xx - cx*W))
    rad = np.sqrt(((xx-cx*W)/W)**2 + ((yy-cy*H)/H)**2)
    rays = (0.5 + 0.5*np.sin(ang * 36)) ** 3
    falloff = np.clip(1 - rad/0.42, 0, 1) ** 1.5
    arr = screen(arr, ray_col[None,None,:] * (rays*falloff)[:,:,None] * (0.22 if mode=='dark' else 0.12))
    arr = screen(arr, blob(cx, cy, 0.34, 0.30, acc, 0.20 if mode=='dark' else 0.10, 1.8))
    arr = arr + grain(0.010)
    ov = emblem_overlay(cx, cy, 1.18, ink, acc, hero=True, ring=True)
    arr = composite_overlay(arr, ov)
    return finalize(arr, mode)

# ---------- shared finalize ----------
def finalize(arr, mode):
    arr = vignette(arr, 0.20 if mode == "dark" else 0.12)
    arr = legibility(arr, mode)
    return to_img(arr)

SKINS = [
    ("01-red-sea-horizon", skin_horizon),
    ("02-marina-depths",   skin_depths),
    ("03-gouna-dunes",     skin_dunes),
    ("04-aurora-mesh",     skin_mesh),
    ("05-signature",       skin_signature),
]

if __name__ == "__main__":
    np.random.seed(7)
    for name, fn in SKINS:
        for mode in ("dark", "light"):
            img = fn(mode)
            p = os.path.join(OUT, f"bnbhubs-fold7-{name}-{mode}.png")
            img.save(p, "PNG")
            print("saved", p, img.size)
    print("DONE")
