#!/usr/bin/env python3
"""BNBHubs 'ONE OF ONE' wallpapers — Galaxy Z Fold 7, BOTH screens.
Inner/unfolded: 1968x2184  ·  Cover/folded: 1080x2520.
5 skins x dark+light x 2 screens. Size-aware so proportions stay correct."""
import os, math, hashlib, numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

OUT = "/tmp/wp"; os.makedirs(OUT, exist_ok=True)

# ---------- identity ----------
OWNER="MUHAMMAD"; INITIAL="M"; EDITION="ONE OF ONE"
_h=hashlib.sha256(f"{OWNER}·BNBHUBS·ONE-OF-ONE·RED-SEA".encode()).hexdigest().upper()
FINGERPRINT=f"{_h[0:4]}·{_h[4:8]}·{_h[8:12]}·{_h[12:16]}"
SEED_INT=int(_h[:8],16); MINTED="MMXXVI"

# ---------- palette ----------
NAVY=np.array([6,11,16])/255; TEAL=np.array([15,181,174])/255; TEAL_D=np.array([8,70,74])/255
GOLD=np.array([232,176,75])/255; GOLD_B=np.array([244,205,110])/255; CORAL=np.array([232,122,96])/255
IVORY=np.array([244,236,221])/255; SAND=np.array([225,207,173])/255; CREAM=np.array([243,244,242])/255

FD="/usr/share/fonts/truetype"
def font(p,s): return ImageFont.truetype(os.path.join(FD,p),max(12,int(s)))
F_SERIF_B="dejavu/DejaVuSerif-Bold.ttf"; F_SANS="liberation/LiberationSans-Regular.ttf"
F_SANS_B="liberation/LiberationSans-Bold.ttf"; F_MONO="liberation/LiberationMono-Regular.ttf"

# ---------- canvas globals (set per screen) ----------
W=H=0; xx=yy=nx=ny=None; S=1.0
def set_canvas(w,h):
    global W,H,xx,yy,nx,ny,S
    W,H=w,h; yy,xx=np.mgrid[0:H,0:W].astype(np.float32); nx=xx/W; ny=yy/H
    S=W/1968.0  # scale factor for absolute-pixel elements

# ---------- helpers ----------
def to_img(a): return Image.fromarray((np.clip(a,0,1)*255).astype(np.uint8),"RGB")
def vgrad(stops):
    pos=[s[0] for s in stops]; cols=np.array([s[1] for s in stops])
    out=np.empty((H,W,3),np.float32); col=ny[:,0]
    for c in range(3): out[:,:,c]=np.interp(col,pos,cols[:,c])[:,None]
    return out
def screen(b,l): return 1-(1-b)*(1-l)
def blob(cx,cy,rx,ry,color,strength=1.0,power=2.0):
    d=((xx-cx*W)/(rx*W))**2+((yy-cy*H)/(ry*H))**2
    return color[None,None,:]*(np.exp(-(d**(power/2.0))*3.0)*strength)[:,:,None]
def grain(a=0.012):
    n=np.random.normal(0,a,(H,W,1)).astype(np.float32); return np.repeat(n,3,axis=2)
def hsv2rgb(h,s,v):
    h=(h%1.0)*6.0; i=np.floor(h).astype(int); f=h-i
    p=v*(1-s); q=v*(1-f*s); t=v*(1-(1-f)*s); i=i%6
    r=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[v,q,p,p,t,v])
    g=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[t,v,v,q,p,p])
    b=np.select([i==0,i==1,i==2,i==3,i==4,i==5],[p,p,t,v,v,q])
    return np.stack([r,g,b],axis=-1)
def iridescent(strength,mode,period=0.85):
    diag=(nx*math.cos(0.7)+ny*math.sin(0.7))
    hue=(diag/period+0.12*np.sin(nx*7.0)+0.10*np.cos(ny*6.0))
    rgb=hsv2rgb(hue,0.55 if mode=='dark' else 0.40,1.0).astype(np.float32)
    band=np.exp(-((diag-0.62)**2)/(2*0.22**2)); amp=0.45+0.55*band
    return rgb*(amp[:,:,None]*strength)
