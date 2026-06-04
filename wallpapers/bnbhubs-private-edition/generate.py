#!/usr/bin/env python3
"""BNBHubs 'ONE OF ONE' unicorn-rare wallpaper pack — Galaxy Z Fold 7 inner display.
5 skins, each dark + light, native 1968x2184. Guilloche engraving, wax-seal
monogram, holographic iridescence, and a unique authenticity fingerprint."""
import os, math, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

W, H = 1968, 2184
OUT = "/tmp/wp"
os.makedirs(OUT, exist_ok=True)

# ---------- identity ----------
OWNER   = "MUHAMMAD"
INITIAL = "M"
EDITION = "ONE OF ONE"
_h = hashlib.sha256(f"{OWNER}·BNBHUBS·ONE-OF-ONE·RED-SEA".encode()).hexdigest().upper()
FINGERPRINT = f"{_h[0:4]}·{_h[4:8]}·{_h[8:12]}·{_h[12:16]}"
SEED_INT = int(_h[:8], 16)
MINTED = "MMXXVI"   # 2026

# ---------- BNBHubs Red Sea coastal palette ----------
NAVY   = np.array([6, 11, 16]) / 255
TEAL   = np.array([15, 181, 174]) / 255
TEAL_D = np.array([8, 70, 74]) / 255
GOLD   = np.array([232, 176, 75]) / 255
GOLD_B = np.array([244, 205, 110]) / 255
CORAL  = np.array([232, 122, 96]) / 255
IVORY  = np.array([244, 236, 221]) / 255
SAND   = np.array([225, 207, 173]) / 255
CREAM  = np.array([243, 244, 242]) / 255

FONT_DIR = "/usr/share/fonts/truetype"
def font(path, size): return ImageFont.truetype(os.path.join(FONT_DIR, path), size)
F_SERIF   = "dejavu/DejaVuSerif.ttf"
F_SERIF_B = "dejavu/DejaVuSerif-Bold.ttf"
F_SANS    = "liberation/LiberationSans-Regular.ttf"
F_SANS_B  = "liberation/LiberationSans-Bold.ttf"
F_MONO    = "liberation/LiberationMono-Regular.ttf"

# ---------- numpy helpers ----------
yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
nx = xx / W
ny = yy / H

def to_img(arr): return Image.fromarray((np.clip(arr,0,1)*255).astype(np.uint8), "RGB")

def vgrad(stops):
    pos=[s[0] for s in stops]; cols=np.array([s[1] for s in stops])
    out=np.empty((H,W,3),np.float32); col=ny[:,0]
    for c in range(3): out[:,:,c]=np.interp(col,pos,cols[:,c])[:,None]
    return out

def screen(b,l): return 1-(1-b)*(1-l)

def blob(cx,cy,rx,ry,color,strength=1.0,power=2.0):
    d=((xx-cx*W)/(rx*W))**2+((yy-cy*H)/(ry*H))**2
    a=np.exp(-(d**(power/2.0))*3.0)*strength
    return color[None,None,:]*a[:,:,None]

def grain(amount=0.012):
    n=np.random.normal(0,amount,(H,W,1)).astype(np.float32)
    return np.repeat(n,3,axis=2)

def hsv2rgb(h,s,v):
    h=(h%1.0)*6.0; i=np.floor(h).astype(int); f=h-i
    p=v*(1-s); q=v*(1-f*s); t=v*(1-(1-f)*s); i=i%6
    r=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[v,q,p,p,t,v])
    g=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[t,v,v,q,p,p])
    b=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[p,p,t,v,v,q])
    return np.stack([r,g,b],axis=-1)

def iridescent(strength, mode, period=0.85, sweep=True):
    """holographic 'unicorn' oil-slick sheen, subtle."""
    diag=(nx*math.cos(0.7)+ny*math.sin(0.7))
    hue=(diag/period + 0.12*np.sin(nx*7.0) + 0.10*np.cos(ny*6.0))
    rgb=hsv2rgb(hue, 0.55 if mode=='dark' else 0.40, 1.0).astype(np.float32)
    amp=np.ones((H,W),np.float32)
    if sweep:
        band=np.exp(-((diag-0.62)**2)/(2*0.22**2))
        amp=0.45+0.55*band
    return rgb*(amp[:,:,None]*strength)

def legibility(arr, mode):
    top=np.clip(1-ny/0.075,0,1)**1.5
    bot=np.clip(1-(1-ny)/0.085,0,1)**1.5
    scrim=(top+bot)[:,:,None]
    return arr*(1-scrim*(0.30 if mode=='light' else 0.38))

