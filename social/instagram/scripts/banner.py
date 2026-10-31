# 記事一覧のバナー（16:9・1600×900）を、Instagramの表紙画像から作る
# 左に見出し、右に表紙の絵の部分を切り抜いて置く。python3 banner.py [記事ID...]
import os, sys, base64, io
from PIL import Image
from playwright.sync_api import sync_playwright

ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../..'))
IMG = os.path.join(ROOT, 'public/images/posts')
W, H = 1600, 900
NAVY = '#0e3452'; SUN = '#ffd678'; CORAL = '#ff6b4a'; WHITE = '#ffffff'; PURPLE = '#5b4bc4'

# 全部同じ型：見出しは88pxで1行8文字まで・3行まで、右の絵は同じ枠（680×680）に収める
# 表紙のファイル、切り抜く範囲（元画像の座標）、背景色（Noneなら表紙の左上の色）、文字色、札、見出し、ひとこと
B = {
  'anna-leigh-waters': dict(src='anna-leigh-waters.jpg', crop=(0, 150, 1080, 740), full=True,
      bg='#071a2c', fg=WHITE, tags=[('シングルス', '#D9FF3D', NAVY), ('ダブルス', '#D9FF3D', NAVY), ('混合ダブルス', '#D9FF3D', NAVY)],
      lines=[[('いま、全部', WHITE)], [('世界1位', '#D9FF3D')]],
      sub='アンナ・リー・ウォーターズの9年'),
  'dink-strategy': dict(src='dink-strategy.jpg', crop=(0, 660, 1080, 1250), full=True,
      bg='#0a1d2e', fg=WHITE, tags=[('ちょっと戦術', SUN, NAVY)],
      lines=[[('強く打った方が', WHITE)], [('負ける？', SUN)]],
      sub='ネット際で「ふわっ」と打つ理由'),
  'doubles-scoring': dict(src='doubles-scoring.png', crop=(60, 640, 1020, 1240),
      bg='#ff6b4a', fg=WHITE, tags=[('保存版', WHITE, CORAL), ('ダブルス', NAVY, WHITE)],
      lines=[[('「0-0-2」', NAVY)], [('って、何の数字？', WHITE)]],
      sub='点数と、立つ場所が絵でわかる'),
  'after-work-courts': dict(src='after-work-courts.png', crop=(56, 680, 1024, 1240),
      bg=None, fg=WHITE, tags=[('保存版', CORAL, WHITE)],
      lines=[[('仕事帰りに', WHITE), ('行ける', SUN)], [('コート5選', WHITE)]],
      sub='夜遅くまで開いている駅近の屋内'),
  'asics-pickleball-connect': dict(src='asics-pickleball-connect.png', crop=(60, 520, 1020, 1000),
      bg=None, fg=NAVY, tags=[('10/31 OPEN', CORAL, WHITE), ('12/27まで', NAVY, WHITE)],
      lines=[[('丸の内に、', NAVY)], [('ASICS', PURPLE), ('の', NAVY)], [('コート', NAVY)]],
      sub='ASICS PICKLEBALL CONNECT'),
  'what-to-wear': dict(src='what-to-wear.png', crop=(66, 636, 1028, 1236),
      bg=None, fg=NAVY, tags=[('保存版', CORAL, WHITE), ('はじめての人へ', NAVY, WHITE)],
      lines=[[('何、着ていく？', NAVY)], [('何、持っていく？', CORAL)]],
      sub='ピックルボールの服装と持ち物'),
  'beginner-friendly': dict(src='beginner-friendly.png', crop=(300, 760, 1080, 1210), noframe=True,
      bg=None, fg=WHITE, tags=[('はじめての人へ', CORAL, WHITE)],
      lines=[[('運動が苦手でも、', WHITE)], [('ピックルボール', SUN)], [('ってできる？', WHITE)]],
      sub='できる理由が、4つあります'),
  'weekend-2026-10-25': dict(src='weekend-2026-10-25.png', crop=(60, 600, 1080, 1170), noframe=True,
      bg=None, fg=WHITE, tags=[('10/25（日）がねらい目', CORAL, WHITE)],
      lines=[[('今週末、', WHITE)], [('ピックルボール', SUN)], [('やってみない？', WHITE)]],
      sub='東京近郊で、日曜に行ける体験会'),
  'usa-pickleball-boom': dict(src='usa-pickleball-boom.png', crop=(830, 20, 1200, 630), noframe=True,
      bg=None, fg=WHITE, tags=[('アメリカのいま', CORAL, WHITE)],
      lines=[[('アメリカで', WHITE)], [('大ブーム', SUN), ('の', WHITE)], [('ピックルボール', WHITE)]],
      sub='プレー人口・賞金・TV中継・セレブ'),
  'start-with-friends': dict(src='start-with-friends.png', crop=(740, 190, 1170, 570), noframe=True, nomask=True, erase=(740, 190, 920, 330),
      bg=None, fg=WHITE, tags=[('はじめての人へ', CORAL, WHITE)],
      lines=[[('友達と', WHITE)], [('始めるなら', WHITE)], [('この順番で', SUN)]],
      sub='道具がなくても、今週末から'),
}
PAD = []


