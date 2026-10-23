# 服・靴・持ち物のイラスト（SVGで描いて、PILに貼る）
import io, cairosvg
from PIL import Image

NAVY = '#0E3452'; SEA = '#1F7FB8'; CORAL = '#FF6B4A'; SUN = '#FFD678'; KIT = '#18A896'
LINE = '#AEBAC5'; INKS = '#0A2740'


def render(svg_inner, vw, vh, width):
    """viewBox vw×vh の絵を、幅 width px の RGBA 画像にする"""
    s = f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {vw} {vh}" width="{width}" height="{int(width * vh / vw)}">{svg_inner}</svg>'
    png = cairosvg.svg2png(bytestring=s.encode('utf-8'), output_width=width * 2)
    im = Image.open(io.BytesIO(png)).convert('RGBA')
    return im.resize((width, int(width * vh / vw)), Image.LANCZOS)


def sneaker(upper='#F3F5F7', accent=NAVY, tab=CORAL, sole='#FFFFFF', outsole=NAVY, flip=False):
    """コート用の運動靴（横から見た図、右向き）。viewBox 400×220"""
    import math
    g = f'''
    <g {'transform="translate(400,0) scale(-1,1)"' if flip else ''}>
    <path d="M24 196 H384 Q394 196 394 203 Q394 210 384 210 H26 Q16 210 16 203 Q16 196 24 196 Z" fill="{outsole}"/>
    <path d="M16 198 V160 Q16 150 30 150 L300 158 Q360 160 384 166 Q398 170 396 184 Q394 198 380 198 Z" fill="{sole}" stroke="{LINE}" stroke-width="3"/>
    <path d="M40 182 H350" stroke="{LINE}" stroke-width="3" stroke-linecap="round"/>
    <path d="M30 152 C24 120 26 84 40 58 C46 48 58 46 68 52 C84 62 104 66 122 60 L138 36 C146 26 164 26 170 36
             C196 62 240 84 290 100 C340 114 376 124 390 144 C396 154 394 164 384 166 L300 158 Z"
          fill="{upper}" stroke="{LINE}" stroke-width="3" stroke-linejoin="round"/>
    <path d="M300 158 C306 132 338 120 370 122 C386 130 396 150 388 164 Z" fill="#FFFFFF" stroke="{LINE}" stroke-width="2.5"/>
    <path d="M84 146 C150 148 230 152 298 156" fill="none" stroke="{LINE}" stroke-width="2.5" stroke-dasharray="6 6"/>
    <path d="M30 152 C24 120 26 84 40 58 C46 50 54 50 60 54 C66 72 78 82 96 86 C102 112 98 136 92 154 Z" fill="{accent}"/>
    <path d="M41 58 C36 40 50 32 60 40 L66 54 Z" fill="{tab}"/>
    <path d="M68 53 C84 63 104 67 122 61" fill="none" stroke="{accent}" stroke-width="6" stroke-linecap="round"/>
    <path d="M150 50 L274 100" stroke="{accent}" stroke-width="24" stroke-linecap="round"/>
    '''
    ux, uy = 124 / 133.7, 50 / 133.7; px, py = -uy, ux
    for t in (0.12, 0.32, 0.52, 0.72, 0.92):
        x, y = 150 + 124 * t, 50 + 50 * t
        g += f'<path d="M{x - px * 9:.1f} {y - py * 9:.1f} L{x + px * 9:.1f} {y + py * 9:.1f}" stroke="#FFFFFF" stroke-width="5" stroke-linecap="round"/>'
    g += '</g>'
    return g, 400, 220


# ---- 上から見た靴（3つとも同じ足型・同じ大きさ・つま先が上）。viewBox 160×340 ----
FOOT = ("M80 10 C122 10 146 44 148 96 C150 140 140 170 136 210 C132 250 140 290 120 316 "
        "C106 332 54 332 40 316 C20 290 28 250 24 210 C20 170 10 140 12 96 C14 44 38 10 80 10 Z")