def vignette(arr, strength=0.2):
    d=((nx-0.5)**2+(ny-0.5)**2)
    return arr*(1-np.clip(d*2.1,0,1)*strength)[:,:,None]

def sparkles(n, mode, col):
    """rare twinkles like scattered gems."""
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    rng=np.random.default_rng(SEED_INT)
    cc=(int(col[0]*255),int(col[1]*255),int(col[2]*255))
    for _ in range(n):
        x=rng.uniform(0.05,0.95)*W; y=rng.uniform(0.10,0.62)*H
        s=rng.uniform(5,16); a=int(rng.uniform(60,150))
        d.line([x-s,y,x+s,y],fill=cc+(a,),width=1)
        d.line([x,y-s,x,y+s],fill=cc+(a,),width=1)
        d.line([x-s*0.5,y-s*0.5,x+s*0.5,y+s*0.5],fill=cc+(a//2,),width=1)
        d.line([x-s*0.5,y+s*0.5,x+s*0.5,y-s*0.5],fill=cc+(a//2,),width=1)
    return ov

# ---------- guilloche engraving ----------
def guilloche(cx,cy,scale,color,alpha,rings=7):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    cc=(int(color[0]*255),int(color[1]*255),int(color[2]*255))
    px,py=cx*W,cy*H
    # hypotrochoid rosette family (R, r, d)
    specs=[(205,44,120),(205,44,158),(188,40,132),(220,52,150),(170,36,110),
           (235,55,168),(160,33,100)]
    for k,(R,r,dd) in enumerate(specs[:rings]):
        g=math.gcd(R,r); turns=r//g
        t=np.linspace(0,2*math.pi*turns,turns*420)
        ratio=(R-r)/r
        x=px+scale*((R-r)*np.cos(t)+dd*np.cos(ratio*t))
        y=py+scale*((R-r)*np.sin(t)-dd*np.sin(ratio*t))
        pts=list(map(tuple,np.stack([x,y],axis=1)))
        d.line(pts,fill=cc+(int(alpha*255),),width=1)
    return ov

# ---------- wax-seal monogram ----------
def monogram_seal(cx,cy,scale,ink,accent,hero=False):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=(int(ink[0]*255),int(ink[1]*255),int(ink[2]*255))
    ac=(int(accent[0]*255),int(accent[1]*255),int(accent[2]*255))
    px,py=int(cx*W),int(cy*H)
    R=int(150*scale)
    # double ring with scalloped seal edge
    d.ellipse([px-R,py-R,px+R,py+R],outline=ac+(240,),width=max(2,int(3*scale)))
    R2=int(R*1.16)
    n=72
    for i in range(n):
        a=i/n*2*math.pi; long=(i%6==0)
        r0=R2; r1=R2+int((22 if long else 12)*scale)
        d.line([px+r0*math.cos(a),py+r0*math.sin(a),
                px+r1*math.cos(a),py+r1*math.sin(a)],
               fill=ac+(180 if long else 90,),width=max(1,int(1.6*scale)))
    d.ellipse([px-R2,py-R2,px+R2,py+R2],outline=ic+(70,),width=max(1,int(1*scale)))
    # initial monogram, serif, with subtle inner ring laurel dots
    fm=font(F_SERIF_B,int(190*scale))
    bw=d.textlength(INITIAL,font=fm); asc,desc=fm.getmetrics()
    d.text((px-bw/2,py-(asc+desc)/2-int(6*scale)),INITIAL,font=fm,fill=ac+(255,))
    return ov

# ---------- the ONE OF ONE mark ----------
def mark(cx,cy,ink,accent,scale=1.0,big_name=False):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=(int(ink[0]*255),int(ink[1]*255),int(ink[2]*255))
    ac=(int(accent[0]*255),int(accent[1]*255),int(accent[2]*255))
    px,py=int(cx*W),int(cy*H)
    fw=font(F_SANS_B,int(30*scale))
    draw_text_spaced(d,(px,py),"B N B H U B S",fw,ic+(225,),tracking=int(8*scale))
    # flanked ONE OF ONE
    fe=font(F_MONO,int(19*scale))
    label=f"{EDITION}"
    lw=draw_text_spaced(d,(px,py+int(36*scale)),label,fe,ac+(220,),tracking=int(6*scale))
    ry=py+int(36*scale)+int(9*scale)
    d.line([px-lw/2-int(40*scale),ry,px-lw/2-int(14*scale),ry],fill=ac+(160,),width=1)
    d.line([px+lw/2+int(14*scale),ry,px+lw/2+int(40*scale),ry],fill=ac+(160,),width=1)
    fo=font(F_SANS,int(16*scale))
    draw_text_spaced(d,(px,py+int(66*scale)),"FOR "+OWNER,fo,ic+(150,),tracking=int(3*scale))
    ff=font(F_MONO,int(12*scale))
    draw_text_spaced(d,(px,py+int(90*scale)),FINGERPRINT,ff,ac+(120,),tracking=int(2*scale))
    return ov

def draw_text_spaced(draw,xy,text,fnt,fill,tracking=0,anchor_center=True):
    widths=[draw.textlength(ch,font=fnt) for ch in text]
    total=sum(widths)+tracking*(len(text)-1)
    x=xy[0]-total/2 if anchor_center else xy[0]
    asc,desc=fnt.getmetrics(); y=xy[1]-asc/2 if anchor_center else xy[1]
    for ch,w in zip(text,widths):
        draw.text((x,y),ch,font=fnt,fill=fill); x+=w+tracking
    return total

def comp(arr,ov,blur=0):
    if blur: ov=ov.filter(ImageFilter.GaussianBlur(blur))
    base=to_img(arr).convert("RGBA"); base.alpha_composite(ov)
    return np.asarray(base.convert("RGB")).astype(np.float32)/255

# =====================================================================
# SKIN 1 — RED SEA HORIZON
# =====================================================================
def skin_horizon(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY),(0.32,TEAL_D*0.7),(0.55,TEAL_D),(0.70,GOLD*0.55),
                   (0.80,GOLD_B*0.9),(0.86,GOLD*0.5),(1.0,NAVY*1.6)])
        sun_col,sky_glow,ink,acc=GOLD_B,TEAL,IVORY,GOLD_B
    else:
        arr=vgrad([(0.0,np.array([0.95,0.93,0.88])),(0.35,SAND*1.05),
                   (0.58,np.array([0.97,0.85,0.66])),(0.74,GOLD_B),(0.82,GOLD*0.95),
                   (1.0,np.array([0.88,0.80,0.66]))])
        sun_col,sky_glow=np.array([1,1,0.96]),TEAL*0.5+SAND*0.5
        ink,acc=np.array([0.20,0.16,0.10]),np.array([0.60,0.42,0.12])
    sun_y=0.80
    arr=screen(arr,blob(0.5,sun_y,0.55,0.16,sky_glow,0.5,1.6))
    arr=screen(arr,blob(0.5,sun_y,0.16,0.075,sun_col,0.95,1.8))
    line=np.exp(-((ny-sun_y)**2)/(2*0.0009**2))
    arr=screen(arr,sun_col[None,None,:]*line[:,:,None]*(0.6 if mode=='dark' else 0.4))
    for k in range(1,6):
        yk=sun_y+0.03*k
        sh=np.exp(-((ny-yk)**2)/(2*0.0016**2))*(0.18/k)*(0.6+0.4*np.sin(nx*40+k))
        arr=screen(arr,sun_col[None,None,:]*sh[:,:,None])
    return finalize(arr,mode,ink,acc,irid=0.05,spark=(mode=='dark'))

# =====================================================================
# SKIN 2 — MARINA DEPTHS (guilloche-grade contours)
# =====================================================================
def skin_depths(mode):
    if mode=="dark":
        base=vgrad([(0.0,NAVY*1.3),(0.5,TEAL_D*0.85),(1.0,NAVY)])
        linecol,ink,acc,lstr=GOLD_B,IVORY,GOLD_B,0.9
    else:
        base=vgrad([(0.0,np.array([0.93,0.95,0.94])),(0.5,np.array([0.86,0.90,0.89])),(1.0,SAND*1.0)])
        linecol,ink,acc,lstr=TEAL_D*0.85,np.array([0.16,0.20,0.20]),np.array([0.55,0.40,0.12]),0.95
    field=np.zeros((H,W),np.float32)
    for cx,cy,r,w in [(0.30,0.40,0.34,1.0),(0.72,0.66,0.40,0.9),(0.55,0.18,0.26,0.6),(0.18,0.85,0.30,0.7)]:
        field+=w*np.exp(-(((nx-cx)**2+((ny-cy)*0.92)**2)/(2*r*r)))
    field+=0.10*np.sin(nx*6.0)+0.10*np.cos(ny*5.0)
    field=(field-field.min())/(field.max()-field.min())
    N=26; fN=field*N; dist=np.abs(fN-np.round(fN))
    grad=np.abs(np.gradient(field)[0])+np.abs(np.gradient(field)[1])+1e-4
    width=0.10/(grad*N+0.6)
    lines=np.clip(1-dist/np.clip(width,0.02,0.5),0,1)**1.4
    arr=base.copy(); a=(lines*lstr)[:,:,None]
    if mode=="dark":
        arr=screen(arr,linecol[None,None,:]*a)
    else:
        arr=arr*(1-a)+arr*linecol[None,None,:]*a
        gl=(np.round(fN)%4==0).astype(np.float32)*lines*0.5; ag=gl[:,:,None]
        arr=arr*(1-ag)+arr*acc[None,None,:]*1.4*ag
    arr=screen(arr,blob(0.30,0.40,0.22,0.20,acc,0.18 if mode=='dark' else 0.10,1.6))
    return finalize(arr,mode,ink,acc,irid=0.05,spark=(mode=='dark'))

# =====================================================================
# SKIN 3 — GOUNA DUNES
# =====================================================================
def skin_dunes(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY*1.2),(1.0,TEAL_D*0.6)])
        layers=[(0.42,GOLD*0.30,0.045,3.0,0.0),(0.55,TEAL_D*1.1,0.05,2.3,1.1),
                (0.66,GOLD*0.45,0.04,2.8,2.0),(0.77,TEAL*0.5,0.05,1.9,0.4),
                (0.88,GOLD_B*0.8,0.035,3.4,3.0)]
        ink,acc,hl=IVORY,GOLD_B,GOLD_B
    else:
        arr=vgrad([(0.0,CREAM),(1.0,SAND*1.0)])
        layers=[(0.42,np.array([0.92,0.88,0.80]),0.045,3.0,0.0),(0.55,np.array([0.85,0.90,0.86]),0.05,2.3,1.1),
                (0.66,GOLD_B*0.85,0.04,2.8,2.0),(0.77,np.array([0.80,0.86,0.84]),0.05,1.9,0.4),
                (0.88,GOLD*0.9,0.035,3.4,3.0)]
        ink,acc,hl=np.array([0.20,0.16,0.10]),np.array([0.60,0.42,0.12]),np.array([1,1,0.95])
    xrow=nx[0]
    for base_y,col,amp,freq,ph in layers:
        curve=base_y+amp*np.sin(xrow*freq*math.pi*2+ph)+amp*0.4*np.sin(xrow*freq*4.3*math.pi+ph*1.7)
        mask=np.clip((ny-curve[None,:])/0.010,0,1)
        shade=0.75+0.25*np.clip((ny-curve[None,:])/0.12,0,1)
        m=mask[:,:,None]; arr=arr*(1-m)+(col[None,None,:]*shade[:,:,None])*m
        crest=np.clip(1-np.abs(ny-curve[None,:])/0.004,0,1)**2
        arr=screen(arr,hl[None,None,:]*crest[:,:,None]*(0.5 if mode=='dark' else 0.3))
    return finalize(arr,mode,ink,acc,irid=0.045,spark=(mode=='dark'))

