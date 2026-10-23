from PIL import Image, ImageOps, ImageDraw, ImageFont, ImageFilter
import os
W, H = 1080, 1350
OUT = '/home/claude/ig'
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)

NAVY = (14, 52, 82); SEA = (31, 127, 184); SAND = (246, 236, 216)
CORAL = (255, 107, 74); WHITE = (255, 255, 255); INK = (30, 40, 50)

photo = ImageOps.exif_transpose(Image.open('/mnt/user-data/uploads/IMG_2146.jpeg')).convert('RGB')

def cover_crop(img, box=None):
    if box: img = img.crop(box)
    r = max(W / img.width, H / img.height)
    img = img.resize((round(img.width * r), round(img.height * r)), Image.LANCZOS)
    x = (img.width - W) // 2; y = (img.height - H) // 2
    return img.crop((x, y, x + W, y + H))

def shade(img, top=0, bottom=230, start=0.35):
    g = Image.new('L', (1, H))
    for y in range(H):
        t = y / H
        a = top if t < start else top + (bottom - top) * ((t - start) / (1 - start)) ** 1.3
        g.putpixel((0, y), int(a))
    g = g.resize((W, H))
    black = Image.new('RGB', (W, H), (8, 22, 36))
    return Image.composite(black, img, g)

def text(d, xy, s, f, fill, anchor='la'):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def footer(d, color):
    text(d, (70, H - 70), 'PICKLEBALL TOKYO', font('Bold', 26), color, 'ls')
    text(d, (W - 70, H - 70), '@pickleballtokyo', font('Medium', 26), color, 'rs')