def legibility(arr,mode):
    top=np.clip(1-ny/0.075,0,1)**1.5; bot=np.clip(1-(1-ny)/0.085,0,1)**1.5
    return arr*(1-(top+bot)[:,:,None]*(0.30 if mode=='light' else 0.38))
def vignette(arr,strength=0.2):
    d=((nx-0.5)**2+(ny-0.5)**2); return arr*(1-np.clip(d*2.1,0,1)*strength)[:,:,None]
def sparkles(n,mode,col):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); rng=np.random.default_rng(SEED_INT)
    cc=(int(col[0]*255),int(col[1]*255),int(col[2]*255))
    for _ in range(n):
        x=rng.uniform(0.05,0.95)*W; y=rng.uniform(0.10,0.62)*H; s=rng.uniform(5,16)*S; a=int(rng.uniform(60,150))
        d.line([x-s,y,x+s,y],fill=cc+(a,),width=1); d.line([x,y-s,x,y+s],fill=cc+(a,),width=1)
        d.line([x-s*0.5,y-s*0.5,x+s*0.5,y+s*0.5],fill=cc+(a//2,),width=1)
        d.line([x-s*0.5,y+s*0.5,x+s*0.5,y-s*0.5],fill=cc+(a//2,),width=1)
    return ov
def guilloche(cx,cy,scale,color,alpha,rings=7):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    cc=(int(color[0]*255),int(color[1]*255),int(color[2]*255)); px,py=cx*W,cy*H
    specs=[(205,44,120),(205,44,158),(188,40,132),(220,52,150),(170,36,110),(235,55,168),(160,33,100)]
    sc=scale*S
    for (R,r,dd) in specs[:rings]:
        g=math.gcd(R,r); turns=r//g; t=np.linspace(0,2*math.pi*turns,turns*420); ratio=(R-r)/r
        x=px+sc*((R-r)*np.cos(t)+dd*np.cos(ratio*t)); y=py+sc*((R-r)*np.sin(t)-dd*np.sin(ratio*t))
        d.line(list(map(tuple,np.stack([x,y],axis=1))),fill=cc+(int(alpha*255),),width=1)
    return ov
def draw_text_spaced(draw,xy,text,fnt,fill,tracking=0,center=True):
    widths=[draw.textlength(ch,font=fnt) for ch in text]; total=sum(widths)+tracking*(len(text)-1)
    x=xy[0]-total/2 if center else xy[0]; asc,_=fnt.getmetrics(); y=xy[1]-asc/2 if center else xy[1]
    for ch,w in zip(text,widths): draw.text((x,y),ch,font=fnt,fill=fill); x+=w+tracking
    return total
def monogram_seal(cx,cy,scale,ink,accent):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=tuple(int(c*255) for c in ink); ac=tuple(int(c*255) for c in accent)
    px,py=int(cx*W),int(cy*H); sc=scale*S; R=int(150*sc)
    d.ellipse([px-R,py-R,px+R,py+R],outline=ac+(240,),width=max(2,int(3*sc)))
    R2=int(R*1.16); n=72
    for i in range(n):
        a=i/n*2*math.pi; lng=(i%6==0); r0=R2; r1=R2+int((22 if lng else 12)*sc)
        d.line([px+r0*math.cos(a),py+r0*math.sin(a),px+r1*math.cos(a),py+r1*math.sin(a)],
               fill=ac+(180 if lng else 90,),width=max(1,int(1.6*sc)))
    d.ellipse([px-R2,py-R2,px+R2,py+R2],outline=ic+(70,),width=max(1,int(1*sc)))
    fm=font(F_SERIF_B,190*sc); bw=d.textlength(INITIAL,font=fm); asc,desc=fm.getmetrics()
    d.text((px-bw/2,py-(asc+desc)/2-int(6*sc)),INITIAL,font=fm,fill=ac+(255,))
    return ov
def mark(cx,cy,ink,accent,scale=1.0):
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=tuple(int(c*255) for c in ink); ac=tuple(int(c*255) for c in accent)
    px,py=int(cx*W),int(cy*H); sc=scale*max(S,0.72)
    draw_text_spaced(d,(px,py),"B N B H U B S",font(F_SANS_B,30*sc),ic+(240,),tracking=int(8*sc))
    lw=draw_text_spaced(d,(px,py+int(38*sc)),EDITION,font(F_MONO,20*sc),ac+(240,),tracking=int(6*sc))
    ry=py+int(38*sc)+int(10*sc)
    d.line([px-lw/2-int(40*sc),ry,px-lw/2-int(14*sc),ry],fill=ac+(190,),width=max(1,int(1.3*sc)))
    d.line([px+lw/2+int(14*sc),ry,px+lw/2+int(40*sc),ry],fill=ac+(190,),width=max(1,int(1.3*sc)))
    draw_text_spaced(d,(px,py+int(70*sc)),"FOR "+OWNER,font(F_SANS,17*sc),ic+(215,),tracking=int(3*sc))
    draw_text_spaced(d,(px,py+int(96*sc)),FINGERPRINT,font(F_MONO,15*sc),ac+(200,),tracking=int(2*sc))
    return ov
def comp(arr,ov,blur=0):
    if blur: ov=ov.filter(ImageFilter.GaussianBlur(blur))
    base=to_img(arr).convert("RGBA"); base.alpha_composite(ov)
    return np.asarray(base.convert("RGB")).astype(np.float32)/255

def shadow_comp(arr,ov,mode,alpha=0.7,blur=None):
    """Composite a text overlay with a soft contrast halo behind it (dark halo
    in dark mode, light halo in light mode) — boosts legibility, keeps tone."""
    if blur is None: blur=max(4,int(7*S))
    base=to_img(arr).convert("RGBA"); a=ov.split()[3]
    val=0 if mode=='dark' else 255
    sh_a=a.point(lambda v:int(v*alpha))
    chan=Image.new("L",(W,H),val)
    shadow=Image.merge("RGBA",(chan,chan,chan,sh_a)).filter(ImageFilter.GaussianBlur(blur))
    base.alpha_composite(shadow); base.alpha_composite(shadow); base.alpha_composite(ov)
    return np.asarray(base.convert("RGB")).astype(np.float32)/255

def finalize(arr,mode,ink,acc,irid=0.05,spark=False,markpos=0.135):
    arr=arr+iridescent(irid,mode); arr=vignette(arr,0.20 if mode=='dark' else 0.12); arr=arr+grain(0.010)
    arr=shadow_comp(arr,mark(0.5,markpos,ink,acc,1.05),mode,alpha=0.6)
    if spark: arr=comp(arr,sparkles(int(22*max(S,0.6)),mode,acc))
    arr=legibility(arr,mode); return to_img(arr)

# ---------- skins ----------
def skin_horizon(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY),(0.32,TEAL_D*0.7),(0.55,TEAL_D),(0.70,GOLD*0.55),(0.80,GOLD_B*0.9),(0.86,GOLD*0.5),(1.0,NAVY*1.6)])
        sun_col,sky=GOLD_B,TEAL; ink,acc=IVORY,GOLD_B
    else:
        arr=vgrad([(0.0,np.array([0.95,0.93,0.88])),(0.35,SAND*1.05),(0.58,np.array([0.97,0.85,0.66])),(0.74,GOLD_B),(0.82,GOLD*0.95),(1.0,np.array([0.88,0.80,0.66]))])
        sun_col,sky=np.array([1,1,0.96]),TEAL*0.5+SAND*0.5; ink,acc=np.array([0.20,0.16,0.10]),np.array([0.60,0.42,0.12])
    sy=0.80
    arr=screen(arr,blob(0.5,sy,0.55,0.16,sky,0.5,1.6)); arr=screen(arr,blob(0.5,sy,0.16,0.075,sun_col,0.95,1.8))
    line=np.exp(-((ny-sy)**2)/(2*0.0009**2)); arr=screen(arr,sun_col[None,None,:]*line[:,:,None]*(0.6 if mode=='dark' else 0.4))
    for k in range(1,6):
        yk=sy+0.03*k; sh=np.exp(-((ny-yk)**2)/(2*0.0016**2))*(0.18/k)*(0.6+0.4*np.sin(nx*40+k))
        arr=screen(arr,sun_col[None,None,:]*sh[:,:,None])
    return finalize(arr,mode,ink,acc,0.05,mode=='dark')

def skin_depths(mode):
    if mode=="dark":
        base=vgrad([(0.0,NAVY*1.3),(0.5,TEAL_D*0.85),(1.0,NAVY)]); linecol,ink,acc,lstr=GOLD_B,IVORY,GOLD_B,0.9
    else:
        base=vgrad([(0.0,np.array([0.93,0.95,0.94])),(0.5,np.array([0.86,0.90,0.89])),(1.0,SAND*1.0)])
        linecol,ink,acc,lstr=TEAL_D*0.85,np.array([0.16,0.20,0.20]),np.array([0.55,0.40,0.12]),0.95
    field=np.zeros((H,W),np.float32)
    for cx,cy,r,w in [(0.30,0.40,0.34,1.0),(0.72,0.66,0.40,0.9),(0.55,0.18,0.26,0.6),(0.18,0.85,0.30,0.7)]:
        field+=w*np.exp(-(((nx-cx)**2+((ny-cy)*0.92)**2)/(2*r*r)))
    field+=0.10*np.sin(nx*6.0)+0.10*np.cos(ny*5.0); field=(field-field.min())/(field.max()-field.min())
    N=26; fN=field*N; dist=np.abs(fN-np.round(fN))
    grad=np.abs(np.gradient(field)[0])+np.abs(np.gradient(field)[1])+1e-4; width=0.10/(grad*N+0.6)
    lines=np.clip(1-dist/np.clip(width,0.02,0.5),0,1)**1.4; arr=base.copy(); a=(lines*lstr)[:,:,None]
    if mode=="dark": arr=screen(arr,linecol[None,None,:]*a)
    else:
        arr=arr*(1-a)+arr*linecol[None,None,:]*a
        gl=(np.round(fN)%4==0).astype(np.float32)*lines*0.5; ag=gl[:,:,None]; arr=arr*(1-ag)+arr*acc[None,None,:]*1.4*ag
    arr=screen(arr,blob(0.30,0.40,0.22,0.20,acc,0.18 if mode=='dark' else 0.10,1.6))
    return finalize(arr,mode,ink,acc,0.05,mode=='dark')

def skin_dunes(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY*1.2),(1.0,TEAL_D*0.6)])
        layers=[(0.42,GOLD*0.30,0.045,3.0,0.0),(0.55,TEAL_D*1.1,0.05,2.3,1.1),(0.66,GOLD*0.45,0.04,2.8,2.0),(0.77,TEAL*0.5,0.05,1.9,0.4),(0.88,GOLD_B*0.8,0.035,3.4,3.0)]
        ink,acc,hl=IVORY,GOLD_B,GOLD_B
    else:
        arr=vgrad([(0.0,CREAM),(1.0,SAND*1.0)])
        layers=[(0.42,np.array([0.92,0.88,0.80]),0.045,3.0,0.0),(0.55,np.array([0.85,0.90,0.86]),0.05,2.3,1.1),(0.66,GOLD_B*0.85,0.04,2.8,2.0),(0.77,np.array([0.80,0.86,0.84]),0.05,1.9,0.4),(0.88,GOLD*0.9,0.035,3.4,3.0)]
        ink,acc,hl=np.array([0.20,0.16,0.10]),np.array([0.60,0.42,0.12]),np.array([1,1,0.95])
    xr=nx[0]
    for by,col,amp,freq,ph in layers:
        curve=by+amp*np.sin(xr*freq*math.pi*2+ph)+amp*0.4*np.sin(xr*freq*4.3*math.pi+ph*1.7)
        mask=np.clip((ny-curve[None,:])/0.010,0,1); shade=0.75+0.25*np.clip((ny-curve[None,:])/0.12,0,1)
        m=mask[:,:,None]; arr=arr*(1-m)+(col[None,None,:]*shade[:,:,None])*m
        crest=np.clip(1-np.abs(ny-curve[None,:])/0.004,0,1)**2; arr=screen(arr,hl[None,None,:]*crest[:,:,None]*(0.5 if mode=='dark' else 0.3))
    return finalize(arr,mode,ink,acc,0.045,mode=='dark')