# =====================================================================
# SKIN 4 — UNICORN AURORA (full holographic iridescence)
# =====================================================================
def skin_aurora(mode):
    if mode=="dark":
        pts=[(0.18,0.14,TEAL_D*1.1,0.42),(0.85,0.20,GOLD*0.8,0.40),(0.50,0.45,TEAL*0.9,0.5),
             (0.15,0.72,CORAL*0.7,0.38),(0.88,0.80,GOLD_B*0.9,0.42),(0.5,0.97,NAVY,0.5),(0.5,0.02,NAVY,0.4)]
        bg,ink,acc=NAVY,IVORY,GOLD_B; irid=0.18
    else:
        pts=[(0.18,0.14,np.array([0.80,0.92,0.90]),0.42),(0.85,0.20,GOLD_B,0.40),
             (0.50,0.45,np.array([0.86,0.94,0.92]),0.5),(0.15,0.72,np.array([0.97,0.86,0.80]),0.40),
             (0.88,0.80,SAND*1.05,0.42),(0.5,0.97,CREAM,0.5),(0.5,0.02,CREAM,0.45)]
        bg,ink,acc=CREAM,np.array([0.20,0.18,0.14]),np.array([0.58,0.42,0.14]); irid=0.11
    wsum=np.zeros((H,W),np.float32); acc_c=np.zeros((H,W,3),np.float32)
    for cx,cy,col,r in pts:
        w=np.exp(-(((nx-cx)**2+(ny-cy)**2)/(2*r*r))); wsum+=w; acc_c+=col[None,None,:]*w[:,:,None]
    arr=acc_c/(wsum[:,:,None]+1e-5); arr=0.85*arr+0.15*bg[None,None,:]
    arr=np.asarray(to_img(arr).filter(ImageFilter.GaussianBlur(40))).astype(np.float32)/255
    return finalize(arr,mode,ink,acc,irid=irid,spark=True)

