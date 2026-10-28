# 投稿11「強く打った方が負ける？」（ディンク）。横から見たコートとパドル（SVG → Chromiumで書き出し）
# python3 dink.py 出力先フォルダ [ページ番号...]
import os, sys, math
from playwright.sync_api import sync_playwright

OUT = sys.argv[1] if len(sys.argv) > 1 else "out"
PAGES = [int(a) for a in sys.argv[2:]] or list(range(1, 8))
os.makedirs(OUT, exist_ok=True)
W, H, N = 1080, 1350, 7
FONT = "'Noto Sans CJK JP'"

NAVY = '#0e3452'; SEA = '#1f7fb8'; CORAL = '#ff6b4a'; SUN = '#ffd678'; WHITE = '#ffffff'
BG = '#faf7f1'; GREY = '#78808a'; INK = '#0b2236'
SKIN = '#f3c9a6'; SKIN2 = '#dda57f'; HAIR = '#2f2523'
BALL = '#ffe03a'


def T(x, y, s, size, c, w=900, a='start', op=1, ls=0):
    return (f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="{w}" font-size="{size}" fill="{c}" '
            f'fill-opacity="{op}" text-anchor="{a}" letter-spacing="{ls}">{s}</text>')


def rich(x, y, segs, size, w=900):
    o = f'<text x="{x}" y="{y}" font-family="{FONT}" font-weight="{w}" font-size="{size}">'
    for s, c in segs: o += f'<tspan fill="{c}">{s}</tspan>'
    return o + '</text>'


def footer(page, c=NAVY):
    return T(70, H - 56, 'PICKLEBALL TOKYO', 26, c, 700) + T(W - 70, H - 56, f'{page}/{N}  @pickleballtokyo', 26, c, 500, 'end')


def tag(s, y, fill, c, x=70):
    w = len(s) * 36 + 52
    return f'<rect x="{x}" y="{y}" width="{w}" height="62" rx="31" fill="{fill}"/>' + T(x + 26, y + 44, s, 36, c, 700)


DEFS = f'''<defs>
<filter id="glow" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="9"/></filter>
<filter id="soft" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="5"/></filter>
<filter id="bokeh" x="-50%" y="-50%" width="200%" height="200%"><feGaussianBlur stdDeviation="14"/></filter>
<linearGradient id="arena" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#071a2b"/><stop offset="1" stop-color="#163f4c"/></linearGradient>
<linearGradient id="shirtC" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#ff7b5c"/><stop offset=".55" stop-color="#ff6b4a"/><stop offset="1" stop-color="#d9502f"/></linearGradient>
<linearGradient id="shirtB" x1="0" y1="0" x2="1" y2="0"><stop offset="0" stop-color="#3c97cf"/><stop offset=".55" stop-color="#1f7fb8"/><stop offset="1" stop-color="#16628f"/></linearGradient>
<linearGradient id="shirtVC" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#ff8466"/><stop offset="1" stop-color="#e5532f"/></linearGradient>
<linearGradient id="shirtVB" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#3f9ad2"/><stop offset="1" stop-color="#15608c"/></linearGradient>
<linearGradient id="padB" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#ff8a6c"/><stop offset="1" stop-color="#e2502f"/></linearGradient>
<linearGradient id="pad" x1="0" y1="0" x2="1" y2="1"><stop offset="0" stop-color="#1d4f78"/><stop offset="1" stop-color="#0a2740"/></linearGradient>
<radialGradient id="spot" cx=".5" cy=".55" r=".6"><stop offset="0" stop-color="#ffffff" stop-opacity=".22"/><stop offset="1" stop-color="#ffffff" stop-opacity="0"/></radialGradient>
<radialGradient id="ballg" cx=".38" cy=".32" r=".75"><stop offset="0" stop-color="#fff6a8"/><stop offset=".55" stop-color="{BALL}"/><stop offset="1" stop-color="#e2b400"/></radialGradient>
</defs>'''


# ---------- 中継カメラの投影（コートの後ろ、少し高い位置から） ----------
class Cam:
    """斜め上から見下ろすカメラ。boxの範囲にコートと2人が収まるように自動で合わせる"""
    def __init__(s, cam, target, box, fit=None):
        s.c = cam
        fw = [target[i] - cam[i] for i in range(3)]; n = math.sqrt(sum(v * v for v in fw)); s.fw = [v / n for v in fw]
        r = [s.fw[1], -s.fw[0], 0]; n = math.hypot(r[0], r[1]); s.rt = [r[0] / n, r[1] / n, 0]
        s.up = [s.rt[1] * s.fw[2] - s.rt[2] * s.fw[1], s.rt[2] * s.fw[0] - s.rt[0] * s.fw[2], s.rt[0] * s.fw[1] - s.rt[1] * s.fw[0]]
        s.f, s.cx, s.cy = 1.0, 0.0, 0.0
        pts = fit or [(x, y, 0) for x in (-10, 10) for y in (-22, 22)] + [(-3, -9, 6.2), (2.5, 9, 6.2)]
        q = [s.P(*p) for p in pts]
        xs, ys = [a for a, _ in q], [b for _, b in q]
        x0, y0, x1, y1 = box
        k = min((x1 - x0) / (max(xs) - min(xs)), (y1 - y0) / (max(ys) - min(ys)))
        s.f = k; s.cx = x0 + (x1 - x0) / 2 - k * (max(xs) + min(xs)) / 2; s.cy = y0 + (y1 - y0) / 2 - k * (max(ys) + min(ys)) / 2
        s.top = s.P(-90, 0, 0)[1]
    def _v(s, X, Y, Z):
        v = (X - s.c[0], Y - s.c[1], Z - s.c[2])
        return sum(v[i] * s.fw[i] for i in range(3)), sum(v[i] * s.rt[i] for i in range(3)), sum(v[i] * s.up[i] for i in range(3))
    def P(s, X, Y, Z=0):
        d, x, y = s._v(X, Y, Z)
        return s.cx + s.f * x / d, s.cy - s.f * y / d
    def kp(s, X, Y, Z=0): return s.f / s._v(X, Y, Z)[0]     # その場所での1フィートの大きさ
    def poly(s, pts, fill, extra=''):
        q = ' '.join('%.1f,%.1f' % s.P(*p) for p in pts)
        return f'<polygon points="{q}" fill="{fill}" {extra}/>'
    def line(s, a, b, c='white', w=5, extra=''):
        (x1, y1), (x2, y2) = s.P(*a), s.P(*b)
        return f'<line x1="{x1:.1f}" y1="{y1:.1f}" x2="{x2:.1f}" y2="{y2:.1f}" stroke="{c}" stroke-width="{w}" {extra}/>'