def uri(im, fmt='PNG'):
    b = io.BytesIO(); im.save(b, fmt); return f'data:image/{fmt.lower()};base64,' + base64.b64encode(b.getvalue()).decode()


def tw(s):  # だいたいの文字幅（全角1・半角0.58）
    return sum(0.58 if ord(ch) < 0x2000 else 1 for ch in s)


def html(k, c):
    src = Image.open(os.path.join(IMG, c['src'])).convert('RGB')
    bg = c['bg'] or '#%02x%02x%02x' % src.getpixel((8, 8))
    if c.get('erase'):
        from PIL import ImageDraw
        ImageDraw.Draw(src).rectangle(c['erase'], fill=src.getpixel((c['crop'][0] + 4, c['crop'][1] + 4)))
    art = src.crop(c['crop'])
    # どの絵も同じくらいの面積に見えるように大きさをそろえる
    k = (680 * 470 / (art.width * art.height)) ** .5
    k = min(k, 720 / art.width, 640 / art.height)
    art = art.resize((round(art.width * k), round(art.height * k)), Image.LANCZOS)
    size = 88
    assert all(tw(''.join(t for t, _ in l)) <= 8.2 for l in c['lines']), k
    lines = ''.join('<div class="l">' + ''.join(f'<span style="color:{col}">{s}</span>' for s, col in l) + '</div>' for l in c['lines'])
    tags = ''.join(f'<span class="tag" style="background:{b};color:{f}">{t}</span>' for t, b, f in c['tags'])
    kick = f'<div class="kick">{c["kicker"]}</div>' if c.get('kicker') else ''
    if c.get('full'):
        right = f'<div class="full" style="background-image:url({uri(art, "JPEG")})"></div>'
    else:
        cls = ('art bare' + (' nomask' if c.get('nomask') else '')) if c.get('noframe') else 'art'
        right = f'<div class="{cls}"><img src="{uri(art)}"></div>'
    return f'''<html><head><style>
body{{margin:0}} *{{box-sizing:border-box}}
.b{{width:{W}px;height:{H}px;background:{bg};position:relative;overflow:hidden;font-family:'Noto Sans CJK JP';color:{c["fg"]}}}
.txt{{position:absolute;left:90px;top:0;bottom:0;width:{740}px;display:flex;flex-direction:column;justify-content:center;z-index:2}}
.tags{{display:flex;gap:14px;margin-bottom:34px}}
.tag{{font-weight:700;font-size:36px;padding:8px 28px;border-radius:40px}}
.kick{{font-weight:700;font-size:30px;letter-spacing:.04em;margin-bottom:10px}}
.l{{font-weight:900;font-size:{size}px;line-height:1.24;white-space:nowrap}}
.sub{{font-weight:700;font-size:38px;margin-top:30px;opacity:.9;white-space:nowrap}}
.foot{{position:absolute;left:80px;bottom:44px;font-weight:700;font-size:24px;letter-spacing:.06em;opacity:.8}}
.art{{position:absolute;left:840px;top:90px;width:720px;height:720px;display:flex;align-items:center;justify-content:center}}
.art img{{border-radius:28px;box-shadow:0 18px 40px rgba(0,0,0,.18)}}
.art.nomask img{{-webkit-mask-image:none!important}}\n.art.bare img{{border-radius:0;box-shadow:none;-webkit-mask-image:radial-gradient(ellipse 60% 60% at 50% 50%,#000 70%,transparent 100%)}}
.full{{position:absolute;left:700px;top:50%;transform:translateY(-50%);width:{W-700}px;aspect-ratio:1080/590;background-size:cover;background-position:center;
  -webkit-mask-image:linear-gradient(90deg,transparent 0,#000 14%),linear-gradient(180deg,transparent 0,#000 16%,#000 84%,transparent 100%);-webkit-mask-composite:source-in;mask-composite:intersect}}
</style></head><body><div class="b"><div class="txt">{kick}<div class="tags">{tags}</div>{lines}<div class="sub">{c["sub"]}</div></div>
{right}</div></body></html>'''


def pad(k):
    im = Image.open(os.path.join(IMG, k + '.png')).convert('RGB')
    w = W; h = round(im.height * W / im.width)
    im = im.resize((w, h), Image.LANCZOS)
    out = Image.new('RGB', (W, H), im.getpixel((6, 6)))
    out.paste(im, (0, H - h))                # 上側に色をのばす（下のしま模様を切らない）
    out.save(os.path.join(IMG, k + '-banner.jpg'), quality=88, optimize=True, progressive=True)


if __name__ == '__main__':
    keys = sys.argv[1:] or list(B) + PAD
    with sync_playwright() as p:
        br = p.chromium.launch(); pg = br.new_page(viewport={'width': W, 'height': H})
        for k in keys:
            if k in PAD: pad(k); continue
            pg.set_content(html(k, B[k])); pg.wait_for_timeout(100)
            pg.screenshot(path='/tmp/_b.png')
            Image.open('/tmp/_b.png').convert('RGB').save(os.path.join(IMG, k + '-banner.jpg'), quality=88, optimize=True, progressive=True)
        br.close()
    print('ok', keys)
