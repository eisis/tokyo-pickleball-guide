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


def flipflop():
    """ビーチサンダル（上から見た図）。viewBox 120×240"""
    g = f'''
    <path d="M60 8 C92 8 108 40 104 84 C100 120 92 140 96 176 C100 214 84 234 60 234 C36 234 20 214 24 176
             C28 140 20 120 16 84 C12 40 28 8 60 8 Z" fill="#E9C9A1" stroke="#B88E62" stroke-width="4"/>
    <path d="M58 50 C40 70 28 96 24 116 M58 50 C78 70 92 96 98 116" fill="none" stroke="{CORAL}" stroke-width="12" stroke-linecap="round"/>
    <circle cx="58" cy="50" r="7" fill="{CORAL}"/>
    '''
    return g, 120, 240


def loafer():
    """革靴（横から見た図）。viewBox 300×140"""
    g = '''
    <path d="M16 112 C10 84 16 60 34 52 C54 46 76 48 96 50 C132 36 192 42 238 66 C272 80 294 96 290 112 Z" fill="#5A3A26"/>
    <path d="M96 50 C132 36 192 42 238 66 C200 62 150 58 104 62 Z" fill="#7A5038"/>
    <path d="M112 72 C140 64 176 66 204 74" fill="none" stroke="#3A2416" stroke-width="6" stroke-linecap="round"/>
    <path d="M12 110 H292 Q298 110 296 118 Q294 124 286 124 H56 V132 H16 Q10 132 10 124 Z" fill="#2A1A10"/>
    '''
    return g, 300, 140


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


def cap(c=NAVY, brim='#0A2740'):
    """スポーツキャップ（正面から見た図）。viewBox 300×190"""
    g = f'''
    <path d="M44 134 C40 56 92 22 150 22 C208 22 260 56 256 134 Z" fill="{c}"/>
    <path d="M150 24 C128 50 118 90 118 128 M150 24 C172 50 182 90 182 128" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.25"/>
    <circle cx="150" cy="22" r="9" fill="{c}"/>
    <circle cx="100" cy="66" r="4" fill="#FFFFFF" opacity="0.4"/><circle cx="200" cy="66" r="4" fill="#FFFFFF" opacity="0.4"/>
    <path d="M36 118 C90 138 210 138 264 118 C276 132 252 168 150 172 C48 168 24 132 36 118 Z" fill="{brim}"/>
    <path d="M60 140 C110 156 190 156 240 140" fill="none" stroke="#FFFFFF" stroke-width="3" opacity="0.3" stroke-dasharray="6 6"/>
    '''
    return g, 300, 190


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