def court(c, hi_far=True, hi_near=False):
    n = -22
    o = f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#arena)"/>'
    # 奥の照明（ぼけた光）
    for x, y, r, a in ((140, c.top - 40, 46, .35), (380, c.top - 90, 34, .25), (720, c.top - 70, 40, .3),
                       (960, c.top - 30, 52, .35), (560, c.top - 150, 26, .2)):
        o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="#ffe9b0" fill-opacity="{a}" filter="url(#bokeh)"/>'
    # 奥の壁と床
    o += c.poly([(-90, -60, 0), (26, -60, 0), (26, 60, 0), (-90, 60, 0)], '#163f4c')
    o += c.poly([(-10, n, 0), (10, n, 0), (10, 22, 0), (-10, 22, 0)], '#2b78a8')
    o += c.poly([(-10, 0, 0), (10, 0, 0), (10, 7, 0), (-10, 7, 0)], '#f08a52' if hi_far else '#3f8bb8')
    o += c.poly([(-10, -7, 0), (10, -7, 0), (10, 0, 0), (-10, 0, 0)], '#f08a52' if hi_near else '#3f8bb8')
    # ライン
    for a, b in (((-10, n), (-10, 22)), ((10, n), (10, 22)), ((-10, 22), (10, 22)),
                 ((-10, 7), (10, 7)), ((-10, -7), (10, -7)), ((0, 7), (0, 22)), ((0, n), (0, -7))):
        o += c.line((*a, 0), (*b, 0), 'white', 4.5, 'stroke-opacity=".92"')
    o += f'<rect x="0" y="0" width="{W}" height="{H}" fill="url(#spot)"/>'
    return o


def net(c):
    o = c.poly([(-11, 0, 0), (11, 0, 0), (11, 0, 3), (0, 0, 2.83), (-11, 0, 3)], '#06192a', 'fill-opacity=".22"')
    for i in range(-21, 22):
        X = i / 2
        zt = 3 - 0.17 * (1 - abs(X) / 11)
        o += c.line((X, 0, 0), (X, 0, zt), '#0a2236', 1.6, 'stroke-opacity=".38"')
    for j in range(1, 6):
        z = j * 0.47
        o += c.line((-11, 0, z), (11, 0, z), '#0a2236', 1.6, 'stroke-opacity=".38"')
    (x1, y1), (xm, ym), (x2, y2) = c.P(-11, 0, 3), c.P(0, 0, 2.83), c.P(11, 0, 3)
    o += f'<path d="M{x1:.1f},{y1:.1f} Q{xm:.1f},{2*ym-(y1+y2)/2:.1f} {x2:.1f},{y2:.1f}" fill="none" stroke="white" stroke-width="8"/>'
    for X in (-11, 11):
        (a, b), (_, e) = c.P(X, 0, 0), c.P(X, 0, 3.15)
        o += f'<rect x="{a-5}" y="{e}" width="10" height="{b-e}" rx="4" fill="#d9e2ea"/>'
    return o


def ball(x, y, r):
    o = f'<circle cx="{x}" cy="{y}" r="{r*2.2}" fill="{BALL}" fill-opacity=".45" filter="url(#glow)"/>'
    o += f'<circle cx="{x}" cy="{y}" r="{r}" fill="url(#ballg)"/>'
    for k in range(6):
        a = math.radians(k * 60 + 20)
        o += f'<circle cx="{x+r*.55*math.cos(a):.1f}" cy="{y+r*.55*math.sin(a):.1f}" r="{r*.12:.1f}" fill="#c99a00" fill-opacity=".8"/>'
    return o + f'<circle cx="{x}" cy="{y}" r="{r*.12:.1f}" fill="#c99a00" fill-opacity=".8"/>'


def flight(c, p0, p1, p2, t1=1.0, n=60, col=BALL, w0=2, w1=24):
    """3Dの放物線を投影して、だんだん太く明るくなる光の帯にする"""
    pts = []
    for i in range(n + 1):
        t = t1 * i / n
        P = [(1 - t) ** 2 * p0[j] + 2 * (1 - t) * t * p1[j] + t * t * p2[j] for j in range(3)]
        pts.append((P, c.P(*P)))
    glow = core = ''
    for i in range(n):
        t = i / n
        (_, a), (_, b) = pts[i], pts[i + 1]
        w = w0 + (w1 - w0) * t
        glow += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="{col}" stroke-opacity="{.05+.5*t:.2f}" stroke-width="{w*2.4:.1f}" stroke-linecap="round"/>'
        core += f'<line x1="{a[0]:.1f}" y1="{a[1]:.1f}" x2="{b[0]:.1f}" y2="{b[1]:.1f}" stroke="#fffbe0" stroke-opacity="{.04+.9*t:.2f}" stroke-width="{w*.45:.1f}" stroke-linecap="round"/>'
    end3, end2 = pts[-1]
    return f'<g filter="url(#soft)">{glow}</g>' + core, end3, end2


