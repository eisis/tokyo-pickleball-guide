from PIL import Image, ImageDraw, ImageFont
import os
W, H = 1080, 1350
OUT = '/home/claude/ig-start'
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)

NAVY = (14, 52, 82); SEA = (31, 127, 184); SAND = (246, 236, 216)
CORAL = (255, 107, 74); WHITE = (255, 255, 255); INK = (30, 40, 50)
SUN = (255, 214, 120); GREY = (90, 100, 110); KIT = (24, 168, 150); PALE = (255, 241, 230)
N = 7

def text(d, xy, s, f, fill, anchor='la'): d.text(xy, s, font=f, fill=fill, anchor=anchor)
def footer(d, color, page):
    text(d, (70, H - 70), 'PICKLEBALL TOKYO', font('Bold', 26), color, 'ls')
    text(d, (W - 70, H - 70), f'{page}/{N}  @pickleballtokyo', font('Medium', 26), color, 'rs')
def pill(d, x, y, s, f, bg, fg, padx=24, pady=12):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + padx * 2, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    text(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')
def step_slide(n, title, sub, tips, draw_icon, page):
    im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
    pill(d, 70, 120, f'STEP {n}', font('Black', 30), CORAL, WHITE)
    text(d, (70, 205), title, font('Black', 80), NAVY)
    text(d, (72, 318), sub, font('Medium', 38), GREY)
    d.rounded_rectangle((70, 400, W - 70, 840), radius=36, fill=WHITE)
    draw_icon(d, W // 2, 620)
    y = 900
    for t in tips:
        d.ellipse((76, y + 14, 98, y + 36), fill=CORAL)
        text(d, (120, y), t, font('Bold', 40), INK)
        y += 80
    footer(d, NAVY, page)
    im.save(f'{OUT}/0{page}.png')

def person(d, x, y, s=1.0, c=NAVY):
    r = 34 * s
    d.ellipse((x - r, y - r - 70 * s, x + r, y + r - 70 * s), fill=c)
    d.rounded_rectangle((x - 58 * s, y - 20 * s, x + 58 * s, y + 90 * s), radius=int(50 * s), fill=c)
def paddle(d, x, y, c=SEA, s=1.0):
    """ピックルボールのパドル：縦長の角丸の板＋太めのグリップ（卓球ラケットに見えないように）"""
    d.rounded_rectangle((x - 70 * s, y - 170 * s, x + 70 * s, y + 50 * s), radius=int(34 * s), fill=c)
    d.rounded_rectangle((x - 70 * s, y - 170 * s, x + 70 * s, y + 50 * s), radius=int(34 * s), outline=NAVY, width=6)
    d.rounded_rectangle((x - 22 * s, y + 46 * s, x + 22 * s, y + 160 * s), radius=int(10 * s), fill=NAVY)
    for k in range(3):
        yy = y + (70 + k * 28) * s
        d.line((x - 22 * s, yy, x + 22 * s, yy + 10 * s), fill=(60, 90, 120), width=4)
def ball(d, x, y, r=46):
    d.ellipse((x - r, y - r, x + r, y + r), fill=SUN, outline=(220, 170, 60), width=4)
    for dx, dy in [(-18, -14), (16, -18), (0, 8), (-20, 22), (20, 18)]:
        d.ellipse((x + dx - 6, y + dy - 6, x + dx + 6, y + dy + 6), fill=(220, 170, 60))

# 1 表紙（元のデザイン＋右上に「アメリカで人気爆発中！」のシール）
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
for i, c in enumerate([WHITE, SUN, WHITE, SUN]):
    person(d, 640 + i * 105, 1000, 0.8, c)
ball(d, 930, 760, 50)
pill(d, 70, 260, 'はじめての人へ', font('Black', 34), CORAL, WHITE)
y = 360
for line, f, c in [('友達と', 96, WHITE), ('ピックルボールを', 96, WHITE), ('始めるなら', 96, WHITE), ('この順番で', 96, SUN)]:
    text(d, (66, y), line, font('Black', f), c, 'lt'); y += 124
text(d, (70, 920), '道具がなくても、', font('Bold', 40), (215, 235, 248))
text(d, (70, 976), '今週末から始められます', font('Bold', 40), (215, 235, 248))
text(d, (70, H - 70), '@pickleballtokyo', font('Bold', 28), WHITE, 'ls')
text(d, (W - 70, H - 70), 'スワイプ →', font('Bold', 30), WHITE, 'rs')
# 見出しの上に一行：白「アメリカで」＋黄「人気爆発中」に下線（シールより控えめに、文字の大きさで印象を出す）
f1 = font('Black', 60)
text(d, (70, 112), 'アメリカで', f1, WHITE)
x2 = 70 + d.textlength('アメリカで', font=f1) + 6
text(d, (x2, 112), '人気爆発中', f1, SUN)
x3 = x2 + d.textlength('人気爆発中', font=f1)
d.rounded_rectangle((x2, 198, x3, 207), radius=5, fill=SUN)
text(d, (x3 + 2, 112), '!', f1, SUN)
im.save(f'{OUT}/01.png')

# 3 4人集める
def icon2(d, cx, cy):
    for i in range(4):
        person(d, cx - 270 + i * 180, cy + 10, 0.95, [NAVY, CORAL, NAVY, CORAL][i])
    text(d, (cx, cy + 165), '4人で1コート', font('Black', 40), NAVY, 'mm')
step_slide(1, '4人集める', 'ダブルス（2対2）が基本です',
           ['4人いれば1コートで試合ができる', '2〜3人でも打ち合いは楽しめる', '経験者が1人いると心強い'], icon2, 2)

# 3 レンタルありのコートを選ぶ
def icon3(d, cx, cy):
    paddle(d, cx - 120, cy - 10, SEA); paddle(d, cx + 40, cy - 10, CORAL)
    ball(d, cx + 220, cy + 80)
    text(d, (cx, cy + 180), 'パドルとボールは借りられる', font('Black', 36), NAVY, 'mm')
step_slide(2, 'コートを探す', 'pickleball-tokyo.comで「レンタルあり」を選ぼう',
           ['レンタルありなら、道具なしでOK', '無料で貸してくれるコートもある', '屋内か屋外かも見ておく'], icon3, 3)

# 4 予約する
def icon4(d, cx, cy):
    x0, y0 = cx - 120, cy - 190
    d.rounded_rectangle((x0, y0, x0 + 240, y0 + 400), radius=36, fill=NAVY)
    d.rounded_rectangle((x0 + 16, y0 + 40, x0 + 224, y0 + 360), radius=16, fill=WHITE)
    text(d, (cx, y0 + 80), '予約', font('Black', 34), NAVY, 'mm')
    for r in range(3):
        for c in range(4):
            fill = CORAL if (r, c) == (1, 2) else (226, 236, 244)
            d.rounded_rectangle((x0 + 34 + c * 45, y0 + 120 + r * 60, x0 + 70 + c * 45, y0 + 160 + r * 60), radius=8, fill=fill)
    d.rounded_rectangle((x0 + 40, y0 + 300, x0 + 200, y0 + 340), radius=20, fill=CORAL)
    text(d, (cx, y0 + 320), '予約する', font('Black', 22), WHITE, 'mm')
step_slide(3, 'ネットで予約', 'ほとんどのコートはスマホで予約できます',
           ['まずは1時間あれば十分楽しめる', '週末は早めに埋まりやすい', '予約ページは公式サイトから'], icon4, 4)

# 5 服装と持ち物
def icon5(d, cx, cy):
    items = ['動きやすい服', '運動靴（屋内は室内用も）', '飲み物・タオル', '着替え']
    y = cy - 170
    for s in items:
        d.rounded_rectangle((cx - 330, y, cx - 280, y + 50), radius=10, outline=KIT, width=6)
        d.line((cx - 320, y + 26, cx - 308, y + 38, cx - 288, y + 12), fill=KIT, width=7)
        text(d, (cx - 250, y + 25), s, font('Black', 40), NAVY, 'lm')
        y += 90
step_slide(4, '服装と持ち物', '特別なものは要りません',
           ['屋内は室内用シューズが必要な施設も', '更衣室がないコートもある', '持ち物は施設のページで確認'], icon5, 5)

# 6 ルールは3つだけ
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
pill(d, 70, 120, 'STEP 5', font('Black', 30), CORAL, WHITE)
text(d, (70, 205), 'ルールは3つだけ', font('Black', 80), NAVY)
text(d, (72, 318), 'あとは打ちながら覚えれば大丈夫', font('Medium', 38), GREY)
y = 420
for i, s in enumerate(['サーブは下から、対角線へ', '最初の2回はワンバウンド', 'キッチンではボレーしない']):
    d.rounded_rectangle((70, y, W - 70, y + 150), radius=30, fill=WHITE)
    d.ellipse((100, y + 45, 160, y + 105), fill=CORAL)
    text(d, (130, y + 75), str(i + 1), font('Black', 36), WHITE, 'mm')
    text(d, (190, y + 75), s, font('Black', 46), NAVY, 'lm')
    y += 180
d.rounded_rectangle((70, 980, W - 70, 1140), radius=28, fill=PALE)
text(d, (110, 1018), '図でくわしく知りたい人は', font('Bold', 36), INK)
text(d, (110, 1074), '前回の「基本ルール」の投稿へ', font('Black', 40), CORAL)
footer(d, NAVY, 6)
im.save(f'{OUT}/06.png')

# 7 送客（実際にたどる順番：プロフィール → サイト → 絞り込み）
im = Image.new('RGB', (W, H), CORAL); d = ImageDraw.Draw(im)
text(d, (W // 2, 230), 'レンタルできるコートは', font('Black', 64), WHITE, 'mm')
text(d, (W // 2, 330), 'サイトですぐ探せます', font('Black', 64), WHITE, 'mm')
flow = [('1', 'プロフィールのリンクから'), ('2', 'pickleball-tokyo.comへ'), ('3', '「レンタルあり」で絞り込み')]
y = 440
for i, (n, s_) in enumerate(flow):
    d.rounded_rectangle((130, y, W - 130, y + 110), radius=55, fill=WHITE)
    d.ellipse((150, y + 20, 220, y + 90), fill=CORAL)
    text(d, (185, y + 55), n, font('Black', 38), WHITE, 'mm')
    text(d, (250, y + 55), s_, font('Black', 42), CORAL, 'lm')
    if i < 2:
        d.polygon([(W // 2 - 22, y + 122), (W // 2 + 22, y + 122), (W // 2, y + 150)], fill=WHITE)
    y += 165
text(d, (W // 2, 1000), '一緒に始めたい友達に', font('Bold', 42), (255, 230, 220), 'mm')
text(d, (W // 2, 1060), 'この投稿を送ってみてください', font('Bold', 42), (255, 230, 220), 'mm')
text(d, (W // 2, 1190), '@pickleballtokyo', font('Black', 44), WHITE, 'mm')
im.save(f'{OUT}/07.png')

sheet = Image.new('RGB', (5 * 270 + 60, 2 * 338 + 30), (200, 200, 200))
for i in range(N):
    t = Image.open(f'{OUT}/0{i+1}.png').resize((270, 338))
    sheet.paste(t, (10 + (i % 5) * 280, 10 + (i // 5) * 348))
sheet.save('/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/start_sheet.png')
