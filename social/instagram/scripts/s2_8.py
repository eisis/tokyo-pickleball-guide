exec(open('/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/us2_base.py').read())
def person(d, x, y, s, c):
    r = 34 * s
    d.ellipse((x - r, y - r - 70 * s, x + r, y + r - 70 * s), fill=c)
    d.rounded_rectangle((x - 58 * s, y - 20 * s, x + 58 * s, y + 90 * s), radius=int(50 * s), fill=c)
def usa(d): pill(d, 70, 120, 'IN USA', font('Black', 30), CORAL, WHITE)

# ---------- 2 プレーする人 ----------
im, d = new(NAVY); usa(d)
T(d, (70, 220), 'アメリカでプレーする人', font('Black', 56), WHITE)
T(d, (60, 300), '約2,400万人', font('Black', 160), SUN)
for i in range(5):
    person(d, 170 + i * 185, 820, 1.25, SUN if i == 2 else NAVY2)
T(d, (W // 2, 1010), '日本人の5人に1人と同じ数', font('Black', 50), WHITE, 'mm')
footer(d, 2, note='2025年の数字。出典：米国スポーツ・フィットネス産業協会（SFIA）2026年レポート')
im.save(f'{OUT}/02.png')

# ---------- 3 プロリーグ（襟付きのポロシャツ） ----------
im, d = new(NAVY); usa(d)
T(d, (70, 210), 'プロリーグまである', font('Black', 92), WHITE)
T(d, (72, 345), '都市ごとのチームが、', font('Bold', 44), PALE)
T(d, (72, 405), 'ドラフトで選手を取り合う', font('Bold', 44), PALE)
def polo(cx, cy, body, accent):
    s = 1.0
    # 袖
    d.polygon([(cx - 92, cy - 120), (cx - 150, cy - 60), (cx - 118, cy - 10), (cx - 86, cy - 40)], fill=body)
    d.polygon([(cx + 92, cy - 120), (cx + 150, cy - 60), (cx + 118, cy - 10), (cx + 86, cy - 40)], fill=body)
    d.line([(cx - 150, cy - 60), (cx - 118, cy - 10)], fill=accent, width=10)
    d.line([(cx + 150, cy - 60), (cx + 118, cy - 10)], fill=accent, width=10)
    # 胴
    d.rounded_rectangle((cx - 96, cy - 130, cx + 96, cy + 150), radius=18, fill=body)
    # 襟
    d.polygon([(cx - 46, cy - 138), (cx, cy - 92), (cx - 18, cy - 60), (cx - 64, cy - 110)], fill=WHITE)
    d.polygon([(cx + 46, cy - 138), (cx, cy - 92), (cx + 18, cy - 60), (cx + 64, cy - 110)], fill=WHITE)
    d.line([(cx - 46, cy - 132), (cx + 46, cy - 132)], fill=WHITE, width=8)
    # 前立てとボタン
    d.rectangle((cx - 8, cy - 92, cx + 8, cy - 10), fill=accent)
    for by in (cy - 74, cy - 46, cy - 20):
        d.ellipse((cx - 5, by - 5, cx + 5, by + 5), fill=WHITE)
    # 裾のライン
    d.rectangle((cx - 96, cy + 120, cx + 96, cy + 132), fill=accent)
    # 胸のボールのワッペン
    d.ellipse((cx + 34, cy - 50, cx + 70, cy - 14), fill=accent)
for i, (b, a) in enumerate([(CORAL, SUN), (SEA, WHITE), (SUN, CORAL)]):
    polo(220 + i * 320, 770, b, a)
T(d, (W // 2, 1030), 'メジャーリーグ・ピックルボール（MLP）', font('Black', 42), SUN, 'mm')
footer(d, 3)
im.save(f'{OUT}/03.png')

# ---------- 4 賞金 ----------
im, d = new(NAVY); usa(d)
T(d, (70, 215), 'アメリカのプロ大会の賞金', font('Black', 60), WHITE)
T(d, (72, 305), '1年間で合計', font('Bold', 44), PALE)
T(d, (56, 360), '約50億円', font('Black', 190), SUN)
d.rounded_rectangle((70, 700, W - 70, 1000), radius=36, fill=NAVY2)
T(d, (110, 740), 'トップ選手は10代で', font('Bold', 44), WHITE)
T(d, (104, 800), '年収4億円以上', font('Black', 110), CORAL)
footer(d, 4, note='2026年見込み。プロツアーとプロリーグ、年間50以上の大会の賞金の合計（3,300万ドル超）\n年収は2024年のアナ・リー・ウォーターズ選手の推定（300万ドル以上）。1ドル150円で換算')
im.save(f'{OUT}/04.png')

# ---------- 5 テレビ（中継映像のような、線の入ったピックルボールコート） ----------
im, d = new(NAVY); usa(d)
T(d, (70, 210), '全米のテレビで中継', font('Black', 88), WHITE)
# 画面の枠
sx, sy, sw, sh = 70, 360, 940, 560
d.rounded_rectangle((sx, sy, sx + sw, sy + sh), radius=28, fill=(18, 92, 70))
# 中継カメラから見たコート（奥が狭い台形）。実寸 6.1m × 13.4m、キッチン 2.13m
def lerp(a, b, t): return (a[0] + (b[0] - a[0]) * t, a[1] + (b[1] - a[1]) * t)
nearL, nearR = (sx + 120, sy + sh - 40), (sx + sw - 120, sy + sh - 40)
farL, farR = (sx + 300, sy + 70), (sx + sw - 300, sy + 70)
def at(u, v):  # u: 横 0..1, v: 奥行き 0(手前)..1(奥)。奥ほど縮む
    vv = v ** 0.85
    L = lerp(nearL, farL, vv); Rr = lerp(nearR, farR, vv)
    return lerp(L, Rr, u)
quad = lambda v1, v2: [at(0, v1), at(1, v1), at(1, v2), at(0, v2)]
d.polygon(quad(0, 1), fill=(31, 127, 184))
k = 2.13 / 13.41
d.polygon(quad(0.5 - k, 0.5 + k), fill=KIT)
LW = 5
for v in (0, 1, 0.5 - k, 0.5 + k):
    d.line([at(0, v), at(1, v)], fill=WHITE, width=LW)
d.line([at(0, 0), at(0, 1)], fill=WHITE, width=LW); d.line([at(1, 0), at(1, 1)], fill=WHITE, width=LW)
d.line([at(0.5, 0), at(0.5, 0.5 - k)], fill=WHITE, width=LW); d.line([at(0.5, 0.5 + k), at(0.5, 1)], fill=WHITE, width=LW)
# ネット
nl, nr = at(-0.04, 0.5), at(1.04, 0.5)
d.polygon([nl, nr, (nr[0], nr[1] - 44), (nl[0], nl[1] - 44)], fill=(20, 30, 40))
for i in range(1, 24):
    x = nl[0] + (nr[0] - nl[0]) * i / 24
    d.line([(x, nl[1] - 44), (x, nl[1])], fill=(70, 90, 110), width=1)
d.line([(nl[0], nl[1] - 44), (nr[0], nr[1] - 44)], fill=WHITE, width=6)
# 選手（小さなピクトグラム）とボール
def mini(x, y, s, c):
    d.ellipse((x - 11 * s, y - 70 * s, x + 11 * s, y - 48 * s), fill=c)
    taper(d, (x, y - 44 * s), (x, y - 12 * s), 12 * s, 10 * s, c)
    taper(d, (x, y - 12 * s), (x - 10 * s, y + 10 * s), 7 * s, 6 * s, c)
    taper(d, (x, y - 12 * s), (x + 10 * s, y + 10 * s), 7 * s, 6 * s, c)
# 選手（小さく、構えた姿勢で4人。手前のチームは背中、奥のチームは正面）
SKIN_ = (196, 140, 104); HAIR_ = (40, 30, 26)
def player(fx, fy, h, shirt, shorts, side=1, front=False):
    lw = max(4, int(h * 0.09))
    hipL, hipR = (fx - h * 0.07, fy - h * 0.44), (fx + h * 0.07, fy - h * 0.44)
    # 脚（少し開いて構える）
    d.line([hipL, (fx - h * 0.16, fy - h * 0.22), (fx - h * 0.2, fy)], fill=SKIN_, width=lw, joint='curve')
    d.line([hipR, (fx + h * 0.16, fy - h * 0.22), (fx + h * 0.2, fy)], fill=SKIN_, width=lw, joint='curve')
    for sx in (-1, 1):
        d.ellipse((fx + sx * h * 0.2 - h * 0.07, fy - h * 0.035, fx + sx * h * 0.2 + h * 0.07, fy + h * 0.035), fill=WHITE)
    # ショーツと上半身（シャツは肩幅を出して人の形に）
    d.polygon([(fx - h * 0.15, fy - h * 0.56), (fx + h * 0.15, fy - h * 0.56), (fx + h * 0.17, fy - h * 0.4), (fx - h * 0.17, fy - h * 0.4)], fill=shorts)
    d.rounded_rectangle((fx - h * 0.17, fy - h * 0.86, fx + h * 0.17, fy - h * 0.54), radius=int(h * 0.06), fill=shirt)
    # 腕：ラケット側は横へ伸ばし、反対はひじを曲げる
    sh_r, sh_l = (fx + side * h * 0.15, fy - h * 0.8), (fx - side * h * 0.15, fy - h * 0.8)
    hand = (fx + side * h * 0.42, fy - h * 0.66)
    d.line([sh_r, (fx + side * h * 0.3, fy - h * 0.7), hand], fill=SKIN_, width=max(3, int(lw * 0.8)), joint='curve')
    d.line([sh_l, (fx - side * h * 0.27, fy - h * 0.66), (fx - side * h * 0.14, fy - h * 0.6)], fill=SKIN_, width=max(3, int(lw * 0.8)), joint='curve')
    # パドル
    px, py = hand[0] + side * h * 0.08, hand[1] - h * 0.1
    d.line([hand, (px, py)], fill=NAVY, width=max(3, int(h * 0.04)))
    d.rounded_rectangle((px - h * 0.08, py - h * 0.2, px + h * 0.08, py), radius=int(h * 0.05), fill=SUN if shirt != SUN else CORAL)
    # 首と頭（顔は描かず、髪で前後を表す）
    d.rectangle((fx - h * 0.035, fy - h * 0.9, fx + h * 0.035, fy - h * 0.84), fill=SKIN_)
    r = h * 0.1; hx, hy = fx, fy - h * 0.98
    d.ellipse((hx - r, hy - r, hx + r, hy + r), fill=SKIN_ if front else HAIR_)
    d.chord((hx - r, hy - r, hx + r, hy + r * 0.2), 180, 360, fill=HAIR_)
for (u, v, h, sh_, so_, sd, fr) in [(0.3, 0.86, 70, SUN, NAVY, -1, True), (0.7, 0.88, 70, SUN, NAVY, 1, True),
                                  (0.32, 0.1, 120, CORAL, WHITE, 1, False), (0.7, 0.14, 120, CORAL, WHITE, -1, False)]:
    p = at(u, v); player(p[0], p[1], h, sh_, so_, sd, fr)
b = at(0.56, 0.62); d.ellipse((b[0] - 14, b[1] - 5, b[0] + 14, b[1] + 5), fill=(20, 80, 120))
d.ellipse((b[0] - 12, b[1] - 62, b[0] + 12, b[1] - 38), fill=SUN)
# LIVE とスコア表示
d.rounded_rectangle((sx + 30, sy + 26, sx + 150, sy + 70), radius=10, fill=CORAL)
T(d, (sx + 90, sy + 48), 'LIVE', font('Black', 28), WHITE, 'mm')
d.rounded_rectangle((sx + sw - 230, sy + sh - 110, sx + sw - 30, sy + sh - 26), radius=12, fill=(10, 30, 50))
T(d, (sx + sw - 214, sy + sh - 90), 'TEAM A   8', font('Bold', 24), WHITE)
T(d, (sx + sw - 214, sy + sh - 58), 'TEAM B   6', font('Bold', 24), SUN)
T(d, (W // 2, 990), 'FOX Sports ・ ESPN ・ CBS', font('Black', 60), SUN, 'mm')
T(d, (W // 2, 1078), '「やる」だけじゃなく「観る」スポーツに', font('Bold', 40), WHITE, 'mm')
footer(d, 5)
im.save(f'{OUT}/05.png')

# ---------- 6 ハリウッドのスター（スポットライト・ヤシの木・レッドカーペット） ----------
im, d = new(DEEP)
# スポットライト（白い光の筋）
g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); gd = ImageDraw.Draw(g)
for bx, tx in [(260, 0), (820, 1080), (540, 560)]:
    gd.polygon([(bx - 24, 1180), (bx + 24, 1180), (tx + 200, 0), (tx - 200, 0)], fill=(255, 255, 255, 34))
g = g.filter(ImageFilter.GaussianBlur(14)); im.paste(g, (0, 0), g); d = ImageDraw.Draw(im)
# ヤシの木（葉は垂れ下がる形）
def leaf(top, ang, L, droop, c, w0=26):
    pts_up, pts_dn = [], []
    for i in range(13):
        t = i / 12
        x = top[0] + math.cos(math.radians(ang)) * L * t
        y = top[1] + math.sin(math.radians(ang)) * L * t + droop * t * t
        wd = w0 * math.sin(math.pi * min(t * 1.1, 1)) + 2
        pts_up.append((x, y - wd / 2)); pts_dn.append((x, y + wd / 2))
    d.polygon(pts_up + pts_dn[::-1], fill=c)
def palm(x, y, h, c, lean=1):
    top = (x + 40 * lean, y - h)
    for i in range(10):
        t0, t1 = i / 10, (i + 1) / 10
        p0 = (x + 40 * lean * t0 ** 1.5, y - h * t0); p1 = (x + 40 * lean * t1 ** 1.5, y - h * t1)
        d.line([p0, p1], fill=c, width=int(26 - 10 * t0))
    for ang, L, dr in [(-170, 190, 120), (-140, 170, 110), (-100, 120, 70), (-60, 160, 100), (-20, 190, 120), (10, 170, 140), (190, 160, 140)]:
        leaf(top, ang, L, dr, c)
palm(70, 1190, 460, (40, 92, 130), 1); palm(1010, 1190, 420, (40, 92, 130), -1)
# レッドカーペット
d.polygon([(W // 2 - 110, 1050), (W // 2 + 110, 1050), (W // 2 + 330, H), (W // 2 - 330, H)], fill=(196, 34, 56))
for sx_ in (-1, 1):
    for k in range(2):
        px = W // 2 + sx_ * (150 + k * 70); py = 1090 + k * 66
        d.rectangle((px - 5, py - 60, px + 5, py), fill=SUN); d.ellipse((px - 12, py - 72, px + 12, py - 48), fill=SUN)
pill(d, 70, 120, 'IN USA', font('Black', 30), CORAL, WHITE)
T(d, (70, 205), 'あの世界的スターも、', font('Black', 76), WHITE)
T(d, (70, 300), 'プレーしてる。', font('Black', 104), SUN)
def star(cx, cy, r, c):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=c)
y = 470
for name, role in [('エマ・ワトソン', '俳優'), ('ビリー・アイリッシュ', '歌手'), ('アンジェリーナ・ジョリー', '俳優')]:
    d.rounded_rectangle((110, y, W - 110, y + 140), radius=70, fill=WHITE)
    star(176, y + 70, 28, SUN)
    T(d, (224, y + 70), name, font('Black', 50), NAVY, 'lm')
    T(d, (W - 150, y + 70), role, font('Bold', 28), (120, 140, 160), 'rm')
    y += 164
footer(d, 6, c=(230, 230, 240), note='それぞれピックルボールの大会に出場。エマ・ワトソンは2022年の米CBSの特番、\nビリー・アイリッシュとアンジェリーナ・ジョリーは2026年6月のチャリティー大会')
im.save(f'{OUT}/06.png')

# ---------- 7 そして東京でも（東京タワーと、実際にコートがある街） ----------
SKY1, SKY2 = (31, 127, 184), (120, 190, 225)
im = Image.new('RGB', (W, H)); d = ImageDraw.Draw(im)
for yy in range(H):
    t = yy / H; d.line([(0, yy), (W, yy)], fill=tuple(int(SKY1[i] + (SKY2[i] - SKY1[i]) * t) for i in range(3)))
T(d, (70, 170), 'そして、', font('Black', 70), WHITE)
T(d, (70, 260), '東京でも。', font('Black', 110), SUN)
T(d, (72, 420), '新しいコートが続々オープン中', font('Black', 50), WHITE)
# ビル群
base = 1180
import random; random.seed(3)
x = 0
while x < W:
    w_ = random.randint(60, 120); h_ = random.randint(120, 300)
    d.rectangle((x, base - h_, x + w_, base), fill=(24, 92, 140))
    for wy in range(base - h_ + 20, base - 20, 34):
        for wx in range(x + 14, x + w_ - 14, 26):
            if random.random() < 0.5: d.rectangle((wx, wy, wx + 10, wy + 14), fill=(120, 180, 215))
    x += w_ + 6
# 東京タワー（赤白の鉄塔）
tx, top, foot = 300, 690, base
def tw(y, hw): return [(tx - hw, y), (tx + hw, y)]
levels = [(top, 4), (top + 90, 13), (top + 190, 27), (top + 240, 36), (top + 350, 68), (foot, 136)]
for (y1, w1), (y2, w2) in zip(levels, levels[1:]):
    seg = int((y2 - y1) / 40) or 1
    for j in range(seg):
        ya = y1 + (y2 - y1) * j / seg; yb = y1 + (y2 - y1) * (j + 1) / seg
        wa = w1 + (w2 - w1) * j / seg; wb = w1 + (w2 - w1) * (j + 1) / seg
        col = CORAL if j % 2 == 0 else WHITE
        d.polygon([(tx - wa, ya), (tx + wa, ya), (tx + wb, yb), (tx - wb, yb)], fill=col)
d.line([(tx, top - 70), (tx, top)], fill=WHITE, width=6)
d.rounded_rectangle((tx - 44, top + 214, tx + 44, top + 246), radius=8, fill=(240, 240, 240))
d.rounded_rectangle((tx - 24, top + 112, tx + 24, top + 132), radius=6, fill=(240, 240, 240))
d.polygon([(tx - 150, foot), (tx - 90, foot - 120), (tx - 60, foot)], fill=(24, 92, 140))
d.polygon([(tx + 150, foot), (tx + 90, foot - 120), (tx + 60, foot)], fill=(24, 92, 140))
d.rectangle((0, base, W, H), fill=NAVY)
# 実際に掲載コートがある街のピン
def pin(cx, cy, label):
    d.ellipse((cx - 38, cy - 38, cx + 38, cy + 38), fill=CORAL)
    d.polygon([(cx - 27, cy + 24), (cx + 27, cy + 24), (cx, cy + 82)], fill=CORAL)
    d.ellipse((cx - 15, cy - 15, cx + 15, cy + 15), fill=WHITE)
    f = font('Black', 40); w_ = d.textlength(label, font=f)
    d.rounded_rectangle((cx - w_ / 2 - 22, cy - 122, cx + w_ / 2 + 22, cy - 56), radius=33, fill=WHITE)
    d.polygon([(cx - 12, cy - 58), (cx + 12, cy - 58), (cx, cy - 44)], fill=WHITE)
    T(d, (cx, cy - 89), label, f, NAVY, 'mm')
f_ = font('Black', 40); lw = d.textlength('東京タワー', font=f_)
d.rounded_rectangle((tx - lw / 2 - 22, 548, tx + lw / 2 + 22, 614), radius=33, fill=WHITE)
d.polygon([(tx - 12, 612), (tx + 12, 612), (tx, 628)], fill=WHITE)
T(d, (tx, 581), '東京タワー', f_, NAVY, 'mm')
for (cx, cy, lab) in [(560, 690, '池袋'), (860, 650, '豊洲'), (700, 900, '銀座'), (950, 960, '幕張')]:
    pin(cx, cy, lab)
footer(d, 7, c=(170, 205, 230))
im.save(f'{OUT}/07.png')

# ---------- 8 行動：アメリカ → 東京 → あなた ----------
im, d = new(CORAL)
T(d, (W // 2, 210), '一緒に始めよう、', font('Black', 84), WHITE, 'mm')
T(d, (W // 2, 345), 'ピックルボール。', font('Black', 112), SUN, 'mm')
T(d, (W // 2, 480), '友達を誘って、この週末から。', font('Bold', 44), WHITE, 'mm')
for i, (a_, b_) in enumerate([('始め方は', '前回の投稿をチェック'), ('コート探しは', 'プロフィールのリンクから')]):
    y = 590 + i * 180
    d.rounded_rectangle((120, y, W - 120, y + 150), radius=75, fill=WHITE)
    T(d, (W // 2, y + 48), a_, font('Bold', 32), (190, 110, 95), 'mm')
    T(d, (W // 2, y + 102), b_, font('Black', 46), CORAL, 'mm')
T(d, (W // 2, 1010), 'pickleball-tokyo.com', font('Black', 50), WHITE, 'mm')
d.line([(W // 2 - 60, 1090), (W // 2 + 60, 1090)], fill=(255, 190, 170), width=3)
T(d, (W // 2, 1150), '@pickleballtokyo', font('Bold', 36), WHITE, 'mm')
T(d, (W - 70, H - 60), '8/8', font('Medium', 24), (255, 210, 195), 'rs')
im.save(f'{OUT}/08.png')

sheet = Image.new('RGB', (4 * 270 + 50, 2 * 338 + 30), (200, 200, 200))
for i in range(N):
    t = Image.open(f'{OUT}/0{i+1}.png').resize((270, 338))
    sheet.paste(t, (10 + (i % 4) * 280, 10 + (i // 4) * 348))
sheet.save(SP + 'usa_sheet.png')