def shadow(c, X, Y, size):
    x, y = c.P(X, Y, 0); k = c.kp(X, Y)
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{size*k:.1f}" ry="{size*k*.28:.1f}" fill="#00121f" fill-opacity=".35" filter="url(#soft)"/>'


# ---------- 人（後ろ姿：あなた） ----------
def L(pts, c, w, extra=''):
    d = 'M' + ' L'.join('%.1f,%.1f' % p for p in pts)
    return f'<path d="{d}" fill="none" stroke="{c}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round" {extra}/>'


def back_person(x, y, s, pose='dink'):
    """足元(x,y)、sは高さ440の絵に対する倍率"""
    o = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f},{s*.9:.3f})">'
    o += '<ellipse cx="0" cy="0" rx="130" ry="20" fill="#00121f" fill-opacity=".4" filter="url(#soft)"/>'
    for sgn in (-1, 1):                                  # 足
        hip, knee, ank = (38 * sgn, -205), (70 * sgn, -112), (78 * sgn, -30)
        o += L([hip, knee], SKIN, 46) + L([knee, ank], SKIN, 34)
        o += L([(knee[0] - 6 * sgn, knee[1] + 14), (ank[0] - 8 * sgn, ank[1] - 18)], SKIN2, 12, 'stroke-opacity=".7"')
        ax = ank[0]
        o += (f'<rect x="{ax-30}" y="-40" width="60" height="40" rx="17" fill="#f4f7fa" stroke="{NAVY}" stroke-width="3"/>'
              f'<rect x="{ax-30}" y="-12" width="60" height="12" rx="6" fill="#c3ccd4"/>'
              f'<rect x="{ax-6}" y="-38" width="12" height="18" rx="5" fill="{CORAL}"/>')
    # 短パン
    o += (f'<path d="M-72,-240 L72,-240 L90,-150 Q52,-138 12,-150 L0,-176 L-12,-150 Q-52,-138 -90,-150 Z" fill="{NAVY}"/>'
          f'<path d="M30,-238 L72,-240 L90,-150 Q70,-144 52,-145 Z" fill="#082238" fill-opacity=".55"/>')
    # 奥の腕（左手はバランス）
    o += L([(-84, -334), (-140, -276)], 'url(#shirtC)', 46) if False else ''
    o += L([(-110, -306), (-146, -268), (-160, -214)], SKIN, 26)
    o += L([(-84, -336), (-114, -302)], '#f0623f', 46)
    # 胴（ポロ）
    o += ('<path d="M-70,-226 Q-80,-292 -94,-338 Q-62,-366 0,-368 Q62,-366 94,-338 Q80,-292 70,-226 Q0,-212 -70,-226 Z" '
          'fill="url(#shirtC)"/>')
    o += '<path d="M-30,-364 Q-56,-330 -88,-322" fill="none" stroke="white" stroke-opacity=".85" stroke-width="5"/>'
    o += '<path d="M30,-364 Q56,-330 88,-322" fill="none" stroke="white" stroke-opacity=".85" stroke-width="5"/>'
    o += '<path d="M-6,-300 Q0,-260 -4,-226" fill="none" stroke="#c94a2b" stroke-opacity=".35" stroke-width="4"/>'
    # 首・襟・頭
    o += f'<rect x="-17" y="-392" width="34" height="34" rx="10" fill="{SKIN2}"/>'
    o += '<path d="M-32,-362 Q0,-376 32,-362 L30,-350 Q0,-360 -30,-350 Z" fill="white"/>'
    o += f'<ellipse cx="-39" cy="-414" rx="8" ry="12" fill="{SKIN2}"/><ellipse cx="39" cy="-414" rx="8" ry="12" fill="{SKIN2}"/>'
    o += f'<ellipse cx="0" cy="-418" rx="40" ry="46" fill="{HAIR}"/>'
    o += '<path d="M-26,-446 Q-6,-458 14,-450 M-30,-424 Q-8,-436 18,-428" fill="none" stroke="#4a3a36" stroke-width="4" stroke-linecap="round"/>'
    o += '<path d="M-40,-432 Q0,-448 40,-432" fill="none" stroke="white" stroke-width="11" stroke-linecap="round"/>'
    # 手前の腕とパドル
    if pose == 'smash':
        arm = [(84, -336), (138, -398), (168, -470)]; pad = (178, -540, -8)
    else:
        arm = [(84, -336), (150, -286), (206, -300)]; pad = (236, -350, 30)
    o += L([arm[0], ((arm[0][0] + arm[1][0]) / 2, (arm[0][1] + arm[1][1]) / 2)], '#ec5c3b', 46)
    o += L([((arm[0][0] * .4 + arm[1][0] * .6), (arm[0][1] * .4 + arm[1][1] * .6)), arm[1], arm[2]], SKIN, 25)
    px, py, rot = pad
    o += L([arm[2], (px, py + 40)], '#1b1b1b', 13)
    o += (f'<g transform="translate({px},{py}) rotate({rot})">'
          f'<rect x="-46" y="-58" width="92" height="104" rx="40" fill="url(#pad)" stroke="#3aa0d8" stroke-width="5"/>'
          f'<rect x="-34" y="-46" width="40" height="44" rx="20" fill="white" fill-opacity=".1"/></g>')
    o += f'<circle cx="{arm[2][0]}" cy="{arm[2][1]}" r="15" fill="{SKIN}"/>'
    return o + '</g>'