def sneaker_top(upper='#F3F5F7', accent=NAVY, tab=CORAL):
    """運動靴（上から）"""
    g = f'''
    <path d="{FOOT}" fill="#FFFFFF" stroke="{LINE}" stroke-width="4"/>
    <g transform="translate(80 170) scale(0.9) translate(-80 -170)"><path d="{FOOT}" fill="{upper}" stroke="{LINE}" stroke-width="3"/></g>
    <path d="M36 70 C40 34 120 34 124 70" fill="none" stroke="{LINE}" stroke-width="3" stroke-dasharray="6 6"/>
    <rect x="56" y="78" width="48" height="140" rx="20" fill="{accent}"/>
    '''
    for y in (96, 122, 148, 174, 200):
        g += f'<path d="M50 {y} H110" stroke="#FFFFFF" stroke-width="7" stroke-linecap="round"/>'
    g += f'''
    <ellipse cx="80" cy="262" rx="34" ry="42" fill="{accent}"/>
    <ellipse cx="80" cy="266" rx="24" ry="32" fill="#2A3B4A"/>
    <rect x="68" y="304" width="24" height="22" rx="6" fill="{tab}"/>
    '''
    return g, 160, 340


def sandal():
    """ビーチサンダル（上から）"""
    g = f'''
    <path d="{FOOT}" fill="#E9DCC6" stroke="#C9B590" stroke-width="4"/>
    <g transform="translate(80 170) scale(0.88) translate(-80 -170)"><path d="{FOOT}" fill="#F4EBDC"/></g>
    <path d="M80 62 C58 84 34 116 26 146 M80 62 C102 84 126 116 134 146" fill="none" stroke="{SEA}" stroke-width="16" stroke-linecap="round"/>
    <circle cx="80" cy="62" r="10" fill="{SEA}"/>
    '''
    return g, 160, 340


def loafer():
    """革靴（上から）"""
    g = f'''
    <path d="{FOOT}" fill="#2A1A10"/>
    <g transform="translate(80 170) scale(0.93) translate(-80 -170)"><path d="{FOOT}" fill="#5A3A26"/></g>
    <path d="M36 150 C30 70 130 70 124 150" fill="none" stroke="#3E2818" stroke-width="5"/>
    <path d="M44 66 C60 40 100 40 116 66" fill="none" stroke="#8A5E42" stroke-width="8" stroke-linecap="round" opacity="0.7"/>
    <ellipse cx="80" cy="250" rx="40" ry="64" fill="#24160D"/>
    <rect x="34" y="162" width="92" height="20" rx="8" fill="#3E2818"/>
    '''
    return g, 160, 340


def bottle(body=SEA, cap=NAVY):
    """スポーツボトル。viewBox 120×260"""
    g = f'''
    <path d="M44 20 H76 Q82 20 82 28 V40 H38 V28 Q38 20 44 20 Z" fill="{cap}"/>
    <path d="M70 18 C92 8 104 26 92 40" fill="none" stroke="{cap}" stroke-width="7" stroke-linecap="round"/>
    <rect x="32" y="38" width="56" height="16" rx="5" fill="{cap}"/>
    <path d="M30 54 H90 Q104 54 104 72 V96 Q96 114 96 130 Q96 146 104 162 V236 Q104 252 86 252 H34 Q16 252 16 236 V162
             Q24 146 24 130 Q24 114 16 96 V72 Q16 54 30 54 Z" fill="{body}"/>
    <path d="M16 170 H104 V206 H16 Z" fill="#FFFFFF" opacity="0.9"/>
    <path d="M30 72 V100" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.7"/>
    '''
    return g, 120, 260


def towel(c='#BFE1F2', band=SEA):
    """たたんだタオル（2枚重ね）。viewBox 260×170"""
    g = ''
    for dy, col in ((0, '#A9D3EA'), (52, c)):
        y = 30 + dy
        g += f'''
        <path d="M14 {y} H226 C246 {y} 252 {y + 14} 252 {y + 40} C252 {y + 66} 246 {y + 80} 226 {y + 80} H14 Q6 {y + 80} 6 {y + 72} V{y + 8} Q6 {y} 14 {y} Z" fill="{col}"/>
        <path d="M226 {y + 4} C240 {y + 8} 244 {y + 22} 244 {y + 40} C244 {y + 58} 240 {y + 72} 226 {y + 76}" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.7"/>
        <path d="M30 {y} V{y + 80} M42 {y} V{y + 80}" stroke="{band}" stroke-width="6" opacity="0.55"/>
        '''
    return g, 260, 170