def skin_aurora(mode):
    if mode=="dark":
        pts=[(0.18,0.14,TEAL_D*1.1,0.42),(0.85,0.20,GOLD*0.8,0.40),(0.50,0.45,TEAL*0.9,0.5),(0.15,0.72,CORAL*0.7,0.38),(0.88,0.80,GOLD_B*0.9,0.42),(0.5,0.97,NAVY,0.5),(0.5,0.02,NAVY,0.4)]
        bg,ink,acc,irid=NAVY,IVORY,GOLD_B,0.18
    else:
        pts=[(0.18,0.14,np.array([0.80,0.92,0.90]),0.42),(0.85,0.20,GOLD_B,0.40),(0.50,0.45,np.array([0.86,0.94,0.92]),0.5),(0.15,0.72,np.array([0.97,0.86,0.80]),0.40),(0.88,0.80,SAND*1.05,0.42),(0.5,0.97,CREAM,0.5),(0.5,0.02,CREAM,0.45)]
        bg,ink,acc,irid=CREAM,np.array([0.20,0.18,0.14]),np.array([0.58,0.42,0.14]),0.11
    wsum=np.zeros((H,W),np.float32); accc=np.zeros((H,W,3),np.float32)
    for cx,cy,col,r in pts:
        w=np.exp(-(((nx-cx)**2+(ny-cy)**2)/(2*r*r))); wsum+=w; accc+=col[None,None,:]*w[:,:,None]
    arr=accc/(wsum[:,:,None]+1e-5); arr=0.85*arr+0.15*bg[None,None,:]
    arr=np.asarray(to_img(arr).filter(ImageFilter.GaussianBlur(max(8,int(40*S))))).astype(np.float32)/255
    return finalize(arr,mode,ink,acc,irid,True)