# ---------- 人（正面：相手） ----------
def front_person(x, y, s, pose='ready'):
    dy = 46 if pose == 'scoop' else 0
    o = f'<g transform="translate({x:.1f},{y:.1f}) scale({s:.3f},{s*.9:.3f})">'
    o += '<ellipse cx="0" cy="0" rx="120" ry="18" fill="#00121f" fill-opacity=".4" filter="url(#soft)"/>'
    for sgn in (-1, 1):
        hip, knee, ank = (36 * sgn, -205 + dy), ((70 + dy * .6) * sgn, -112 + dy * .4), (76 * sgn, -30)
        o += L([hip, knee], SKIN, 46) + L([knee, ank], SKIN, 34)
        ax = ank[0]
        o += (f'<path d="M{ax-30},-6 Q{ax-30},-40 {ax},-42 Q{ax+30},-40 {ax+30},-6 Z" fill="#f4f7fa" stroke="{NAVY}" stroke-width="3"/>'
              f'<rect x="{ax-31}" y="-10" width="62" height="10" rx="5" fill="#c3ccd4"/>')
    o += f'<path d="M-72,{-240+dy} L72,{-240+dy} L90,{-150+dy} Q52,{-138+dy} 12,{-150+dy} L0,{-176+dy} L-12,{-150+dy} Q-52,{-138+dy} -90,{-150+dy} Z" fill="{NAVY}"/>'
    lean = 'rotate(0)' if pose != 'scoop' else 'translate(0,46)'
    o += f'<g transform="{lean}">'
    o += ('<path d="M-70,-226 Q-80,-292 -94,-338 Q-62,-366 0,-368 Q62,-366 94,-338 Q80,-292 70,-226 Q0,-212 -70,-226 Z" fill="url(#shirtB)"/>')
    o += '<path d="M-22,-366 L0,-330 L22,-366 Z" fill="white"/><path d="M-30,-366 L-14,-344 L0,-366 M30,-366 L14,-344 L0,-366" fill="white"/>'
    o += f'<rect x="-17" y="-392" width="34" height="30" rx="10" fill="{SKIN2}"/>'
    o += f'<ellipse cx="-40" cy="-416" rx="8" ry="12" fill="{SKIN2}"/><ellipse cx="40" cy="-416" rx="8" ry="12" fill="{SKIN2}"/>'
    o += f'<ellipse cx="0" cy="-418" rx="40" ry="46" fill="{SKIN}"/>'
    o += f'<path d="M-41,-414 Q-44,-470 0,-466 Q44,-470 41,-414 Q30,-446 0,-444 Q-24,-446 -41,-414 Z" fill="{HAIR}"/>'
    o += f'<circle cx="-14" cy="-414" r="5" fill="{HAIR}"/><circle cx="14" cy="-414" r="5" fill="{HAIR}"/>'
    o += f'<circle cx="-24" cy="-398" r="7" fill="{CORAL}" fill-opacity=".3"/><circle cx="24" cy="-398" r="7" fill="{CORAL}" fill-opacity=".3"/>'
    o += f'<path d="M-11,-394 Q0,-384 11,-394" fill="none" stroke="{HAIR}" stroke-width="4" stroke-linecap="round"/>'
    if pose == 'scoop':
        o += L([(-84, -336), (-120, -280), (-104, -222)], SKIN, 25)
        arm = [(84, -336), (128, -268), (118, -196)]; pad = (100, -126, 170)
    else:
        o += L([(-84, -336), (-130, -280), (-96, -246)], SKIN, 25)
        arm = [(84, -336), (130, -280), (110, -250)]; pad = (60, -270, -20)
    o += L([(-84, -336), (-110, -300)], '#1a6fa3', 44)
    o += L(arm[1:], SKIN, 25) + L([arm[0], arm[1]], SKIN, 25) + L([arm[0], ((arm[0][0] + arm[1][0]) / 2, (arm[0][1] + arm[1][1]) / 2)], '#1a6fa3', 44)
    px, py, rot = pad
    o += (f'<g transform="translate({px},{py}) rotate({rot})">'
          f'<rect x="-44" y="-56" width="88" height="100" rx="38" fill="{CORAL}" stroke="#ffb199" stroke-width="5"/></g>')
    o += f'<circle cx="{arm[2][0]}" cy="{arm[2][1]}" r="15" fill="{SKIN}"/>'
    return o + '</g></g>'


