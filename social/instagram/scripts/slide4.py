from PIL import Image, ImageDraw, ImageFont
W, H = 1080, 1350
SP = '/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/'
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)
NAVY = (14, 52, 82); SAND = (246, 236, 216); CORAL = (255, 107, 74); WHITE = (255, 255, 255)
INK = (30, 40, 50); GREY = (90, 100, 110)

im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
def text(xy, s, f, fill, anchor='la'): d.text(xy, s, font=f, fill=fill, anchor=anchor)
def pill(x, y, s, f, bg, fg, padx=24, pady=12):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + padx * 2, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    text((x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')

pill(70, 120, 'STEP 3', font('Black', 30), CORAL, WHITE)
text((70, 205), '予約する', font('Black', 80), NAVY)
text((72, 318), 'コートのページから、そのまま予約へ', font('Medium', 36), GREY)

# スマホ（実際のサイト画面：東京タワーのコートページ）
sw = 360; sh = int(sw * 844 / 390)
px, py = 610, 400
d.rounded_rectangle((px - 20, py - 20, px + sw + 20, py + sh + 20), radius=56, fill=NAVY)
shot = Image.open(SP + 'site_tt2.png').resize((sw, sh), Image.LANCZOS)
mask = Image.new('L', (sw, sh), 0); ImageDraw.Draw(mask).rounded_rectangle((0, 0, sw, sh), radius=38, fill=255)
im.paste(shot, (px, py), mask)
# 予約ボタンを丸で囲む
k = sw / 390
bx1, by1, bx2, by2 = px + 20 * k, py + 521 * k, px + 370 * k, py + 577 * k
d.rounded_rectangle((bx1 - 12, by1 - 12, bx2 + 12, by2 + 12), radius=40, outline=CORAL, width=8)
# 吹き出し「ここから予約」
d.rounded_rectangle((330, by1 - 120, 600, by1 - 40), radius=40, fill=CORAL)
text((465, by1 - 80), 'ここから予約', font('Black', 34), WHITE, 'mm')
d.polygon([(560, by1 - 44), (600, by1 - 44), (bx1 - 6, by1 + 6)], fill=CORAL)

# 左側の説明
steps = [('1', ['コートのページで', '予約方法を確認']),
         ('2', ['予約ボタンから', '公式の予約ページへ']),
         ('3', ['まずは1時間あれば', '十分楽しめる'])]
y = 430
for n, lines in steps:
    if n == '2': y = by1 + 60
    d.ellipse((70, y, 122, y + 52), fill=CORAL)
    text((96, y + 26), n, font('Black', 30), WHITE, 'mm')
    for i, l in enumerate(lines):
        text((140, y + 4 + i * 50), l, font('Bold', 36), INK)
    y += 50 * len(lines) + 60

text((70, H - 70), 'PICKLEBALL TOKYO', font('Bold', 26), NAVY, 'ls')
text((W - 70, H - 70), '4/7  @pickleballtokyo', font('Medium', 26), NAVY, 'rs')
im.save('/home/claude/ig-start/04.png')