def skin_signature(mode):
    if mode=="dark":
        arr=vgrad([(0.0,NAVY*1.4),(0.45,TEAL_D*0.7),(0.5,TEAL_D*0.78),(0.55,TEAL_D*0.7),(1.0,NAVY*1.1)]); ink,acc,ray=IVORY,GOLD_B,GOLD
    else:
        arr=vgrad([(0.0,CREAM),(0.5,np.array([0.92,0.94,0.92])),(1.0,SAND*1.0)]); ink,acc,ray=np.array([0.15,0.18,0.18]),np.array([0.55,0.40,0.12]),GOLD*0.7
    cx,cy=0.5,0.42
    ang=np.arctan2((yy-cy*H),(xx-cx*W)); rad=np.sqrt(((xx-cx*W)/W)**2+((yy-cy*H)/H)**2)
    rays=(0.5+0.5*np.sin(ang*36))**3; fall=np.clip(1-rad/0.42,0,1)**1.5
    arr=screen(arr,ray[None,None,:]*(rays*fall)[:,:,None]*(0.20 if mode=='dark' else 0.11))
    arr=screen(arr,blob(cx,cy,0.34,0.30,acc,0.20 if mode=='dark' else 0.10,1.8))
    arr=comp(arr,guilloche(cx,cy,0.92,acc,0.16 if mode=='dark' else 0.20))
    arr=comp(arr,monogram_seal(cx,cy,1.05,ink,acc))
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ic=tuple(int(c*255) for c in ink); ac=tuple(int(c*255) for c in acc)
    px=int(cx*W); by=int((cy+0.135)*H); sc=max(S,0.72)
    draw_text_spaced(d,(px,by),OWNER,font(F_SERIF_B,74*sc),ic+(255,),tracking=int(14*sc))
    lw=draw_text_spaced(d,(px,by+int(60*sc)),EDITION,font(F_MONO,24*sc),ac+(250,),tracking=int(10*sc))
    ry=by+int(60*sc)+int(13*sc)
    d.line([px-lw/2-int(54*sc),ry,px-lw/2-int(18*sc),ry],fill=ac+(210,),width=max(1,int(1.4*sc)))
    d.line([px+lw/2+int(18*sc),ry,px+lw/2+int(54*sc),ry],fill=ac+(210,),width=max(1,int(1.4*sc)))
    draw_text_spaced(d,(px,by+int(108*sc)),"B N B H U B S  ·  P R I V A T E",font(F_SANS_B,20*sc),ic+(225,),tracking=int(5*sc))
    draw_text_spaced(d,(px,by+int(144*sc)),"FINGERPRINT  "+FINGERPRINT,font(F_MONO,17*sc),ac+(210,),tracking=int(2*sc))
    draw_text_spaced(d,(px,by+int(170*sc)),"MINTED  "+MINTED+"  ·  EL GOUNA · RED SEA",font(F_SANS,15*sc),ic+(185,),tracking=int(2*sc))
    arr=shadow_comp(arr,ov,mode); arr=vignette(arr,0.2 if mode=='dark' else 0.12)
    arr=arr+iridescent(0.08 if mode=='dark' else 0.05,mode)
    arr=np.clip(arr,0,1); arr=comp(arr,sparkles(int(26*max(S,0.6)),mode,acc)); arr=legibility(arr,mode)
    return to_img(arr)