def side_person(x, y, s, facing=1, pose='ready', team='C'):
    """横向きの人。足元(x,y)、高さ約480の絵をs倍。facing=1で右向き"""
    shirt = 'url(#shirtV%s)' % team
    dark = '#d9502f' if team == 'C' else '#16628f'
    padc, pade = ('url(#pad)', '#3aa0d8') if team == 'C' else (CORAL, '#ffb199')
    crouch = {'scoop': 46, 'smash': -6}.get(pose, 0)
    lean = {'scoop': 26, 'smash': -4}.get(pose, 12)
    hy = -238 + crouch
    def R(p):                                    # 上半身を腰の位置を中心に前へ倒す
        a = math.radians(lean); dx, dy = p[0], p[1] - hy
        return (dx * math.cos(a) - dy * math.sin(a), hy + dx * math.sin(a) + dy * math.cos(a))
    o = f'<g transform="translate({x:.1f},{y:.1f}) scale({s*facing:.3f},{s:.3f})">'
    o += '<ellipse cx="6" cy="0" rx="110" ry="16" fill="#00121f" fill-opacity=".38" filter="url(#soft)"/>'
    # 奥の腕
    if pose == 'smash': ba = [(-6, -150), (-40, -110), (-30, -70)]
    else: ba = [(-4, -150), (-16, -92), (12, -60)]
    o += L([R((10, -142 + 0)), R(ba[1]), R(ba[2])], SKIN2, 24) if False else ''
    sh = R((14, -150 + 0 - 0))
    o += L([R((4, hy - 150 - hy + hy)), ], SKIN2, 1) if False else ''
    def up(px, py): return R((px, hy + py))       # 腰からの相対位置（上半身）
    o += L([up(6, -148), up(*ba[1]), up(*ba[2])], SKIN2, 24)
    o += L([up(6, -150), up(0, -118)], dark, 40)
    # 足（奥 → 手前）
    kb, kf = (-44 - crouch * .4, hy + 104 - crouch * .5), (40 + crouch * .5, hy + 102 - crouch * .5)
    ab, af = (-58, -30), (34, -30)
    for hip, k, an, sk in (((-6, hy), kb, ab, SKIN2), ((8, hy), kf, af, SKIN)):
        o += L([hip, k], sk, 42) + L([k, an], sk, 30)
        ax = an[0]
        o += (f'<path d="M{ax-20},-4 Q{ax-24},-34 {ax-6},-36 L{ax+14},-34 Q{ax+46},-22 {ax+52},-8 L{ax+52},0 L{ax-20},0 Z" '
              f'fill="#f4f7fa" stroke="{NAVY}" stroke-width="3.5" stroke-linejoin="round"/>'
              f'<rect x="{ax-20}" y="-9" width="72" height="9" rx="4" fill="#c3ccd4"/>'
              f'<path d="M{ax+2},-28 L{ax+26},-14" stroke="{CORAL}" stroke-width="6" stroke-linecap="round"/>')
    # 短パン
    o += L([(-6, hy), ((-6 + kb[0]) * .5, (hy + kb[1]) * .5)], NAVY, 56) + L([(8, hy), ((8 + kf[0]) * .52, (hy + kf[1]) * .52)], NAVY, 56)
    o += f'<ellipse cx="2" cy="{hy-6}" rx="44" ry="26" fill="{NAVY}"/>'
    # 胴（ポロ）
    pts = [(-38, 6), (-30, -80), (-18, -150), (8, -166), (34, -160), (52, -112), (44, -40), (40, 8)]
    q = [up(*p) for p in pts]
    d = f'M{q[0][0]:.1f},{q[0][1]:.1f} C{q[1][0]:.1f},{q[1][1]:.1f} {q[2][0]:.1f},{q[2][1]:.1f} {q[3][0]:.1f},{q[3][1]:.1f} '
    d += f'Q{q[4][0]:.1f},{q[4][1]:.1f} {q[5][0]:.1f},{q[5][1]:.1f} Q{q[6][0]:.1f},{q[6][1]:.1f} {q[7][0]:.1f},{q[7][1]:.1f} Z'
    o += f'<path d="{d}" fill="{shirt}"/>'
    c1, c2 = up(-8, -150), up(30, -160)
    o += f'<path d="M{c1[0]:.1f},{c1[1]:.1f} Q{up(14,-138)[0]:.1f},{up(14,-138)[1]:.1f} {c2[0]:.1f},{c2[1]:.1f}" fill="none" stroke="white" stroke-width="7" stroke-linecap="round"/>'
    # 首と頭
    o += L([up(14, -160), up(20, -186)], SKIN, 28)
    hx, hy2 = up(30, -222)
    o += f'<circle cx="{hx:.1f}" cy="{hy2:.1f}" r="35" fill="{SKIN}"/>'
    o += f'<circle cx="{hx+33:.1f}" cy="{hy2+6:.1f}" r="7" fill="{SKIN}"/>'
    o += (f'<path d="M{hx+20},{hy2-28} A35,35 0 1 0 {hx-16},{hy2+31} Q{hx-4},{hy2+4} {hx+2},{hy2-12} '
          f'Q{hx+10},{hy2-22} {hx+20},{hy2-28} Z" fill="{HAIR}"/>')
    o += f'<path d="M{hx-30},{hy2-18} Q{hx},{hy2-34} {hx+32},{hy2-16}" fill="none" stroke="white" stroke-width="10" stroke-linecap="round"/>'
    o += f'<ellipse cx="{hx-4}" cy="{hy2+4}" rx="7" ry="10" fill="{SKIN2}"/>'
    o += f'<circle cx="{hx+20}" cy="{hy2-2}" r="4.2" fill="{HAIR}"/>'
    o += f'<circle cx="{hx+14}" cy="{hy2+12}" r="7" fill="{CORAL}" fill-opacity=".3"/>'
    o += f'<path d="M{hx+18},{hy2+18} Q{hx+25},{hy2+23} {hx+31},{hy2+16}" fill="none" stroke="{HAIR}" stroke-width="3.6" stroke-linecap="round"/>'
    # 手前の腕とパドル
    if pose == 'smash':
        arm = [(20, -150), (44, -214), (60, -282)]; pad = (66, -334, -6)
    elif pose == 'scoop':
        arm = [(20, -150), (52, -92), (88, -58)]; pad = (124, -36, 60)
    else:
        arm = [(20, -150), (56, -94), (104, -84)]; pad = (146, -98, 24)
    A = [up(*p) for p in arm]
    o += L([A[0], ((A[0][0] + A[1][0]) / 2, (A[0][1] + A[1][1]) / 2)], shirt, 42)
    o += L([((A[0][0] * .45 + A[1][0] * .55), (A[0][1] * .45 + A[1][1] * .55)), A[1], A[2]], SKIN, 24)
    P = up(pad[0], pad[1]); rot = pad[2] + lean
    o += L([A[2], P], '#1b1b1b', 12)
    o += (f'<g transform="translate({P[0]:.1f},{P[1]:.1f}) rotate({rot})">'
          f'<rect x="-22" y="-56" width="44" height="100" rx="20" fill="{padc}" stroke="{pade}" stroke-width="5"/></g>')
    o += f'<circle cx="{A[2][0]:.1f}" cy="{A[2][1]:.1f}" r="14" fill="{SKIN}"/>'
    return o + '</g>'


def paddle_pt(c, X, Y, facing, pose):
    """パドルの面の位置（3D）。だいたいの位置でよい"""
    Z = {'scoop': 1.0, 'smash': 6.5}.get(pose, 2.8)
    return (X, Y + facing * 0.6, Z + 0.6)


