"""パドルとボールの描き込み版（3倍で描いて縮小し、輪郭をなめらかにする）"""
from PIL import Image, ImageDraw, ImageFilter, ImageChops
import math

def _vgrad(w, h, c1, c2):
    g = Image.new('RGB', (w, h)); d = ImageDraw.Draw(g)
    for y in range(h):
        t = y / max(1, h - 1)
        d.line([(0, y), (w, y)], fill=tuple(int(c1[i] + (c2[i] - c1[i]) * t) for i in range(3)))
    return g

def paddle(width=220, face=(255, 214, 120), face2=(250, 190, 80), rim=(14, 52, 82), grip=(14, 52, 82), accent=(255, 107, 74), angle=-30):
    S = 3; w, h = 600, 1120
    im = Image.new('RGBA', (w, h), (0, 0, 0, 0))
    # 面のかたち
    fmask = Image.new('L', (w, h), 0); ImageDraw.Draw(fmask).rounded_rectangle((36, 36, 564, 720), radius=170, fill=255)
    facel = _vgrad(w, h, (255, 228, 150), face2).convert('RGBA')
    # 表面の細かい斜線（カーボン調）
    tex = Image.new('RGBA', (w, h), (0, 0, 0, 0)); td = ImageDraw.Draw(tex)
    for k in range(-h, w + h, 18):
        td.line([(k, 0), (k + h, h)], fill=(255, 255, 255, 22), width=3)
    facel = Image.alpha_composite(facel, tex)
    # デザインの帯とエンブレム
    band = Image.new('RGBA', (w, h), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
    bd.polygon([(36, 470), (564, 360), (564, 450), (36, 560)], fill=accent + (255,))
    bd.polygon([(36, 580), (564, 470), (564, 492), (36, 602)], fill=(255, 255, 255, 230))
    facel = Image.alpha_composite(facel, band)
    # 光の反射
    shine = Image.new('RGBA', (w, h), (0, 0, 0, 0)); sd = ImageDraw.Draw(shine)
    sd.ellipse((70, 60, 330, 330), fill=(255, 255, 255, 90))
    shine = shine.filter(ImageFilter.GaussianBlur(40))
    facel = Image.alpha_composite(facel, shine)
    im.paste(facel, (0, 0), fmask)
    # ふち（エッジガード）
    ImageDraw.Draw(im).rounded_rectangle((36, 36, 564, 720), radius=170, outline=rim + (255,), width=34)
    d = ImageDraw.Draw(im)
    # 首（面とグリップのつなぎ）
    d.polygon([(220, 700), (380, 700), (350, 780), (250, 780)], fill=rim + (255,))
    # グリップ（巻きテープ）
    gmask = Image.new('L', (w, h), 0); ImageDraw.Draw(gmask).rounded_rectangle((238, 760, 362, 1080), radius=40, fill=255)
    gl = Image.new('RGBA', (w, h), grip + (255,)); gd = ImageDraw.Draw(gl)
    for k in range(700, 1120, 46):
        gd.polygon([(220, k), (380, k - 40), (380, k - 22), (220, k + 18)], fill=(255, 255, 255, 120))
    im.paste(gl, (0, 0), gmask)
    d.rounded_rectangle((226, 1040, 374, 1100), radius=28, fill=accent + (255,))
    # 縮小・回転・影
    sw = width; sh = int(h * width / w)
    im = im.resize((sw, sh), Image.LANCZOS).rotate(angle, expand=True, resample=Image.BICUBIC)
    shadow = Image.new('RGBA', im.size, (0, 0, 0, 0))
    shadow.putalpha(im.getchannel('A').point(lambda a: int(a * 0.35)))
    shadow = shadow.filter(ImageFilter.GaussianBlur(10))
    out = Image.new('RGBA', (im.width + 30, im.height + 30), (0, 0, 0, 0))
    out.paste(shadow, (18, 22), shadow); out.paste(im, (0, 0), im)
    return out

def ball(r=44, base=(255, 222, 80)):
    S = 4; R = r * S; size = R * 2 + 8
    im = Image.new('RGBA', (size, size), (0, 0, 0, 0))
    cx = cy = size / 2
    # 立体感（左上が明るく、右下が暗い）
    g = Image.new('RGBA', (size, size), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
    for i in range(R, 0, -2):
        t = i / R
        col = tuple(int(base[k] * (0.82 + 0.18 * (1 - t)) + (255 - base[k]) * 0.35 * (1 - t) ** 2) for k in range(3))
        ox, oy = -R * 0.28 * (1 - t), -R * 0.28 * (1 - t)
        gd.ellipse((cx + ox - i, cy + oy - i, cx + ox + i, cy + oy + i), fill=col + (255,))
    mask = Image.new('L', (size, size), 0); ImageDraw.Draw(mask).ellipse((cx - R, cy - R, cx + R, cy + R), fill=255)
    im.paste(g, (0, 0), mask)
    d = ImageDraw.Draw(im)
    # 穴（球の表面に並ぶように、ふちほど細く）
    holes = [(0, 0)] + [(0.5, a) for a in range(0, 360, 72)] + [(0.84, a + 36) for a in range(0, 360, 72)]
    for rad, ang in holes:
        a = math.radians(ang)
        px, py = cx + R * rad * math.cos(a), cy + R * rad * math.sin(a)
        hr = R * 0.13 * (1 - 0.3 * rad)
        sq = math.sqrt(max(0.3, 1 - rad ** 2))
        # 球のふちほど、中心に向かって押しつぶされた楕円になる
        hole = Image.new('RGBA', (int(hr * 4), int(hr * 4)), (0, 0, 0, 0)); hd = ImageDraw.Draw(hole)
        c0 = hr * 2
        hd.ellipse((c0 - hr * sq, c0 - hr, c0 + hr * sq, c0 + hr), fill=(222, 170, 45, 255))
        hd.ellipse((c0 - hr * sq * .6, c0 - hr * .45, c0 + hr * sq * .6, c0 + hr * .75), fill=(196, 140, 30, 255))
        hole = hole.rotate(-ang, resample=Image.BICUBIC)
        im.alpha_composite(hole, (int(px - c0), int(py - c0)))
    d = ImageDraw.Draw(im)
    # 光
    sh = Image.new('RGBA', (size, size), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((cx - R * .62, cy - R * .7, cx - R * .1, cy - R * .25), fill=(255, 255, 255, 140))
    sh = sh.filter(ImageFilter.GaussianBlur(R * 0.08))
    im = Image.alpha_composite(im, sh)
    im.putalpha(ImageChops.multiply(im.getchannel('A'), mask))
    ImageDraw.Draw(im).ellipse((cx - R, cy - R, cx + R, cy + R), outline=(215, 160, 40, 255), width=S * 2)
    return im.resize((size // S, size // S), Image.LANCZOS)

def place_ball(im, x, y, r, glow=True):
    if glow:
        g = Image.new('RGBA', im.size, (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
        gd.ellipse((x - r * 2.2, y - r * 2.2, x + r * 2.2, y + r * 2.2), fill=(255, 230, 140, 80))
        g = g.filter(ImageFilter.GaussianBlur(r * 0.8)); im.paste(g, (0, 0), g)
    b = ball(r); im.paste(b, (int(x - b.width / 2), int(y - b.height / 2)), b)