def pill(d, x, y, s, f, bg, fg, padx=26, pady=14):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + padx * 2, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    text(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')

# 1 cover
im = shade(cover_crop(photo), top=20, bottom=235, start=0.3)
d = ImageDraw.Draw(im)
pill(d, 70, 690, '東京・神奈川・千葉・埼玉', font('Bold', 30), CORAL, WHITE)
y = 790
for line in ['東京近郊で', 'ピックルボールが', 'できる場所、']:
    text(d, (66, y), line, font('Black', 92), WHITE, 'lt'); y += 118
text(d, (66, y + 6), 'まとめました', font('Black', 92), (255, 214, 120), 'lt')
text(d, (W - 70, H - 70), '@pickleballtokyo  →', font('Bold', 28), WHITE, 'rs')
im.save(f'{OUT}/01.png')

# 2 why
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
text(d, (70, 230), 'WHY', font('Black', 34), CORAL)
y = 320
for line in ['コートは増えてるのに、', 'どこにあるのか', '分からない。']:
    text(d, (70, y), line, font('Black', 80), NAVY); y += 108
d.rectangle((70, y + 50, 190, y + 58), fill=CORAL)
y += 120
for line in ['自分がまさにそうでした。', 'だから首都圏のコートを', 'ひとつにまとめたサイトを', '作りました。']:
    text(d, (70, y), line, font('Medium', 46), INK); y += 72
footer(d, NAVY)
im.save(f'{OUT}/02.png')

# 3 areas
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
text(d, (70, 200), 'エリアから探せる', font('Black', 80), WHITE)
text(d, (70, 315), '近くのコートも地図でわかります', font('Medium', 40), (215, 235, 248))
areas = [('東京', 'TOKYO'), ('神奈川', 'KANAGAWA'), ('千葉', 'CHIBA'), ('埼玉', 'SAITAMA')]
cw, ch, gap = 450, 300, 40
for i, (jp, en) in enumerate(areas):
    x = 70 + (i % 2) * (cw + gap); y = 450 + (i // 2) * (ch + gap)
    d.rounded_rectangle((x, y, x + cw, y + ch), radius=36, fill=WHITE)
    d.ellipse((x + 40, y + 46, x + 64, y + 70), fill=CORAL)
    text(d, (x + 40, y + 190), jp, font('Black', 84), NAVY, 'ls')
    text(d, (x + 44, y + 245), en, font('Bold', 28), SEA, 'ls')
footer(d, WHITE)
im.save(f'{OUT}/03.png')

# 4 three points
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
text(d, (70, 180), 'はじめてなら', font('Bold', 46), CORAL)
text(d, (70, 250), 'この3つで選べばOK', font('Black', 76), NAVY)
pts = [('01', '道具のレンタル', 'パドルやボールを借りられるか'),
       ('02', '予約の方法', 'ネット予約か、電話か、当日か'),
       ('03', '屋内か屋外か', '雨の日も遊べるかどうか')]
y = 420
for n, t, s in pts:
    d.rounded_rectangle((70, y, W - 70, y + 230), radius=32, fill=WHITE)
    text(d, (115, y + 135), n, font('Black', 84), CORAL, 'ls')
    text(d, (270, y + 105), t, font('Black', 54), NAVY, 'ls')
    text(d, (270, y + 170), s, font('Medium', 36), (90, 100, 110), 'ls')
    y += 265
footer(d, NAVY)
im.save(f'{OUT}/04.png')

# 5 tokyo tower (court-side crop)
pw, ph = photo.size
crop = cover_crop(photo, (0, int(ph * 0.33), pw, ph))
im = shade(crop, top=150, bottom=200, start=0.0)
im = Image.blend(crop, im, 0.55)
d = ImageDraw.Draw(im)
pill(d, 70, 150, '実際に行ってきました', font('Bold', 32), CORAL, WHITE)
text(d, (66, 250), '東京タワーの', font('Black', 96), WHITE)
text(d, (66, 370), 'コート', font('Black', 96), WHITE)
y = 1000
for line in ['見上げると、真上に東京タワーの鉄骨。', 'この景色の中でプレーできます。']:
    text(d, (70, y), line, font('Bold', 42), WHITE); y += 66
text(d, (70, y + 30), 'くわしいレビューは次の投稿で', font('Medium', 34), (255, 214, 120))
footer(d, WHITE)
im.save(f'{OUT}/05.png')

# 6 what we post
im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
text(d, (70, 200), 'このアカウントで', font('Bold', 50), (170, 205, 230))
text(d, (70, 275), '発信すること', font('Black', 88), WHITE)
items = [('コートのレビュー', '実際に行って、良かったところも正直に'),
         ('新しくできたコート', '首都圏の新コート情報をいち早く'),
         ('練習会・イベント', '一緒にプレーできる場も作っていきます')]
y = 470
for t, s in items:
    d.ellipse((70, y + 14, 106, y + 50), fill=CORAL)
    text(d, (140, y), t, font('Black', 58), WHITE)
    text(d, (140, y + 90), s, font('Medium', 36), (170, 205, 230))
    y += 230
footer(d, (170, 205, 230))
im.save(f'{OUT}/06.png')

# 7 CTA
im = Image.new('RGB', (W, H), CORAL); d = ImageDraw.Draw(im)
text(d, (W // 2, 330), '全コートの地図と検索は', font('Black', 64), WHITE, 'mm')
text(d, (W // 2, 430), 'プロフィールのリンクから', font('Black', 64), WHITE, 'mm')
d.rounded_rectangle((110, 560, W - 110, 700), radius=70, fill=WHITE)
text(d, (W // 2, 630), 'pickleball-tokyo.com', font('Black', 54), CORAL, 'mm')
text(d, (W // 2, 860), '保存して、次のコート探しに。', font('Bold', 46), WHITE, 'mm')
text(d, (W // 2, 940), 'フォローもぜひ！', font('Bold', 46), WHITE, 'mm')
text(d, (W // 2, 1150), '@pickleballtokyo', font('Black', 50), WHITE, 'mm')
text(d, (W // 2, 1215), 'PICKLEBALL TOKYO', font('Bold', 28), (255, 225, 210), 'mm')
im.save(f'{OUT}/07.png')

# contact sheet
sheet = Image.new('RGB', (4 * 270 + 50, 2 * 338 + 30), (200, 200, 200))
for i in range(7):
    t = Image.open(f'{OUT}/0{i+1}.png').resize((270, 338))
    sheet.paste(t, (10 + (i % 4) * 280, 10 + (i // 4) * 348))
sheet.save('/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/sheet.png')