def paddle_at(c, X, Y, facing, pose, team):
    # 人の代わりにパドルだけを置く。高さはそのショットを打つ位置
    Z = {'scoop': 1.0, 'smash': 6.5}.get(pose, 2.8)
    x, y = c.P(X, Y, Z); gx, gy = c.P(X, Y, 0); k = c.kp(X, Y, Z)
    rot = {'scoop': 70, 'smash': -10}.get(pose, 28) * facing
    face, edge = ('url(#pad)', '#3aa0d8') if team == 'C' else ('url(#padB)', '#ffb199')
    s = k / 60
    o = f'<ellipse cx="{gx:.1f}" cy="{gy:.1f}" rx="{70*s:.1f}" ry="{14*s:.1f}" fill="#00121f" fill-opacity=".45" filter="url(#soft)"/>'
    o += f'<line x1="{gx:.1f}" y1="{gy:.1f}" x2="{x:.1f}" y2="{y:.1f}" stroke="white" stroke-opacity=".18" stroke-width="2" stroke-dasharray="0"/>' if False else ''
    o += f'<g transform="translate({x:.1f},{y:.1f}) rotate({rot}) scale({s:.3f})">'
    o += '<rect x="-14" y="40" width="28" height="78" rx="10" fill="#1d2228"/>'
    for i in range(5): o += f'<line x1="-12" y1="{50+i*14}" x2="12" y2="{58+i*14}" stroke="#3b444e" stroke-width="5"/>'
    o += '<rect x="-16" y="112" width="32" height="12" rx="6" fill="#2b323a"/>'
    o += f'<rect x="-62" y="-104" width="124" height="150" rx="56" fill="{face}" stroke="{edge}" stroke-width="7"/>'
    o += '<path d="M-40,-70 Q-36,-90 -12,-92" fill="none" stroke="white" stroke-opacity=".5" stroke-width="9" stroke-linecap="round"/>'
    return o + '</g>'


def person_at(c, X, Y, facing, pose, team):
    return paddle_at(c, X, Y, facing, pose, team)


def _old_person_at(c, X, Y, facing, pose, team):
    x, y = c.P(X, Y, 0); s = c.kp(X, Y) * 5.8 / 480
    return side_person(x, y, s, facing, pose, team)


def page(body, bg=BG):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}">{DEFS}'
            f'<rect width="{W}" height="{H}" fill="{bg}"/>{body}</svg>')


def panel(cid, x, y, w, h, r, inner):
    return (f'<clipPath id="{cid}"><rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{r}"/></clipPath>'
            f'<g clip-path="url(#{cid})">{inner}</g>')


# ================= スライド =================
CAM = (30.0, -6.0, 13.0); AIM = (0.0, 0.0, 1.6)        # コートの横、少し高いところから
YOU = (1.0, -9.0); OPP = (-1.0, 9.0)
FIT = [(x, y, 0) for x in (-1, 7) for y in (-10.6, 10.6)] + [(YOU[0], YOU[1], 6.4), (OPP[0], OPP[1], 6.4)]


def pill(x, y, s, fill, c=WHITE, size=30):
    w = len(s) * size + 40
    return (f'<rect x="{x-w/2:.0f}" y="{y-size-12:.0f}" width="{w}" height="{size+24}" rx="{(size+24)/2}" fill="{fill}"/>'
            + T(x, y + 2, s, size, c, 900, 'middle'))


def head_top(c, X, Y): return c.P(X, Y, 5.0)


def rally(c, opp_pose='ready', land=(-1.0, 3.2, 0), t1=1.0, bounce=None, you_pose='ready', p_top=6.0):
    sc = court(c) + net(c)
    sc += person_at(c, *OPP, -1, opp_pose, 'B')
    p0 = paddle_pt(c, *YOU, 1, you_pose)
    tr, e3, e2 = flight(c, p0, ((p0[0] + land[0]) / 2, -0.6, p_top), land, t1=t1)
    if bounce is None:
        tail = shadow(c, e3[0], e3[1], .45) + tr + ball(e2[0], e2[1], 22 * c.kp(*e3) / 40)
    else:
        lx, ly = c.P(*land)
        tail = tr + f'<ellipse cx="{lx:.1f}" cy="{ly:.1f}" rx="{c.kp(*land)*.8:.1f}" ry="{c.kp(*land)*.22:.1f}" fill="white" fill-opacity=".95"/>'
        tr2, e3, e2 = flight(c, land, *bounce, w0=20, w1=24)
        tail += shadow(c, e3[0], e3[1], .45) + tr2 + ball(e2[0], e2[1], 22 * c.kp(*e3) / 40)
    sc += person_at(c, *YOU, 1, you_pose, 'C') + tail
    return sc


def s1():
    c = Cam(CAM, AIM, (30, 640, 1050, 1230), FIT)
    sc = rally(c, t1=.62, p_top=7.2)
    sc += ('<linearGradient id="fade" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#061624" stop-opacity=".96"/>'
           '<stop offset=".36" stop-color="#061624" stop-opacity=".7"/><stop offset=".48" stop-color="#061624" stop-opacity="0"/></linearGradient>'
           f'<rect width="{W}" height="{H}" fill="url(#fade)"/>')
    sc += ('<linearGradient id="fade2" x1="0" y1="0" x2="0" y2="1"><stop offset=".9" stop-color="#061624" stop-opacity="0"/>'
           '<stop offset="1" stop-color="#061624" stop-opacity=".9"/></linearGradient>'
           f'<rect width="{W}" height="{H}" fill="url(#fade2)"/>')
    b = sc + tag('ちょっと戦術', 92, SUN, NAVY)
    b += T(70, 290, 'ピックルボールは、', 82, WHITE)
    b += rich(70, 400, [('強く打った方が', WHITE), ('負ける？', SUN)], 82)
    b += T(70, 480, 'ネット際で「ふわっ」と打ち合う理由', 42, WHITE, 500, op=.9)
    b += footer(1, WHITE)
    return page(b)