def cap(c=NAVY, brim='#0A2740', mesh='#2B5F86', pipe=CORAL):
    """スポーツキャップ（横から見た図、右向き。浅めのクラウンとメッシュ）。viewBox 300×170"""
    g = f'''
    <path d="M22 124 C20 72 70 40 138 40 C196 40 232 72 236 118 L236 124 Z" fill="{c}"/>
    <path d="M70 86 C100 70 146 66 176 74 L178 114 L68 116 Z" fill="{mesh}"/>
    '''
    for i in range(6):
        for j in range(3):
            g += f'<circle cx="{86 + i * 16 + j * 4}" cy="{86 + j * 11}" r="2.6" fill="#FFFFFF" opacity="0.55"/>'
    g += f'''
    <path d="M138 40 C150 60 156 90 154 122" fill="none" stroke="#FFFFFF" stroke-width="2.5" opacity="0.25"/>
    <circle cx="138" cy="41" r="7" fill="{c}"/>
    <path d="M190 112 C236 104 282 112 296 128 C300 134 294 140 284 138 C252 130 216 128 184 132 Z" fill="{brim}"/>
    <path d="M190 130 C222 126 256 128 288 138" fill="none" stroke="{pipe}" stroke-width="4" stroke-linecap="round"/>
    <rect x="22" y="112" width="30" height="12" rx="3" fill="{mesh}"/>
    '''
    return g, 300, 170


def tee(c=CORAL):
    """平置きのTシャツ（丸首）。viewBox 300×300"""
    dk = '#000000'
    g = f'''
    <path d="M112 22 C100 26 70 32 50 44 C34 54 18 80 8 104 L50 124 L70 104 V282 Q70 290 78 290 H222 Q230 290 230 282 V104
             L250 124 L292 104 C282 80 266 54 250 44 C230 32 200 26 188 22 C178 40 122 40 112 22 Z" fill="{c}"/>
    <path d="M112 22 C122 44 178 44 188 22" fill="none" stroke="{dk}" stroke-width="7" opacity="0.15"/>
    <path d="M8 104 L50 124" stroke="{dk}" stroke-width="5" opacity="0.12"/><path d="M292 104 L250 124" stroke="{dk}" stroke-width="5" opacity="0.12"/>
    '''
    return g, 300, 300


def shorts(c=NAVY, stripe='#FFFFFF'):
    """平置きのハーフパンツ。viewBox 260×200"""
    g = f'''
    <path d="M36 30 H224 L250 180 Q252 190 242 190 H150 L130 96 L110 190 H18 Q8 190 10 180 Z" fill="{c}"/>
    <rect x="34" y="14" width="192" height="26" rx="8" fill="{c}"/>
    <path d="M34 40 H226" stroke="#000000" stroke-width="3" opacity="0.2"/>
    <path d="M120 30 C112 46 104 56 96 60 M140 30 C148 46 156 56 164 60" fill="none" stroke="{stripe}" stroke-width="3" stroke-linecap="round"/>
    <path d="M40 40 L18 182 M220 40 L242 182" stroke="{stripe}" stroke-width="7"/>
    '''
    return g, 260, 200