# =====================================================================
# SKIN 5 — ONE OF ONE  (guilloche certificate, hero)
# =====================================================================
def skin_signature(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY*1.4),(0.45,TEAL_D*0.7),(0.5,TEAL_D*0.78),(0.55,TEAL_D*0.7),(1.0,NAVY*1.1)])
        ink,acc,ray=IVORY,GOLD_B,GOLD
    else:
        arr=vgrad([(0.0,CREAM),(0.5,np.array([0.92,0.94,0.92])),(1.0,SAND*1.0)])
        ink,acc,ray=np.array([0.15,0.18,0.18]),np.array([0.55,0.40,0.12]),GOLD*0.7
    cx,cy=0.5,0.42
    ang=np.arctan2((yy-cy*H),(xx-cx*W)); rad=np.sqrt(((xx-cx*W)/W)**2+((yy-cy*H)/H)**2)
    rays=(0.5+0.5*np.sin(ang*36))**3; falloff=np.clip(1-rad/0.42,0,1)**1.5
    arr=screen(arr,ray[None,None,:]*(rays*falloff)[:,:,None]*(0.20 if mode=='dark' else 0.11))
    arr=screen(arr,blob(cx,cy,0.34,0.30,acc,0.20 if mode=='dark' else 0.10,1.8))
    # guilloche rosette engraving behind seal
    arr=comp(arr,guilloche(cx,cy,0.92,acc,0.16 if mode=='dark' else 0.20),blur=0)
    arr=comp(arr,monogram_seal(cx,cy,1.05,ink,acc,hero=True))
    # hero typography below seal
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=(int(ink[0]*255),int(ink[1]*255),int(ink[2]*255)); ac=(int(acc[0]*255),int(acc[1]*255),int(acc[2]*255))
    px=int(cx*W); base_y=int((cy+0.135)*H)
    fname=font(F_SERIF_B,int(74)); draw_text_spaced(d,(px,base_y),OWNER,fname,ic+(255,),tracking=14)
    fe=font(F_MONO,int(24)); lw=draw_text_spaced(d,(px,base_y+58),EDITION,fe,ac+(235,),tracking=10)
    ry=base_y+58+12
    d.line([px-lw/2-54,ry,px-lw/2-18,ry],fill=ac+(170,),width=1)
    d.line([px+lw/2+18,ry,px+lw/2+54,ry],fill=ac+(170,),width=1)
    fb=font(F_SANS_B,int(20)); draw_text_spaced(d,(px,base_y+104),"B N B H U B S  ·  P R I V A T E",fb,ic+(170,),tracking=5)
    ff=font(F_MONO,int(16)); draw_text_spaced(d,(px,base_y+138),"FINGERPRINT  "+FINGERPRINT,ff,ac+(150,),tracking=2)
    draw_text_spaced(d,(px,base_y+162),"MINTED  "+MINTED+"  ·  EL GOUNA · RED SEA",font(F_SANS,14),ic+(110,),tracking=2)
    arr=comp(arr,ov)
    arr=vignette(arr,0.2 if mode=='dark' else 0.12)
    arr=arr+iridescent(0.08 if mode=='dark' else 0.05,mode)
    arr=np.asarray(to_img(arr).convert("RGBA"))  # ensure clip
    arr=np.clip(arr.astype(np.float32)/255,0,1)[:,:,:3]
    arr=comp(arr,sparkles(26,mode,acc))
    arr=legibility(arr,mode)
    return to_img(arr)

# ---------- shared finalize ----------
def finalize(arr,mode,ink,acc,irid=0.05,spark=False):
    arr=arr+iridescent(irid,mode)
    arr=vignette(arr,0.20 if mode=='dark' else 0.12)
    arr=arr+grain(0.010)
    arr=comp(arr,mark(0.5,0.135,ink,acc,1.05))
    if spark:
        arr=comp(arr,sparkles(22,mode,acc))
    arr=legibility(arr,mode)
    return to_img(arr)

SKINS=[("01-red-sea-horizon",skin_horizon),("02-marina-depths",skin_depths),
       ("03-gouna-dunes",skin_dunes),("04-unicorn-aurora",skin_aurora),
       ("05-one-of-one",skin_signature)]

if __name__=="__main__":
    np.random.seed(7)
    for name,fn in SKINS:
        for mode in ("dark","light"):
            img=fn(mode); p=os.path.join(OUT,f"bnbhubs-fold7-{name}-{mode}.png")
            img.save(p,"PNG"); print("saved",p,img.size)
    print("DONE", "FP", FINGERPRINT)