def s4():
    b = tag('ふわっと落とすと', 78, NAVY, WHITE)
    b += T(70, 262, '相手は、下から上へ', 88, NAVY)
    b += T(70, 375, '打つしかない', 88, NAVY)
    b += T(70, 460, 'キッチンに落ちた球は、ノーバウンドで打てない。', 38, GREY, 500)
    b += T(70, 512, '弾んだ低い球を、持ち上げて返すだけ。', 38, GREY, 500)
    c = Cam(CAM, AIM, (70, 690, 1010, 1150), FIT)
    land = (-0.6, 3.4, 0)
    hit = paddle_pt(c, *OPP, -1, 'scoop')
    sc = rally(c, 'scoop', land, bounce=(((land[0] + hit[0]) / 2, 5.2, 2.4), (hit[0], hit[1] - .5, hit[2] + .5)))
    kx, ky = c.P(0, 3.5, 0)
    sc += pill(kx, ky + 74, '相手のキッチン', '#e8763c', size=28)
    ox, oy = head_top(c, *OPP); yx, yy = head_top(c, *YOU)
    sc += pill(ox, oy - 12, '相手', CORAL) + pill(yx, yy - 12, 'あなた', SEA)
    ax, ay = c.P(OPP[0], OPP[1] - 2.6, 0)
    sc += (f'<line x1="{ax}" y1="{ay-30}" x2="{ax}" y2="{ay-150}" stroke="{SUN}" stroke-width="9" stroke-linecap="round"/>'
           f'<path d="M{ax-18},{ay-144} L{ax},{ay-172} L{ax+18},{ay-144} Z" fill="{SUN}" stroke="{SUN}" stroke-width="4" stroke-linejoin="round"/>')
    b += panel('p4', 40, 570, 1000, 660, 40, sc)
    b += footer(4)
    return page(b)



def head(tagtxt, l1, l2, sub=(), dark=False, size=88):
    c1 = WHITE if dark else NAVY
    b = tag(tagtxt, 78, SUN if dark else NAVY, NAVY if dark else WHITE)
    b += (rich(70, 262, l1, size) if isinstance(l1, list) else T(70, 262, l1, size, c1))
    if l2: b += (rich(70, 375, l2, size) if isinstance(l2, list) else T(70, 375, l2, size, c1))
    y = 460 if l2 else 350
    for i, t in enumerate(sub): b += T(70, y + i * 52, t, 38, '#c9d3dc' if dark else GREY, 500)
    return b


def ball_at(c, P3, r=22): return shadow(c, P3[0], P3[1], .45) + ball(*c.P(*P3), r * c.kp(*P3) / 40)


def mark(c, P3):
    x, y = c.P(*P3); k = c.kp(*P3)
    return f'<ellipse cx="{x:.1f}" cy="{y:.1f}" rx="{k*.8:.1f}" ry="{k*.22:.1f}" fill="white" fill-opacity=".95"/>'


def burst(x, y, r, col=CORAL):
    pts = []
    for i in range(16):
        a = math.pi * 2 * i / 16; rr = r if i % 2 == 0 else r * .45
        pts.append('%.1f,%.1f' % (x + rr * math.cos(a), y + rr * .55 * math.sin(a)))
    return f'<polygon points="{" ".join(pts)}" fill="{col}" fill-opacity=".9"/>'


FIT_HI = FIT + [(OPP[0], OPP[1], 9.5), (0, -1.5, 8.5)]


def smash_scene(c, label=True):
    """あなたの球が浮く → 相手が上からたたく"""
    sc = court(c, hi_far=False) + net(c)
    p0 = paddle_pt(c, *YOU, 1, 'ready'); top = paddle_pt(c, *OPP, -1, 'smash')
    tr, _, _ = flight(c, p0, (0, -1.5, 13.0), top, t1=1.0)
    hit = (YOU[0], -4.5, 0)
    tr2, _, _ = flight(c, top, (OPP[0], 2.0, 6.0), hit, col=CORAL, w0=8, w1=26)
    sc += paddle_at(c, *OPP, -1, 'smash', 'B') + paddle_at(c, *YOU, 1, 'ready', 'C') + tr + tr2
    bx, by = c.P(*hit)
    sc += burst(bx, by, c.kp(*hit) * 1.6) + ball(bx, by - c.kp(*hit) * .5, 22 * c.kp(*hit) / 40)
    return sc


def dink_scene(c, bounce=True):
    sc = court(c) + net(c)
    p0 = paddle_pt(c, *YOU, 1, 'ready'); land = (-0.6, 3.4, 0)
    tr, _, _ = flight(c, p0, ((p0[0] + land[0]) / 2, -0.6, 6.0), land)
    sc += paddle_at(c, *OPP, -1, 'ready', 'B') + paddle_at(c, *YOU, 1, 'ready', 'C') + tr + mark(c, land)
    tr2, e3, e2 = flight(c, land, (-0.7, 5.0, 2.0), (-0.8, 6.2, 1.6), w0=20, w1=24)
    sc += tr2 + ball(e2[0], e2[1], 22 * c.kp(*e3) / 40)
    return sc, land


