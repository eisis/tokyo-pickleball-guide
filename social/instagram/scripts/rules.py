from PIL import Image, ImageDraw, ImageFont
import os, math
W, H = 1080, 1350
OUT = '/home/claude/ig-rules'
os.makedirs(OUT, exist_ok=True)
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)

NAVY = (14, 52, 82); SEA = (31, 127, 184); SAND = (246, 236, 216)
CORAL = (255, 107, 74); WHITE = (255, 255, 255); INK = (30, 40, 50)
SUN = (255, 214, 120); GREY = (90, 100, 110); COURT = (39, 140, 196); KIT = (24, 168, 150)

def text(d, xy, s, f, fill, anchor='la'): d.text(xy, s, font=f, fill=fill, anchor=anchor)
def footer(d, color, page):
    text(d, (70, H - 70), 'PICKLEBALL TOKYO', font('Bold', 26), color, 'ls')
    text(d, (W - 70, H - 70), f'{page}/8  @pickleballtokyo', font('Medium', 26), color, 'rs')
def pill(d, x, y, s, f, bg, fg, padx=24, pady=12):
    w = d.textlength(s, font=f)
    d.rounded_rectangle((x, y, x + w + padx * 2, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    text(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')
    return x + w + padx * 2
def head(d, no, title, sub, dark=False):
    if no: pill(d, 70, 120, no, font('Black', 30), CORAL, WHITE)
    text(d, (70, 205), title, font('Black', 76), WHITE if dark else NAVY)
    if sub: text(d, (72, 310), sub, font('Medium', 38), (215, 235, 248) if dark else GREY)

def court(d, x, y, w, h, kitchen=KIT, surface=COURT, line=WHITE, lw=5):
    """縦向きのコート（上が相手、下が自分）。キッチンはネットから全長の15.9%ずつ"""
    k = h * 2.13 / 13.41
    mid = y + h / 2
    d.rectangle((x, y, x + w, y + h), fill=surface)
    d.rectangle((x, mid - k, x + w, mid + k), fill=kitchen)
    d.rectangle((x, y, x + w, y + h), outline=line, width=lw)
    d.line((x, mid - k, x + w, mid - k), fill=line, width=lw)
    d.line((x, mid + k, x + w, mid + k), fill=line, width=lw)
    d.line((x + w / 2, y, x + w / 2, mid - k), fill=line, width=lw)
    d.line((x + w / 2, mid + k, x + w / 2, y + h), fill=line, width=lw)
    d.line((x - 18, mid, x + w + 18, mid), fill=NAVY, width=9)  # ネット
    return k, mid

def arrow(d, p, q, color, width=7, dash=None, head_len=30):
    (x1, y1), (x2, y2) = p, q
    ang = math.atan2(y2 - y1, x2 - x1)
    ex, ey = x2 - head_len * 0.8 * math.cos(ang), y2 - head_len * 0.8 * math.sin(ang)
    if dash:
        L = math.hypot(ex - x1, ey - y1); n = int(L // dash)
        for i in range(0, n, 2):
            a, b = i / n, min((i + 1) / n, 1)
            d.line((x1 + (ex - x1) * a, y1 + (ey - y1) * a, x1 + (ex - x1) * b, y1 + (ey - y1) * b), fill=color, width=width)
    else:
        d.line((x1, y1, ex, ey), fill=color, width=width)
    a1, a2 = ang + 2.6, ang - 2.6
    d.polygon([(x2, y2), (x2 + head_len * math.cos(a1), y2 + head_len * math.sin(a1)), (x2 + head_len * math.cos(a2), y2 + head_len * math.sin(a2))], fill=color)

def bounce(d, x, y, color=SUN):
    d.ellipse((x - 16, y - 16, x + 16, y + 16), fill=color, outline=NAVY, width=4)
def badge(d, x, y, n, bg=CORAL):
    d.ellipse((x - 26, y - 26, x + 26, y + 26), fill=bg)
    text(d, (x, y), str(n), font('Black', 32), WHITE, 'mm')
def person(d, x, y, color=NAVY):
    d.ellipse((x - 18, y - 18, x + 18, y + 18), fill=color, outline=WHITE, width=4)

def bullets(d, x, y, items, f=None, gap=78, color=INK, dot=CORAL):
    f = f or font('Bold', 42)
    for s in items:
        d.ellipse((x, y + 14, x + 20, y + 34), fill=dot)
        text(d, (x + 40, y), s, f, color)
        y += gap
    return y

# 1 表紙
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
court(d, 620, 300, 330, 724, kitchen=(28, 160, 150), surface=(48, 150, 205))
bounce(d, 700, 420); arrow(d, (880, 1000), (712, 438), SUN, dash=22)
pill(d, 70, 300, '保存版', font('Black', 34), CORAL, WHITE)
y = 400
for line, c in [('3分でわかる', SUN), ('ピックル', WHITE), ('ボールの', WHITE), ('基本ルール', WHITE)]:
    text(d, (66, y), line, font('Black', 96 if c == WHITE else 64), c, 'lt'); y += 128 if c == WHITE else 96
text(d, (70, 1010), 'コートに行く前に、', font('Bold', 38), (215, 235, 248))
text(d, (70, 1064), 'これだけ覚えればOK', font('Bold', 38), (215, 235, 248))
text(d, (W - 70, H - 70), 'スワイプ →', font('Bold', 30), WHITE, 'rs')
text(d, (70, H - 70), '@pickleballtokyo', font('Bold', 28), WHITE, 'ls')
im.save(f'{OUT}/01.png')

# 2 どんなスポーツ
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
head(d, None, 'まずは全体像', 'テニス・バドミントン・卓球のいいとこ取り')
cx, cy, cw, ch = 100, 420, 300, 660
k, mid = court(d, cx, cy, cw, ch)
text(d, (cx + cw / 2, cy - 22), '約6.1m × 約13.4m', font('Bold', 30), NAVY, 'ms')
text(d, (cx + cw / 2, mid - k / 2 + 4), 'ネット ↓', font('Bold', 28), WHITE, 'mm')
text(d, (cx + cw / 2, mid + k / 2 + 4), 'キッチン', font('Bold', 28), WHITE, 'mm')
y = 440
for t, s in [('広さ', 'バドミントンと同じ'), ('人数', 'ダブルスが基本'), ('道具', 'パドルと穴あきボール'), ('勝敗', '11点先取')]:
    text(d, (500, y), t, font('Bold', 32), CORAL)
    text(d, (500, y + 46), s, font('Black', 44), NAVY)
    y += 160
text(d, (110, 1160), 'テニスコートの約4分の1。近い距離で打ち合います', font('Medium', 34), INK)
footer(d, NAVY, 2)
im.save(f'{OUT}/02.png')

# 3 サーブ
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
head(d, 'RULE 1', 'サーブは下から', '相手コートの対角線にワンバウンド')
cx, cy, cw, ch = 110, 410, 300, 660
k, mid = court(d, cx, cy, cw, ch)
person(d, cx + cw * 0.78, cy + ch + 34)
tx, ty = cx + cw * 0.25, cy + (mid - k - cy) * 0.45
arrow(d, (cx + cw * 0.78, cy + ch + 10), (tx + 8, ty + 22), CORAL, dash=22)
bounce(d, tx, ty)
text(d, (cx + cw * 0.78 + 34, cy + ch + 44), 'サーバー', font('Bold', 28), NAVY, 'ls')
bullets(d, 500, 470, ['腰より下で打つ', '対角線のエリアへ', 'キッチンに落ちたらアウト', 'チャンスは1回だけ'], f=font('Bold', 40), gap=110)
footer(d, NAVY, 3)
im.save(f'{OUT}/03.png')

# 4 ツーバウンドルール（1打ずつ、横向きの小さなコート3つで見せる）
def court_h(d, x, y, w, h, lw=4):
    """横向きのコート（左が自分たち、右が相手）"""
    k = w * 2.13 / 13.41; mid = x + w / 2
    d.rectangle((x, y, x + w, y + h), fill=COURT)
    d.rectangle((mid - k, y, mid + k, y + h), fill=KIT)
    d.rectangle((x, y, x + w, y + h), outline=WHITE, width=lw)
    for xx in (mid - k, mid + k): d.line((xx, y, xx, y + h), fill=WHITE, width=lw)
    d.line((x, y + h / 2, mid - k, y + h / 2), fill=WHITE, width=lw)
    d.line((mid + k, y + h / 2, x + w, y + h / 2), fill=WHITE, width=lw)
    d.line((mid, y - 12, mid, y + h + 12), fill=NAVY, width=8)
    return k, mid
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
head(d, 'RULE 2', '最初の2回はワンバウンド', 'サーブとリターンは、必ず1回弾ませてから打つ')
ORANGE = (255, 150, 50)
cx, cw, chh = 70, 500, 228
rows = [
    (1, 'サーブ', ['相手はワンバウンド', 'してから返す'], CORAL),
    (2, 'リターン', ['こちらもワンバウンド', 'してから返す'], ORANGE),
    (3, 'その後は', ['ノーバウンドで打つ', '（ボレー）のもOK'], SEA),
]
for i, (n, t, sub, c) in enumerate(rows):
    y = 400 + i * 268
    k, mid = court_h(d, cx, y, cw, chh)
    L = (cx + 30, y + chh * 0.72); R = (cx + cw - 30, y + chh * 0.28)
    if n == 1:
        b = (cx + cw * 0.80, y + chh * 0.28)
        person(d, *L); person(d, *R, color=GREY)
        arrow(d, L, (b[0] - 22, b[1] + 4), c, dash=20); bounce(d, *b)
    elif n == 2:
        b = (cx + cw * 0.20, y + chh * 0.72)
        person(d, *L, color=GREY); person(d, *R)
        arrow(d, R, (b[0] + 22, b[1] - 4), c, dash=20); bounce(d, *b)
    else:
        V = (mid + k + 26, y + chh * 0.40)
        person(d, *L); person(d, *V, color=GREY)
        arrow(d, L, (V[0] - 24, V[1] + 4), c, width=7)
        text(d, (V[0] + 30, V[1] - 2), 'ボレー', font('Black', 28), WHITE, 'lm')
    badge(d, 622, y + 40, n, c)
    text(d, (662, y + 14), t, font('Black', 46), NAVY)
    for j, line in enumerate(sub):
        text(d, (622, y + 92 + j * 46), line, font('Medium', 32), GREY)
bounce(d, 92, 1222); text(d, (122, 1222), '= ここでバウンド', font('Bold', 28), NAVY, 'lm')
text(d, (W - 70, 1222), 'テニス経験者が忘れやすいルール', font('Bold', 28), CORAL, 'rm')
footer(d, NAVY, 4)
im.save(f'{OUT}/04.png')

# 5 キッチン
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
head(d, 'RULE 3', 'キッチンではボレー禁止', 'ネットから約2.1mのゾーン')
cx, cy, cw, ch = 110, 410, 300, 660
k, mid = court(d, cx, cy, cw, ch, kitchen=CORAL)
text(d, (cx + cw / 2, mid + k / 2 + 4), 'キッチン', font('Black', 36), WHITE, 'mm')
text(d, (cx + cw / 2, mid - k / 2 + 4), 'キッチン', font('Black', 36), WHITE, 'mm')
y = 470
for mark, t, sub, c in [('×', '中に立ってボレー', 'ラインを踏んでいてもNG', CORAL),
                        ('×', '打った勢いで入る', 'ボレーの後の一歩に注意', CORAL),
                        ('○', 'ワンバウンドなら', '中に入って打ってOK', KIT)]:
    d.ellipse((500, y, 556, y + 56), fill=c)
    text(d, (528, y + 28), mark, font('Black', 36), WHITE, 'mm')
    text(d, (580, y), t, font('Black', 44), NAVY)
    text(d, (580, y + 64), sub, font('Medium', 30), GREY)
    y += 190
text(d, (110, 1160), '正式名は「ノンボレーゾーン」', font('Bold', 34), GREY)
footer(d, NAVY, 5)
im.save(f'{OUT}/05.png')

# 6 点数
im = Image.new('RGB', (W, H), NAVY); d = ImageDraw.Draw(im)
head(d, 'RULE 4', '点が入るのはサーブ側だけ', None, dark=True)
text(d, (W // 2, 560), '11', font('Black', 300), SUN, 'mm')
text(d, (W // 2, 760), '点先取（2点差がつくまで続く）', font('Bold', 46), WHITE, 'mm')
d.rounded_rectangle((90, 880, W - 90, 1150), radius=32, fill=(28, 72, 108))
text(d, (140, 920), 'サーブ側がラリーに勝つ', font('Bold', 40), WHITE)
text(d, (W - 140, 920), '＋1点', font('Black', 40), SUN, 'ra')
text(d, (140, 1020), 'レシーブ側がラリーに勝つ', font('Bold', 40), WHITE)
text(d, (W - 140, 1020), 'サーブ権が移る', font('Black', 40), (170, 205, 230), 'ra')
footer(d, (170, 205, 230), 6)
im.save(f'{OUT}/06.png')

# 7 スコアのコール（例で見せる → サーバー番号の意味 → 試合開始の例外）
im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
head(d, 'RULE 5', 'スコアは3つの数字で言う', 'サーブする人が、打つ前に声に出します')
d.rounded_rectangle((70, 390, W - 70, 720), radius=32, fill=WHITE)
pill(d, 100, 415, '例', font('Black', 28), CORAL, WHITE)
nums = [('5', '自分たちの点', NAVY), ('3', '相手の点', NAVY), ('1', 'サーブ1人目', CORAL)]
for i, (n, lab, c) in enumerate(nums):
    x = 230 + i * 310
    text(d, (x, 560), n, font('Black', 170), c, 'mm')
    text(d, (x, 680), lab, font('Bold', 32), INK, 'mm')
    if i < 2: text(d, (x + 155, 555), '-', font('Black', 90), GREY, 'mm')
text(d, (70, 790), 'ダブルスは、ペアの2人ともサーブします', font('Black', 42), NAVY)
bw, by, bh = 250, 870, 120
boxes = [('1人目が', 'サーブ', CORAL), ('2人目が', 'サーブ', CORAL), ('相手チーム', 'へ交代', GREY)]
for i, (l1, l2, c) in enumerate(boxes):
    x = 75 + i * (bw + 85)
    d.rounded_rectangle((x, by, x + bw, by + bh), radius=24, fill=c)
    text(d, (x + bw / 2, by + 40), l1, font('Black', 34), WHITE, 'mm')
    text(d, (x + bw / 2, by + 84), l2, font('Black', 34), WHITE, 'mm')
    if i < 2:
        ax = x + bw + 12
        arrow(d, (ax, by + bh / 2), (ax + 61, by + bh / 2), NAVY, width=6, head_len=22)
        text(d, (ax + 36, by + bh + 30), '負けたら', font('Bold', 26), GREY, 'mm')
d.rounded_rectangle((70, 1070, W - 70, 1210), radius=24, fill=(255, 241, 230))
text(d, (100, 1098), '試合開始のコールだけは「0-0-2」', font('Black', 36), CORAL)
text(d, (100, 1152), '最初のチームはサーブが1人分だけなので「2人目」から', font('Medium', 30), INK)
footer(d, NAVY, 7)
im.save(f'{OUT}/07.png')

# 8 まとめ・送客
im = Image.new('RGB', (W, H), CORAL); d = ImageDraw.Draw(im)
text(d, (W // 2, 200), '今日覚えるのはこの3つ', font('Black', 62), WHITE, 'mm')
y = 300
for s in ['サーブは下から、対角線へ', '最初の2回はワンバウンド', 'キッチンではボレーしない']:
    d.rounded_rectangle((110, y, W - 110, y + 110), radius=55, fill=WHITE)
    text(d, (W // 2, y + 55), s, font('Black', 46), CORAL, 'mm')
    y += 140
text(d, (W // 2, 820), 'もっと詳しい解説と、', font('Bold', 44), WHITE, 'mm')
text(d, (W // 2, 885), '近くのコート探しはプロフィールから', font('Bold', 44), WHITE, 'mm')
text(d, (W // 2, 990), 'pickleball-tokyo.com', font('Black', 52), WHITE, 'mm')
text(d, (W // 2, 1110), 'わからないルールは、コメントで質問してね', font('Medium', 36), (255, 230, 220), 'mm')
text(d, (W // 2, 1230), '@pickleballtokyo', font('Black', 44), WHITE, 'mm')
im.save(f'{OUT}/08.png')

sheet = Image.new('RGB', (4 * 270 + 50, 2 * 338 + 30), (200, 200, 200))
for i in range(8):
    t = Image.open(f'{OUT}/0{i+1}.png').resize((270, 338))
    sheet.paste(t, (10 + (i % 4) * 280, 10 + (i // 4) * 348))
sheet.save('/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/rules_sheet.png')