# ===== NEW ultra-premium skins =====
def skin_obsidian(mode):  # matte black + blueprint grid + rising gold arc-sun
    if mode=="dark":
        arr=vgrad([(0.0,np.array([3,5,8])/255),(0.55,NAVY*1.25),(1.0,TEAL_D*0.5)])
        ink,acc,arcc=IVORY,GOLD_B,GOLD_B; gline=70
    else:
        arr=vgrad([(0.0,np.array([0.96,0.96,0.95])),(0.5,np.array([0.93,0.91,0.86])),(1.0,SAND*1.0)])
        ink,acc,arcc=np.array([0.15,0.16,0.17]),np.array([0.5,0.36,0.10]),np.array([0.50,0.36,0.10]); gline=40
    cx,cy=0.5,0.80
    arr=screen(arr,blob(cx,cy,0.55,0.22,acc,0.16 if mode=='dark' else 0.12,1.6))
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    ac=tuple(int(c*255) for c in arcc); ic=tuple(int(c*255) for c in ink)
    g=int(W/12)
    for x in range(0,W,g): d.line([x,0,x,H],fill=ic+(gline//5,),width=1)
    for y in range(0,H,g): d.line([0,y,W,y],fill=ic+(gline//5,),width=1)
    pxx,pyy=cx*W,cy*H
    abase=118 if mode=='dark' else 150
    for i in range(48):
        r=int((0.03+0.0215*i)*H); a=int(max(10,abase-i*2.2))
        d.ellipse([pxx-r,pyy-r,pxx+r,pyy+r],outline=ac+(a,),width=max(1,int(1.6*S)))
    arr=comp(arr,ov)
    return finalize(arr,mode,ink,acc,0.05,mode=='dark')

def skin_silk(mode):  # flowing silk ribbons with specular sheen
    warp=np.sin(nx*math.pi*3.0+np.sin(ny*math.pi*2.0)*1.3)
    field=ny*5.0+warp*0.7+0.4*np.sin(nx*math.pi*1.5)
    t=0.5+0.5*np.sin(field*math.pi*2.0)
    if mode=="dark":
        c0,c1,bs=TEAL_D*0.85,GOLD*0.9,NAVY; ink,acc,irid,spc=IVORY,GOLD_B,0.08,0.35
    else:
        c0,c1,bs=np.array([0.86,0.90,0.88]),GOLD_B,CREAM; ink,acc,irid,spc=np.array([0.18,0.17,0.13]),np.array([0.55,0.40,0.12]),0.05,0.2
    arr=c0[None,None,:]*(1-t[:,:,None])+c1[None,None,:]*t[:,:,None]
    arr=screen(arr,np.ones(3)[None,None,:]*(t**6)[:,:,None]*spc)
    arr=arr*(0.8+0.2*ny)[:,:,None]; arr=0.9*arr+0.1*bs[None,None,:]
    arr=np.asarray(to_img(arr).filter(ImageFilter.GaussianBlur(max(2,int(3*S))))).astype(np.float32)/255
    return finalize(arr,mode,ink,acc,irid,mode=='dark')

def skin_glass(mode):  # glassmorphism frosted panels
    if mode=="dark":
        base=vgrad([(0.0,NAVY*1.3),(0.45,TEAL_D*0.9),(0.7,np.array([0.10,0.30,0.34])),(1.0,NAVY*1.1)])
        base=screen(base,blob(0.2,0.25,0.4,0.3,TEAL,0.25,1.6)); base=screen(base,blob(0.85,0.7,0.4,0.3,GOLD,0.22,1.6)); base=screen(base,blob(0.7,0.12,0.3,0.2,CORAL,0.16,1.6))
        ink,acc=IVORY,GOLD_B; fill=(255,255,255,30); bord=(255,255,255,150)
    else:
        base=vgrad([(0.0,CREAM),(0.5,np.array([0.88,0.92,0.91])),(1.0,SAND*1.02)])
        base=screen(base,blob(0.2,0.25,0.4,0.3,TEAL*0.4,0.18,1.6)); base=screen(base,blob(0.85,0.7,0.4,0.3,GOLD_B,0.18,1.6))
        ink,acc=np.array([0.16,0.18,0.18]),np.array([0.55,0.40,0.12]); fill=(255,255,255,75); bord=(255,255,255,180)
    img=to_img(base).convert("RGBA"); blurred=img.filter(ImageFilter.GaussianBlur(max(10,int(28*S))))
    for x0,y0,x1,y1,rad in [(0.16,0.30,0.84,0.60,0.06),(0.30,0.55,0.70,0.78,0.05)]:
        bx=(int(x0*W),int(y0*H),int(x1*W),int(y1*H)); rr=int(rad*W)
        mask=Image.new("L",(W,H),0); ImageDraw.Draw(mask).rounded_rectangle(bx,radius=rr,fill=255)
        img.paste(blurred,(0,0),mask)
        ov=Image.new("RGBA",(W,H),(0,0,0,0)); od=ImageDraw.Draw(ov)
        od.rounded_rectangle(bx,radius=rr,fill=fill); od.rounded_rectangle(bx,radius=rr,outline=bord,width=max(1,int(2*S)))
        img.alpha_composite(ov)
    arr=np.asarray(img.convert("RGB")).astype(np.float32)/255
    return finalize(arr,mode,ink,acc,0.06,False)

def skin_arabesque(mode):  # fine gold Islamic star geometry
    if mode=="dark":
        arr=vgrad([(0.0,NAVY*1.3),(0.5,TEAL_D*0.9),(1.0,NAVY*1.1)]); linec,ink,acc=GOLD_B,IVORY,GOLD_B; la=130
    else:
        arr=vgrad([(0.0,CREAM),(0.5,np.array([0.90,0.92,0.90])),(1.0,SAND*1.0)]); linec,ink,acc=GOLD*0.62,np.array([0.16,0.18,0.18]),np.array([0.55,0.40,0.12]); la=180
    arr=screen(arr,blob(0.5,0.42,0.42,0.42,acc,0.16 if mode=='dark' else 0.09,1.6))
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov); lc=tuple(int(c*255) for c in linec)
    def star8(cxp,cyp,ro,ri,rot=0):
        p=[]
        for k in range(8):
            p.append((cxp+ro*math.cos(rot+k*2*math.pi/8),cyp+ro*math.sin(rot+k*2*math.pi/8)))
            p.append((cxp+ri*math.cos(rot+(k+0.5)*2*math.pi/8),cyp+ri*math.sin(rot+(k+0.5)*2*math.pi/8)))
        return p
    def octo(cxp,cyp,r,rot=0): return [(cxp+r*math.cos(rot+k*2*math.pi/8),cyp+r*math.sin(rot+k*2*math.pi/8)) for k in range(8)]
    g=int(W/7); Ro=g*0.60; Ri=Ro*0.40; wdt=max(1,int(1.5*S))
    nodes=[]
    for gy in range(-1,int(H/g)+2):
        for gx in range(-1,int(W/g)+2):
            nodes.append((gx*g,gy*g)); nodes.append((gx*g+g/2,gy*g+g/2))  # main + offset lattice
    for cxp,cyp in nodes:
        dxn,dyn=cxp/W-0.5,cyp/H-0.5; fade=max(0.0,1-(dxn*dxn+dyn*dyn)*1.7); a=int(la*fade)
        if a<8: continue
        s=star8(cxp,cyp,Ro,Ri,math.pi/8); d.line(s+[s[0]],fill=lc+(a,),width=wdt)
        o=octo(cxp,cyp,Ri*0.92,math.pi/8); d.line(o+[o[0]],fill=lc+(int(a*0.55),),width=wdt)
    arr=comp(arr,ov)
    return finalize(arr,mode,ink,acc,0.05,mode=='dark')

def skin_nebula(mode):  # deep cosmos, starfield, M constellation
    if mode=="dark":
        arr=vgrad([(0.0,np.array([4,6,12])/255),(0.5,TEAL_D*0.6),(1.0,np.array([8,8,18])/255)])
        arr=screen(arr,blob(0.30,0.35,0.45,0.30,TEAL,0.30,1.6)); arr=screen(arr,blob(0.72,0.62,0.40,0.30,CORAL*0.8,0.22,1.6)); arr=screen(arr,blob(0.55,0.50,0.50,0.40,GOLD*0.6,0.16,1.6))
        ink,acc,stars=IVORY,GOLD_B,True
    else:
        arr=vgrad([(0.0,CREAM),(0.5,np.array([0.90,0.93,0.93])),(1.0,np.array([0.93,0.90,0.85]))])
        arr=screen(arr,blob(0.30,0.35,0.45,0.30,TEAL*0.3,0.15,1.6)); arr=screen(arr,blob(0.72,0.62,0.40,0.30,GOLD_B,0.16,1.6))
        ink,acc,stars=np.array([0.16,0.18,0.2]),np.array([0.55,0.40,0.12]),False
    arr=np.asarray(to_img(arr).filter(ImageFilter.GaussianBlur(max(6,int(24*S))))).astype(np.float32)/255
    ov=Image.new("RGBA",(W,H),(0,0,0,0)); d=ImageDraw.Draw(ov)
    if stars:
        rng=np.random.default_rng(SEED_INT+1)
        for _ in range(int(460*max(S,0.5))):
            x=rng.uniform(0,1)*W; y=rng.uniform(0,1)*H; b=rng.uniform(0.2,1.0); s=max(1,(2 if b>0.85 else 1)*S)
            col=(255,255,255) if rng.uniform(0,1)>0.25 else (244,205,110)
            d.ellipse([x-s,y-s,x+s,y+s],fill=col+(int(190*b),))
        Mp=[(0.40,0.33),(0.425,0.25),(0.46,0.30),(0.495,0.25),(0.52,0.33)]; Mp=[(px*W,py*H) for px,py in Mp]
        for i in range(len(Mp)-1): d.line([Mp[i],Mp[i+1]],fill=(244,205,110,95),width=max(1,int(1.2*S)))
        for x,y in Mp:
            r=3*S; d.ellipse([x-r,y-r,x+r,y+r],fill=(255,255,255,235))
    arr=comp(arr,ov)
    return finalize(arr,mode,ink,acc,0.07 if mode=='dark' else 0.04,False)

SKINS=[("01-red-sea-horizon",skin_horizon),("02-marina-depths",skin_depths),
       ("03-gouna-dunes",skin_dunes),("04-unicorn-aurora",skin_aurora),("05-one-of-one",skin_signature),
       ("06-obsidian-royale",skin_obsidian),("07-liquid-silk",skin_silk),
       ("08-spectral-glass",skin_glass),("09-arabesque-gold",skin_arabesque),
       ("10-velvet-nebula",skin_nebula)]
SCREENS=[("inner-unfolded",1968,2184),("cover-folded",1080,2520)]

if __name__=="__main__":
    for scr,w,h in SCREENS:
        d=os.path.join(OUT,scr); os.makedirs(d,exist_ok=True)
        for name,fn in SKINS:
            for mode in ("dark","light"):
                np.random.seed(7); set_canvas(w,h)
                fn(mode).save(os.path.join(d,f"bnbhubs-{scr}-{name}-{mode}.png"),"PNG")
        print("done",scr,w,"x",h)
    print("DONE","FP",FINGERPRINT)
