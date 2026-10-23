exec(open('/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/us2_base.py').read())
im, d = new(NAVY)
def star(cx, cy, r, c):
    pts = []
    for i in range(10):
        a = math.radians(-90 + i * 36); rr = r if i % 2 == 0 else r * 0.45
        pts.append((cx + rr * math.cos(a), cy + rr * math.sin(a)))
    d.polygon(pts, fill=c)
# 下：星条旗のようなストライプの帯（少し傾ける）
band = Image.new('RGBA', (1500, 420), (0, 0, 0, 0)); bd = ImageDraw.Draw(band)
for i in range(7):
    bd.rectangle((0, i * 60, 1500, i * 60 + 60), fill=CORAL if i % 2 == 0 else WHITE)
band = band.rotate(14, expand=True, resample=Image.BICUBIC)
im.paste(band, (-260, 860), band); d = ImageDraw.Draw(im)
# 右上：整列した星
for r_ in range(4):
    for c_ in range(5):
        star(700 + c_ * 66 + (33 if r_ % 2 else 0), 120 + r_ * 62, 13, (70, 112, 150))
# パドル（全体が見える大きさ）と光るボール
pad = Image.new('RGBA', (420, 700), (0, 0, 0, 0)); pd = ImageDraw.Draw(pad)
pd.rounded_rectangle((30, 20, 390, 470), radius=90, fill=SUN, outline=WHITE, width=12)
pd.rounded_rectangle((64, 54, 356, 436), radius=70, outline=(240, 190, 90), width=6)
pd.rounded_rectangle((168, 456, 252, 690), radius=24, fill=NAVY2, outline=WHITE, width=6)
pad = pad.resize((300, 500), Image.LANCZOS).rotate(-24, expand=True, resample=Image.BICUBIC)
im.paste(pad, (590, 520), pad); d = ImageDraw.Draw(im)
for k, a in enumerate([220, 140, 80]):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.line([(560 - k * 10, 640 + k * 34), (330 - k * 30, 700 + k * 44)], fill=(255, 255, 255, a), width=10 - k * 2)
    im.paste(ov, (0, 0), ov)
d = glow_ball(im, 590, 616, 42)
y = 110
for line, c in [('アメリカで、', WHITE), ('ピックルボールが', WHITE), ('とんでもない', SUN), ('ことになってる', SUN)]:
    T(d, (64, y), line, font('Black', 82), c); y += 96
d.rounded_rectangle((60, 1240, 250, 1300), radius=30, fill=NAVY)
T(d, (80, 1284), 'スワイプ →', font('Bold', 30), WHITE, 'ls')
im.save(OUT + '/01.png')