def polo(c=NAVY, trim='#FFFFFF'):
    """平置きのポロシャツ。viewBox 300×300"""
    g = f'''
    <path d="M112 22 C100 26 70 32 50 44 C34 54 18 80 8 104 L50 124 L70 104 V282 Q70 290 78 290 H222 Q230 290 230 282 V104
             L250 124 L292 104 C282 80 266 54 250 44 C230 32 200 26 188 22 Z" fill="{c}"/>
    <path d="M8 104 L50 124 L56 112 L16 92 Z M292 104 L250 124 L244 112 L284 92 Z" fill="{trim}" opacity="0.9"/>
    <path d="M112 22 L150 64 L124 78 L102 30 Z M188 22 L150 64 L176 78 L198 30 Z" fill="{trim}"/>
    <rect x="144" y="60" width="12" height="54" rx="3" fill="#000000" opacity="0.18"/>
    <circle cx="150" cy="78" r="4" fill="{trim}"/><circle cx="150" cy="100" r="4" fill="{trim}"/>
    '''
    return g, 300, 300


def skort(c='#FFFFFF', stroke=LINE):
    """プリーツスコート。viewBox 260×180"""
    g = f'<path d="M50 14 H210 L250 164 Q252 172 244 172 H16 Q8 172 10 164 Z" fill="{c}" stroke="{stroke}" stroke-width="3"/>'
    g += f'<rect x="48" y="8" width="164" height="22" rx="6" fill="{c}" stroke="{stroke}" stroke-width="3"/>'
    for i in range(1, 6):
        xt = 50 + 160 * i / 6; xb = 10 + 240 * i / 6
        g += f'<path d="M{xt} 30 L{xb} 170" stroke="{stroke}" stroke-width="3"/>'
    return g, 260, 180


def arrow(c=NAVY):
    return f'<path d="M10 40 H90" stroke="{c}" stroke-width="10" stroke-linecap="round"/><path d="M72 18 L100 40 L72 62" fill="none" stroke="{c}" stroke-width="10" stroke-linecap="round" stroke-linejoin="round"/>', 110, 80


