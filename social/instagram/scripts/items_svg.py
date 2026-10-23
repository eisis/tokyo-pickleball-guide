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


def sandal():
    """シャワーサンダル（横から見た図、右向き）。運動靴と同じ viewBox 400×220・同じ縮尺"""
    g = '''
    <path d="M30 210 H372 Q392 210 394 196 Q396 182 380 178 L46 168 Q24 168 22 186 Q20 210 30 210 Z" fill="#3E4A55"/>
    <path d="M26 178 Q28 160 48 158 L376 168 Q392 170 390 180 L26 182 Z" fill="#E9E1D3"/>
    <path d="M140 170 C146 124 192 104 250 104 C304 104 344 126 372 170 Z" fill="#1F7FB8"/>
    <path d="M160 168 C166 132 202 116 250 116 C294 116 328 134 350 168" fill="none" stroke="#FFFFFF" stroke-width="4" opacity="0.35"/>
    <path d="M196 120 C228 112 272 112 302 122" fill="none" stroke="#FFFFFF" stroke-width="8" stroke-linecap="round" opacity="0.5"/>
    '''
    return g, 400, 220


def loafer():
    """革靴（横から見た図、右向き）。運動靴と同じ viewBox 400×220・同じ縮尺"""
    g = '''
    <path d="M30 196 C22 164 26 136 44 126 C70 120 100 122 128 126 C144 114 196 108 246 118
             C290 128 330 142 362 158 C386 170 394 182 390 192 C388 196 384 198 378 198 L30 198 Z" fill="#5A3A26"/>
    <path d="M160 122 C220 112 300 132 362 160" fill="none" stroke="#3E2818" stroke-width="4"/>
    <path d="M144 134 C196 124 236 128 270 140" fill="none" stroke="#3E2818" stroke-width="12" stroke-linecap="round"/>
    <path d="M250 124 C300 132 344 150 372 168" fill="none" stroke="#8A5E42" stroke-width="6" stroke-linecap="round" opacity="0.8"/>
    <path d="M44 128 C70 124 100 126 128 128" fill="none" stroke="#3E2818" stroke-width="5" stroke-linecap="round"/>
    <path d="M24 196 H384 Q394 196 394 202 Q394 208 384 208 H96 V214 H28 Q22 214 22 206 Z" fill="#2A1A10"/>
    '''
    return g, 400, 220


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
