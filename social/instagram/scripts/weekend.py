from PIL import Image, ImageDraw, ImageFont, ImageFilter
import math, os
SP = '/tmp/claude-0/-home-claude/0fff00e8-7c5d-5fff-9e17-a4c63dd6bcc3/scratchpad/'
OUT = '/home/claude/ig-weekend'; os.makedirs(OUT, exist_ok=True)
W, H = 1080, 1350; N = 5
F = '/usr/share/fonts/opentype/noto/NotoSansCJK-%s.ttc'
def font(w, s): return ImageFont.truetype(F % w, s, index=0)
NAVY = (14, 52, 82); SEA = (31, 127, 184); CORAL = (255, 107, 74); SUN = (255, 214, 120)
WHITE = (255, 255, 255); SAND = (246, 236, 216); INK = (30, 40, 50); GREY = (100, 110, 120); KIT = (24, 168, 150)
def T(d, xy, s, f, c, a='la'): d.text(xy, s, font=f, fill=c, anchor=a)
def pill(d, x, y, s, f, bg, fg, padx=24, pady=12, anchor='l'):
    w = d.textlength(s, font=f); tw = w + padx * 2
    if anchor == 'c': x = x - tw / 2
    d.rounded_rectangle((x, y, x + tw, y + f.size + pady * 2), radius=(f.size + pady * 2) // 2, fill=bg)
    T(d, (x + padx, y + pady + f.size * 0.88), s, f, fg, 'ls')
    return x + tw
def footer(d, page, c=NAVY):
    T(d, (70, H - 60), 'PICKLEBALL TOKYO', font('Bold', 24), c, 'ls')
    T(d, (W - 70, H - 60), f'{page}/{N}  @pickleballtokyo', font('Medium', 24), c, 'rs')
def ball(d, x, y, r):
    d.ellipse((x - r, y - r, x + r, y + r), fill=(255, 226, 90), outline=(225, 175, 50), width=max(2, r // 10))
    for dx, dy in [(-.35, -.3), (.35, -.35), (0, .15), (-.4, .45), (.4, .4)]:
        rr = r * 0.15; d.ellipse((x + dx * r - rr, y + dy * r - rr, x + dx * r + rr, y + dy * r + rr), fill=(225, 175, 50))
# アイコン
def ic_cal(d, x, y, s=44, c=CORAL):
    d.rounded_rectangle((x, y + 6, x + s, y + s), radius=8, fill=WHITE, outline=c, width=5)
    d.rectangle((x, y + 6, x + s, y + 18), fill=c)
    for k in (0.3, 0.7): d.rounded_rectangle((x + s * k - 3, y, x + s * k + 3, y + 14), radius=3, fill=NAVY)
    for r in range(2):
        for q in range(3): d.rectangle((x + 8 + q * 11, y + 24 + r * 9, x + 14 + q * 11, y + 29 + r * 9), fill=c)
def ic_yen(d, x, y, s=44, c=SUN):
    d.ellipse((x, y, x + s, y + s), fill=c, outline=(225, 175, 50), width=4)
    T(d, (x + s / 2, y + s / 2 + 1), '¥', font('Black', int(s * 0.62)), NAVY, 'mm')
def ic_star(d, x, y, s=44, c=KIT):
    d.ellipse((x, y, x + s, y + s), fill=c)
    d.line([(x + s * .25, y + s * .52), (x + s * .43, y + s * .7), (x + s * .75, y + s * .32)], fill=WHITE, width=6, joint='curve')
def ic_pin(d, x, y, s=36, c=CORAL):
    d.ellipse((x, y, x + s, y + s), fill=c)
    d.polygon([(x + s * .18, y + s * .7), (x + s * .82, y + s * .7), (x + s / 2, y + s * 1.25)], fill=c)
    d.ellipse((x + s * .32, y + s * .32, x + s * .68, y + s * .68), fill=WHITE)

# ---------- 1 表紙 ----------
im = Image.new('RGB', (W, H), SEA); d = ImageDraw.Draw(im)
pill(d, 70, 110, '土曜は雨予報。日曜がねらい目！', font('Black', 30), CORAL, WHITE)
T(d, (64, 200), '今週末、', font('Black', 92), WHITE)
T(d, (60, 312), 'ピックルボール', font('Black', 118), SUN)
T(d, (64, 456), 'やってみない？', font('Black', 92), WHITE)
# 日めくりカレンダー2枚
for i, (m, day, wd, col, htxt, wdc) in enumerate([('OCT', '24', 'SAT', SUN, NAVY, (205, 145, 30)), ('OCT', '25', 'SUN', CORAL, WHITE, CORAL)]):
    x0, y0 = 100 + i * 330, 690
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.rounded_rectangle((x0 + 10, y0 + 16, x0 + 290, y0 + 376), radius=28, fill=(0, 0, 0, 60))
    sh = sh.filter(ImageFilter.GaussianBlur(10)); im.paste(sh, (0, 0), sh); d = ImageDraw.Draw(im)
    d.rounded_rectangle((x0, y0, x0 + 280, y0 + 360), radius=28, fill=WHITE)
    d.rounded_rectangle((x0, y0, x0 + 280, y0 + 90), radius=28, fill=col)
    d.rectangle((x0, y0 + 60, x0 + 280, y0 + 90), fill=col)
    T(d, (x0 + 140, y0 + 46), m, font('Black', 40), htxt, 'mm')
    T(d, (x0 + 140, y0 + 210), day, font('Black', 170), NAVY, 'mm')
    T(d, (x0 + 140, y0 + 318), wd, font('Black', 40), wdc, 'mm')
    for k in (0.3, 0.7): d.rounded_rectangle((x0 + 280 * k - 8, y0 - 18, x0 + 280 * k + 8, y0 + 22), radius=8, fill=NAVY)
# 土曜は薄くして雨雲、日曜には太陽
fade = Image.new('RGBA', (W, H), (0, 0, 0, 0)); fd = ImageDraw.Draw(fade)
fd.rounded_rectangle((100, 672, 380, 1050), radius=28, fill=(31, 127, 184, 120))
im.paste(fade, (0, 0), fade); d = ImageDraw.Draw(im)
# カードの下に、天気のマークと一言（カードやパドルと重ならない位置）
def cloud(cx, cy, k=0.6):
    for (dx, dy, r) in [(-34, 8, 30), (0, -10, 40), (38, 6, 30)]:
        d.ellipse((cx + (dx - r) * k, cy + (dy - r) * k, cx + (dx + r) * k, cy + (dy + r) * k), fill=(235, 240, 245))
    d.rounded_rectangle((cx - 64 * k, cy + 4 * k, cx + 68 * k, cy + 38 * k), radius=int(17 * k), fill=(235, 240, 245))
    for j in range(3):
        x = cx + (-34 + j * 34) * k
        d.line([(x, cy + 50 * k), (x - 8 * k, cy + 74 * k)], fill=(170, 210, 240), width=6)
def sun(cx, cy, r):
    for j in range(12):
        a = math.radians(j * 30)
        d.line([(cx + (r + 7) * math.cos(a), cy + (r + 7) * math.sin(a)), (cx + (r + 20) * math.cos(a), cy + (r + 20) * math.sin(a))], fill=SUN, width=6)
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=SUN, outline=(240, 180, 60), width=3)
# カードの中心にそろえて、マークと文字の間をあける
def label_group(cx, draw_icon, icon_w, text, color):
    f = font('Black', 34); tw = d.textlength(text, font=f); gap = 18
    x0 = cx - (icon_w + gap + tw) / 2
    draw_icon(x0 + icon_w / 2)
    T(d, (x0 + icon_w + gap, 1118), text, f, color, 'lm')
label_group(240, lambda x: cloud(x, 1110), 84, '雨予報', (200, 225, 245))
label_group(570, lambda x: sun(x, 1118, 20), 84, 'ねらい目！', SUN)
# パドルとボール（描き込み版）
exec(open(SP + 'art.py').read())
pd_ = paddle(width=230, angle=-28)
im.paste(pd_, (690, 660), pd_)
# ボールの軌跡
for k, a_ in enumerate([200, 130, 70]):
    ov = Image.new('RGBA', (W, H), (0, 0, 0, 0)); od = ImageDraw.Draw(ov)
    od.line([(800 - k * 6, 668 + k * 20), (700 - k * 16, 628 + k * 24)], fill=(255, 255, 255, a_), width=9 - k * 2)
    im.paste(ov, (0, 0), ov)
place_ball(im, 850, 680, 48)
d = ImageDraw.Draw(im)
T(d, (W - 70, H - 70), 'スワイプ →', font('Bold', 30), WHITE, 'rs')
T(d, (70, H - 70), '@pickleballtokyo', font('Bold', 28), WHITE, 'ls')
im.save(f'{OUT}/01.png')

# ---------- 2〜5 イベント（共通フォーマット） ----------
def event_slide(page, lead, lead_c, name1, name2, area, badge, badge_c, rows, note):
    im = Image.new('RGB', (W, H), SAND); d = ImageDraw.Draw(im)
    pill(d, 70, 100, '10/25（日）', font('Black', 28), NAVY, WHITE)
    T(d, (70, 190), lead, font('Black', 48), lead_c)
    T(d, (70, 290), name1, font('Black', 66), NAVY)
    T(d, (70, 376), name2, font('Black', 66), NAVY)
    ic_pin(d, 72, 482, 34)
    T(d, (124, 482), area, font('Bold', 36), GREY)
    # 情報カード
    # 中身の高さから白い箱の大きさを決める（上下の余白を同じにする）
    top, pad_ = 580, 56
    heights = [38 + 50 * len(lines) for _, lines in rows]
    gap = 40
    inner = sum(heights) + gap * (len(rows) - 1)
    bottom = top + pad_ + inner + pad_ - 10
    d.rounded_rectangle((70, top, W - 70, bottom), radius=36, fill=WHITE)
    y = top + pad_
    icons = [ic_cal, ic_yen, ic_star]
    for (label, lines), ic, h_ in zip(rows, icons, heights):
        ic(d, 110, y)
        T(d, (176, y - 2), label, font('Bold', 28), GREY)
        for j, l in enumerate(lines):
            T(d, (176, y + 38 + j * 50), l, font('Black', 40), INK)
        y += h_ + gap
    note_y = bottom + 30
    # 料金バッジ（カードの右上に重ねる）
    bx, by, r = 900, 560, 112
    sh = Image.new('RGBA', (W, H), (0, 0, 0, 0)); sd = ImageDraw.Draw(sh)
    sd.ellipse((bx - r + 6, by - r + 12, bx + r + 6, by + r + 12), fill=(0, 0, 0, 50))
    sh = sh.filter(ImageFilter.GaussianBlur(8)); im.paste(sh, (0, 0), sh); d = ImageDraw.Draw(im)
    d.ellipse((bx - r, by - r, bx + r, by + r), fill=badge_c)
    fs = 64 if len(badge) <= 2 else 46
    T(d, (bx, by), badge, font('Black', fs), WHITE if badge_c != SUN else NAVY, 'mm')
    if note:
        for j, l in enumerate(note.split('\n')):
            T(d, (74, note_y + j * 36), l, font('Medium', 26), GREY)
    footer(d, page)
    im.save(f'{OUT}/0{page}.png')

event_slide(2, '無料・予約不要で試すなら', CORAL, 'ピックルボール', 'チャレンジデイズ in 都庁', '新宿・都庁 都民広場', '無料', CORAL,
            [('日時', ['10/25（日）11:00〜15:00']), ('参加', ['予約不要。当日11時から整理券']), ('ここがいい', ['コーチが基本から教えてくれる', '30分の体験プログラム'])],
            '※雨天時は内容変更・中止の場合あり。参加は期間中1人1回まで')
event_slide(3, '安く、じっくり試すなら', KIT, 'WELL PICKLE CLUB', '体験会', '葛飾・水元', '1,100円', KIT,
            [('日時', ['10/25（日）11:20〜ほか']), ('料金', ['1人1,100円・60分']), ('ここがいい', ['定員6名の少人数で', 'ゆっくり教われる'])],
            '※要予約。予約サイトの会員登録が必要です')
event_slide(4, '道具が気になるなら', (200, 140, 30), 'ピックルボールワン銀座新橋', 'パドル試打会', '新橋（駅直結）', '1,500円', SUN,
            [('日時', ['10/25（日）']), ('料金', ['1,500円']), ('ここがいい', ['いろいろなパドルを', '実際に打ち比べられる'])],
            '※定員6名。時間は予約ページで確認してください。屋内なので天気の心配なし')

# ---------- 6 まとめ ----------
im = Image.new('RGB', (W, H), CORAL); d = ImageDraw.Draw(im)
T(d, (W // 2, 230), 'ほかにも、', font('Black', 70), WHITE, 'mm')
T(d, (W // 2, 340), '練習会や交流会が', font('Black', 84), SUN, 'mm')
T(d, (W // 2, 440), 'たくさん', font('Black', 84), SUN, 'mm')
d.rounded_rectangle((120, 560, W - 120, 720), radius=80, fill=WHITE)
T(d, (W // 2, 610), 'イベント一覧は', font('Bold', 34), (190, 110, 95), 'mm')
T(d, (W // 2, 668), 'プロフィールのリンクから', font('Black', 48), CORAL, 'mm')
T(d, (W // 2, 800), 'pickleball-tokyo.com/events', font('Black', 44), WHITE, 'mm')
d.rounded_rectangle((180, 900, W - 180, 1010), radius=55, outline=WHITE, width=4)
T(d, (W // 2, 955), '行く人は、コメントで教えてね', font('Black', 40), WHITE, 'mm')
T(d, (W // 2, 1160), '@pickleballtokyo', font('Black', 40), WHITE, 'mm')
T(d, (W - 70, H - 60), f'{N}/{N}', font('Medium', 24), (255, 210, 195), 'rs')
im.save(f'{OUT}/05.png')

sheet = Image.new('RGB', (3 * 270 + 40, 2 * 338 + 30), (200, 200, 200))
for i in range(N):
    t = Image.open(f'{OUT}/0{i+1}.png').resize((270, 338))
    sheet.paste(t, (10 + (i % 3) * 280, 10 + (i // 3) * 348))
sheet.save(SP + 'weekend_sheet.png')