if __name__ == '__main__':
    import sys
    out = sys.argv[1]
    parts = [sneaker(), sneaker('#FFFFFF', SEA, SUN), flipflop(), loafer(), bottle(), towel(), cap(), polo(), skort()]
    sheet = Image.new('RGBA', (1500, 900), (255, 255, 255, 255))
    for i, (g, vw, vh) in enumerate(parts):
        im = render(g, vw, vh, 280)
        sheet.alpha_composite(im, (20 + (i % 5) * 300, 20 + (i // 5) * 440))
    sheet.save(out)


# ---- 斜め上から見た靴（立体）。上から見た足型 FOOT を斜めに投影し、少しずつ持ち上げて重ねて厚みを出す ----
PROJ = 'matrix(0.25 0.62 -0.95 -0.18 341 165)'  # 足型（つま先が上）→ つま先が右・斜め上から見た形


def _mix(c1, c2, t):
    a = [int(c1[i:i + 2], 16) for i in (1, 3, 5)]; b = [int(c2[i:i + 2], 16) for i in (1, 3, 5)]
    return '#%02x%02x%02x' % tuple(int(a[i] + (b[i] - a[i]) * t) for i in range(3))


def _layer(lift, k, fill, ox=80, oy=290, stroke=None, inner=''):
    st = f' stroke="{stroke}" stroke-width="2.5"' if stroke else ''
    return (f'<g transform="translate(0 {-lift:.1f}) {PROJ}"><g transform="translate({ox} {oy}) scale({k:.3f}) translate({-ox} {-oy})">'
            f'<path d="{FOOT}" fill="{fill}"{st}/>{inner}</g></g>')


def _stack(h0, h1, k0, k1, c0, c1, n=18, oy=290):
    g = ''
    for i in range(n + 1):
        t = i / n
        g += _layer(h0 + (h1 - h0) * t, k0 + (k1 - k0) * t, _mix(c0, c1, t), oy=oy)
    return g


def _ground():
    return ('<defs><radialGradient id="gs"><stop offset="0" stop-color="#0E3452" stop-opacity="0.28"/>'
            '<stop offset="1" stop-color="#0E3452" stop-opacity="0"/></radialGradient></defs>'
            '<ellipse cx="196" cy="236" rx="180" ry="30" fill="url(#gs)"/>')


def _top(lift, k, inner, oy=290):
    """いちばん上の段に、足型の座標系で模様を描く"""
    return (f'<g transform="translate(0 {-lift:.1f}) {PROJ}"><g transform="translate(80 {oy}) scale({k:.3f}) translate(-80 {-oy})">'
            f'{inner}</g></g>')


def _proj(x, y, lift=0):
    return (0.25 * x - 0.95 * y + 341, 0.62 * x - 0.18 * y + 165 - lift)


def _scaled(x, y, k, oy=290):
    return (80 + (x - 80) * k, oy + (y - oy) * k)


def _layer2(lift, sx, sy, fill, oy=300):
    return (f'<g transform="translate(0 {-lift:.1f}) {PROJ}"><g transform="translate(80 {oy}) scale({sx:.3f} {sy:.3f}) translate(-80 {-oy})">'
            f'<path d="{FOOT}" fill="{fill}"/></g></g>')


def _hw(y):
    """足型の半分の幅（上から見た図、y はつま先0〜かかと340）"""
    pts = [(10, 0), (30, 40), (60, 60), (100, 68), (150, 64), (200, 56), (250, 54), (290, 46), (320, 30), (332, 0)]
    for (y0, w0), (y1, w1) in zip(pts, pts[1:]):
        if y0 <= y <= y1: return w0 + (w1 - w0) * (y - y0) / (y1 - y0)
    return 0


def sneaker34():
    g = _ground()
    g += _stack(0, 7, 1.0, 1.0, '#13304A', '#0E3452', n=4)              # 底（紺のゴム）
    g += _stack(7, 30, 1.0, 0.995, '#C3CCD4', '#FFFFFF', n=12)           # ミッドソール（白・厚め）
    # アッパー：つま先は低く、履き口（かかと側）がいちばん高い。横幅はほぼ保ち、前後を短くしていく
    H0, H1, n = 30, 104, 40
    SX = lambda t: 0.95 - 0.10 * t
    SY = lambda t: 0.96 - 0.50 * (t ** 0.85)
    for i in range(n + 1):
        t = i / n
        g += _layer2(H0 + (H1 - H0) * t, SX(t), SY(t), _mix('#C9D2DA', '#F8FAFB', t))
    # つま先の補強（うすいグレー）
    for i in range(0, 12):
        t = i / 40
        sx, sy, lift = SX(t), SY(t), H0 + (H1 - H0) * t
        g += (f'<g transform="translate(0 {-lift:.1f}) {PROJ}"><g transform="translate(80 300) scale({sx:.3f} {sy:.3f}) translate(-80 -300)">'
              f'<clipPath id="tc{i}"><rect x="0" y="0" width="160" height="70"/></clipPath>'
              f'<path d="{FOOT}" fill="{_mix("#D5DCE3", "#E9EEF2", i / 11)}" clip-path="url(#tc{i})"/></g></g>')
    # 手前の横の、紺のライン（なめらかに、かかとへ少し上がる）
    side = []
    for i in range(16):
        yy = 120 + 175 * i / 15
        t = 0.22 + 0.25 * (i / 15) ** 1.5
        sx, sy, lift = SX(t), SY(t), H0 + (H1 - H0) * t
        side.append(_proj(80 + _hw(yy) * sx, 300 + (yy - 300) * sy, lift))
    d = 'M' + ' L'.join(f'{px:.1f} {py:.1f}' for px, py in side)
    g += f'<path d="{d}" fill="none" stroke="#0E3452" stroke-width="12" stroke-linecap="round" stroke-linejoin="round"/>'
    # ベロと靴ひも（甲の坂）
    pts = []
    for i in range(21):
        t = 0.2 + 0.78 * i / 20
        sy = SY(t); lift = H0 + (H1 - H0) * t
        pts.append(_proj(80, 300 + (10 - 300) * sy + 20, lift))
    d = 'M' + ' L'.join(f'{px:.1f} {py:.1f}' for px, py in pts)
    g += f'<path d="{d}" fill="none" stroke="#E4E9EE" stroke-width="34" stroke-linecap="round" stroke-linejoin="round"/>'
    g += f'<path d="{d}" fill="none" stroke="#0E3452" stroke-width="5" stroke-linecap="round" opacity="0.25"/>'
    for i in range(2, 21, 3):
        t = 0.2 + 0.78 * i / 20
        sy = SY(t); sx = SX(t); lift = H0 + (H1 - H0) * t
        yf = 300 + (10 - 300) * sy + 20
        p1 = _proj(80 - 22 * sx, yf, lift); p2 = _proj(80 + 22 * sx, yf, lift)
        g += f'<path d="M{p1[0]:.1f} {p1[1]:.1f} L{p2[0]:.1f} {p2[1]:.1f}" stroke="#0E3452" stroke-width="6" stroke-linecap="round"/>'
    # 履き口：やわらかい白いふち＋中は濃い色、かかとのつまみ
    sx1, sy1 = SX(1), SY(1)
    g += (f'<g transform="translate(0 {-H1}) {PROJ}"><g transform="translate(80 300) scale({sx1:.3f} {sy1:.3f}) translate(-80 -300)">'
          '<rect x="50" y="10" width="60" height="110" rx="26" fill="#E4E9EE"/><path d="M58 40 H102 M58 70 H102 M58 100 H102" stroke="#0E3452" stroke-width="6" stroke-linecap="round"/><ellipse cx="80" cy="212" rx="58" ry="110" fill="#E3E8ED"/>'
          '<ellipse cx="80" cy="216" rx="46" ry="96" fill="#2A3D50"/>'
          '<ellipse cx="80" cy="228" rx="38" ry="78" fill="#1B2B3A"/>'
          '<rect x="66" y="320" width="28" height="18" rx="7" fill="#FF6B4A"/></g></g>')
    return g, 400, 300


def sandal34():
    g = _ground()
    g += _stack(0, 6, 1.0, 1.0, '#7A6248', '#8D7458', n=3)
    g += _stack(6, 22, 1.0, 1.0, '#C9B48F', '#DCC9A6', n=8)
    g += _layer(22, 1.0, '#F2E8D6')
    post = _proj(80, 62, 22); top_ = _proj(80, 62, 40)
    for side, col, w in ((-1, '#135A85', 20), (1, '#1F7FB8', 18)):
        ax, ay = (24, 150) if side < 0 else (136, 150)
        end = _proj(ax, ay, 22)
        c1 = _proj(80 + side * 20, 84, 62); c2 = _proj(ax + side * 2, ay - 40, 56)
        g += (f'<path d="M{top_[0]:.1f} {top_[1]:.1f} C{c1[0]:.1f} {c1[1]:.1f} {c2[0]:.1f} {c2[1]:.1f} {end[0]:.1f} {end[1]:.1f}" '
              f'fill="none" stroke="{col}" stroke-width="{w}" stroke-linecap="round"/>')
    g += f'<path d="M{post[0]:.1f} {post[1]:.1f} L{top_[0]:.1f} {top_[1]:.1f}" stroke="#1F7FB8" stroke-width="12" stroke-linecap="round"/>'
    g += f'<circle cx="{top_[0]:.1f}" cy="{top_[1]:.1f}" r="10" fill="#1F7FB8"/>'
    return g, 400, 300


def loafer34():
    g = _ground()
    g += _stack(0, 8, 1.0, 1.0, '#1C110A', '#2A1A10', n=4)
    g += _stack(8, 64, 0.98, 0.7, '#3E2818', '#6B4630', n=24)
    top = ('<path d="M34 156 C26 70 134 70 126 156" fill="none" stroke="#3E2818" stroke-width="6"/>'
           '<path d="M46 62 C62 36 98 36 114 62" fill="none" stroke="#9A6C4E" stroke-width="10" stroke-linecap="round" opacity="0.7"/>'
           '<rect x="32" y="162" width="96" height="22" rx="9" fill="#3E2818"/>'
           '<ellipse cx="80" cy="252" rx="44" ry="66" fill="#3E2818"/><ellipse cx="80" cy="256" rx="36" ry="58" fill="#1E120A"/>')
    g += _top(64, 0.7, top)
    return g, 400, 300