def s2():
    b = head('答え', [('強さ', NAVY), ('より、', NAVY), ('低さ', CORAL)], None,
             ['ネットの手前に、ふわっと落とすのが強い。'])
    # 上：高く浮くと
    c = Cam(CAM, AIM, (70, 440, 1010, 800), FIT_HI)
    sc = smash_scene(c)
    b += panel('p2a', 40, 420, 1000, 400, 36, sc)
    b += pill(190, 482, '高く浮くと', CORAL, size=30)
    b += pill(880, 790, 'たたかれる', CORAL, size=30)
    c = Cam(CAM, AIM, (70, 900, 1010, 1210), FIT)
    sc, land = dink_scene(c)
    b += panel('p2b', 40, 846, 1000, 400, 36, sc)
    b += pill(190, 908, '低く落とすと', '#e8a400', NAVY, size=30)
    b += pill(880, 1216, '攻められない', '#e8a400', NAVY, size=30)
    b += footer(2)
    return page(b)


def s3():
    b = head('ディンクって？', 'ネットすれすれで、', [('相手の', NAVY), ('キッチン', '#e0702f'), ('に落とす', NAVY)],
             ['キッチンの線のそばから、軽く打つだけ。', '強く振らなくていいので、初心者でもできる。'])
    c = Cam(CAM, AIM, (70, 690, 1010, 1150), FIT)
    sc, land = dink_scene(c)
    tx, ty = c.P(0, -0.6, 5.6)
    sc += pill(tx, ty - 40, 'ネットすれすれ', SUN, NAVY, size=28)
    kx, ky = c.P(0, 3.5, 0)
    sc += pill(kx, ky + 74, '相手のキッチン', '#e8763c', size=28)
    yx, yy = head_top(c, *YOU); sc += pill(yx, yy - 30, 'あなた', SEA)
    b += panel('p3', 40, 570, 1000, 660, 40, sc)
    b += footer(3)
    return page(b)


def s5():
    b = head('だから始まる', '我慢くらべ', None,
             ['ポコン、ポコン…と、キッチンどうしで', '何往復も、ふわっとした打ち合いが続く。'])
    c = Cam(CAM, AIM, (70, 560, 1010, 1150), FIT)
    sc = court(c, True, True) + net(c)
    sc += paddle_at(c, *OPP, -1, 'scoop', 'B') + paddle_at(c, *YOU, 1, 'scoop', 'C')
    a = paddle_pt(c, *YOU, 1, 'scoop'); bb = paddle_pt(c, *OPP, -1, 'scoop')
    lands = [(-0.4, 3.0, 0), (0.6, -3.2, 0)]
    for (p0, l, q) in ((a, lands[0], bb), (bb, lands[1], a)):
        tr, _, _ = flight(c, p0, ((p0[0] + l[0]) / 2, (p0[1] + l[1]) / 2 * .3, 5.2), l, col=SUN, w0=4, w1=14)
        sc += tr + mark(c, l)
    e3 = (OPP[0], OPP[1] - 3.0, 1.6)
    sc += ball_at(c, e3)
    for (X, Y), t in (((0, -7.5), 'ポコン'), ((0, 7.5), 'ポコン')):
        x, y = c.P(X, Y, 6.2); sc += T(x, y, t, 44, SUN, 900, 'middle')
    b += panel('p5', 40, 470, 1000, 760, 40, sc)
    b += footer(5)
    return page(b)


def s6():
    b = head('勝負が決まるのは', '先に浮かせた方が、', [('たたかれる', CORAL)],
             ['我慢できずに浮いた球は、相手のチャンスボール。', 'ディンクは、浮いた球を引き出すための球。'])
    c = Cam(CAM, AIM, (70, 610, 1010, 1180), FIT_HI)
    sc = smash_scene(c)
    ox, oy = c.P(*paddle_pt(c, *OPP, -1, 'smash'))
    sc += pill(ox + 10, oy + 120, 'チャンス！', CORAL, size=30)
    yx, yy = head_top(c, *YOU); sc += pill(yx, yy - 30, 'あなた', SEA)
    b += panel('p6', 40, 570, 1000, 660, 40, sc)
    b += footer(6)
    return page(b)


def s7():
    b = f'<rect width="{W}" height="{H}" fill="{NAVY}"/>'
    b += tag('次のラリーで', 92, SUN, NAVY)
    b += T(70, 262, '1球だけ、', 88, WHITE)
    b += rich(70, 375, [('ふわっと', SUN), ('試してみて', WHITE)], 88)
    items = [('1', 'ネットの手前に、ふわっと落とす', '強く振らなくていい'),
             ('2', '浮いた球が来たら、チャンス', '上からたたける'),
             ('3', '先にしびれを切らさない', '我慢くらべに勝つ')]
    for i, (n, t, sub) in enumerate(items):
        y = 470 + i * 170
        b += f'<rect x="70" y="{y}" width="940" height="146" rx="30" fill="#163f63"/>'
        b += f'<circle cx="140" cy="{y+73}" r="38" fill="{SUN}"/>' + T(140, y + 88, n, 42, NAVY, 900, 'middle')
        b += T(204, y + 66, t, 42, WHITE, 900) + T(204, y + 116, sub, 32, '#b9c7d4', 500)
    b += f'<rect x="70" y="1000" width="940" height="160" rx="30" fill="white"/>'
    b += T(540, 1062, '保存して、次の練習で見返してね', 36, NAVY, 900, 'middle')
    b += T(540, 1118, '体験会や練習会は、プロフィールのリンクから', 30, GREY, 500, 'middle')
    b += T(540, 1222, '一緒にやる友達にも、送ってみてね！', 32, WHITE, 700, 'middle')
    b += footer(7, WHITE)
    return page(b, NAVY)


SLIDES = {1: s1, 2: s2, 3: s3, 4: s4, 5: s5, 6: s6, 7: s7}
with sync_playwright() as p:
    br = p.chromium.launch()
    pg = br.new_page(viewport={'width': W, 'height': H})
    for n in PAGES:
        if n not in SLIDES: continue
        pg.set_content(f'<html><body style="margin:0">{SLIDES[n]()}</body></html>')
        pg.screenshot(path=os.path.join(OUT, f'dink_{n}.png'))
    br.close()
print('ok', PAGES)
