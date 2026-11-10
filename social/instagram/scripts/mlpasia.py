# 投稿16「ピックルボールのメジャーリーグ、アジアで初開催。」（MLP Asia 2026、11/13 池袋開幕）
# python3 mlpasia.py [ページ番号...] → out2/s1.png ...
# src/：Anton.ttf、選手写真、ロゴ（mlp_dark.png・logo_*.png）、court.png（Sansan池袋）※素材はリポジトリ外。完成画像は public/images/posts/mlp-asia-2026*.jpg
import sys, pathlib, asyncio, base64
from playwright.async_api import async_playwright
D = pathlib.Path(__file__).parent.resolve(); SRC = D/"src"; OUT = D/"out2"; OUT.mkdir(exist_ok=True)
def U(n):
    m = {"png":"image/png","ttf":"font/ttf","jpg":"image/jpeg"}[n.rsplit(".",1)[1]]
    return "data:%s;base64,%s" % (m, base64.b64encode((SRC/n).read_bytes()).decode())
N = 7
INK="#09131F"; PANEL="#132036"; LINE="rgba(255,255,255,.14)"; TXT="#F5F1EA"; MUTE="#A9B4C6"; OR="#E07A52"
TEAMS=[("日本","THE DOTS TOKYO","logo_dots"),("中国","DRAGON WARRIORS","logo_dragon"),("香港","HONG KONG CANNONS","logo_cannons"),
       ("フィリピン","MANILA HELIOS","logo_helios"),("ベトナム","VIET PANTHERS","logo_panthers"),("マレーシア","MALAYAN STRIPES","logo_stripes")]
CSS = f"""
@font-face {{ font-family:Anton; src:url('{U("Anton.ttf")}'); }}
*{{margin:0;padding:0;box-sizing:border-box}}
body{{width:1080px;height:1350px;overflow:hidden;font-family:'Noto Sans CJK JP';position:relative;background:{INK};color:{TXT}}}
.en{{font-family:Anton;letter-spacing:2px}}
.k{{position:absolute;left:64px;top:66px;font-family:Anton;font-size:32px;letter-spacing:5px;color:{OR};display:flex;align-items:center;gap:18px}}
.k:after{{content:"";width:72px;height:3px;background:{OR}}}
h1{{position:absolute;left:64px;top:122px;font-size:92px;line-height:1.24;font-weight:900;letter-spacing:-1px}}
.or{{color:{OR}}} .mute{{color:{MUTE}}}
.foot{{position:absolute;left:64px;right:64px;bottom:36px;display:flex;justify-content:space-between;font-family:Anton;font-size:24px;letter-spacing:4px;color:{MUTE};opacity:.75}}
.logo{{background:#fff;border-radius:22px;display:flex;align-items:center;justify-content:center}}
.logo img{{max-width:80%;max-height:74%;object-fit:contain}}
.cr{{position:absolute;font-size:24px;color:{MUTE}}}
"""
def foot(n): return f'<div class="foot"><span>PICKLEBALL TOKYO</span><span>{n:02d} / {N:02d}</span></div>'

# 1 表紙：初開催
def p1():
    circ="".join(f'<div class="logo c"><img src="{U(l+".png")}"></div>' for _,_,l in TEAMS)
    return f"""<style>
.mlp{{position:absolute;left:58px;top:84px;height:120px}}
.season{{position:absolute;right:64px;top:112px;font-family:Anton;font-size:36px;letter-spacing:4px;color:{MUTE};text-align:right;line-height:1.25}}
h1{{top:300px;font-size:100px;line-height:1.24}}
.date{{position:absolute;left:64px;right:64px;top:770px;display:flex;align-items:center;gap:32px}}
.date .d{{font-family:Anton;font-size:170px;line-height:.95;color:{OR}}}
.date .t{{font-size:54px;font-weight:900;line-height:1.3}}
.row{{position:absolute;left:64px;right:64px;top:1080px;display:flex;justify-content:space-between}}
.c{{height:132px;width:132px;border-radius:50%}}
.c img{{max-width:76%;max-height:66%}}
.rl{{position:absolute;left:64px;right:64px;top:1180px;font-size:36px;color:{MUTE};font-weight:700}}
</style>
<img class="mlp" src="{U("mlp_dark.png")}">
<div class="season">2026<br>FIRST SEASON</div>
<h1>ピックルボールの<br>メジャーリーグ、<br><span class="or">アジアで初開催。</span></h1>
<div class="date"><span class="d">11.13</span><span class="t">開幕は、<br>東京・池袋から</span></div>
<div class="row">{circ}</div>""" + foot(1)

# 2 出場チーム
def p2():
    cards="".join(f'<div><div class="logo t"><img src="{U(l+".png")}"></div><div class="cn">{c}</div><div class="tn en">{t}</div></div>' for c,t,l in TEAMS)
    return f"""<style>
.g{{position:absolute;left:64px;right:64px;top:424px;display:grid;grid-template-columns:repeat(3,1fr);gap:38px 26px}}
.t{{height:186px}} .cn{{font-size:48px;color:{OR};font-weight:900;margin-top:14px;line-height:1.2}}
.tn{{font-size:32px;letter-spacing:1px;line-height:1.15;margin-top:2px}}
.note{{position:absolute;left:64px;right:64px;top:1088px;padding-top:26px;border-top:1px solid {LINE};font-size:42px;line-height:1.45;font-weight:900}}
.note span{{display:block;color:{MUTE};font-weight:700;font-size:36px}}
</style>
<div class="k">06 TEAMS</div>
<div class="cr" style="right:64px;top:72px">ロゴ：MLP Asia・各チーム</div>
<h1>アジアの6チームが、<br>初代王者を争う。</h1>
<div class="g">{cards}</div>
<div class="note">各チーム6人<span>地元の選手3人 ＋ 国際ドラフトで選んだ3人</span></div>""" + foot(2)

# 3 1回の対戦
def p3():
    cols="".join(f'<div class="b"><div class="w">{a}</div><div class="x">ダブルス</div></div>' for a in ["女子","男子","混合","混合"])
    return f"""<style>
.lab{{position:absolute;left:64px;top:410px;font-size:38px;color:{MUTE};font-weight:700}}
.row{{position:absolute;left:64px;right:64px;top:430px;display:grid;grid-template-columns:repeat(4,1fr);gap:18px}}
.b{{background:{PANEL};border-radius:24px;height:210px;display:flex;flex-direction:column;align-items:center;justify-content:center}}
.w{{font-size:66px;font-weight:900}} .x{{font-size:34px;color:{MUTE};margin-top:2px}}
.ar{{position:absolute;left:64px;right:64px;top:730px;text-align:center;font-size:48px;font-weight:900}}
.ar b{{color:{OR}}}
.db{{position:absolute;left:64px;right:64px;top:870px;border-radius:28px;padding:50px 52px;background:linear-gradient(135deg,{OR},#B9573A)}}
.db .t{{font-family:Anton;font-size:92px;letter-spacing:3px;line-height:1}}
.db .s{{font-size:42px;font-weight:900;line-height:1.55;margin-top:24px}}
</style>
<div class="k">HOW A MATCH WORKS</div>
<h1>1回の対戦は、<br>4ゲームの団体戦。</h1>
<div class="row">{cols}</div>
<div class="ar"><b>2勝2敗</b>で並んだら ↓</div>
<div class="db"><div class="t">DREAMBREAKER</div>
<div class="s">4人が交代しながら、<br>シングルスで21点を争う決着戦。</div></div>""" + foot(3)

# 4 優勝まで（下から上へ）
def p4():
    S=[("決勝","2チーム","12/12","初代アジア王者が決まる",60,1),
       ("準決勝","4チーム","12/11","上位4チームが進出",80,0),
       ("グループステージ","6チーム","11/13〜11/28","各チームが1日ずつホームで開催",100,0)]
    it=""
    for i,(nm,ct,dt,ds,w,h) in enumerate(S):
        it+=f'''<div class="bar{" on" if h else ""}" style="width:{w}%"><span class="nm">{nm}</span><span class="ct">{ct}</span></div>
<div class="info"><span class="dt en">{dt}</span></div>'''
        if i<2: it+='<div class="up"></div>'
    return f"""<style>
.col{{position:absolute;left:64px;right:64px;top:396px;display:flex;flex-direction:column;align-items:center}}
.bar{{height:116px;border-radius:24px;background:{PANEL};display:flex;align-items:center;justify-content:center;gap:24px;padding:0 30px}}
.bar.on{{background:{OR};box-shadow:0 0 60px rgba(224,122,82,.35)}}
.nm{{font-size:58px;font-weight:900;white-space:nowrap}}
.ct{{font-size:38px;font-weight:900;color:{MUTE};white-space:nowrap}} .bar.on .ct{{color:{INK}}}
.info{{margin-top:16px}}
.dt{{font-size:44px;color:{MUTE}}} .ds{{font-size:36px;color:{MUTE}}}
.up{{width:0;height:0;border-left:18px solid transparent;border-right:18px solid transparent;border-bottom:22px solid {OR};margin:26px 0 22px}}
.nt{{position:absolute;left:64px;right:64px;top:1186px;font-size:26px;color:{MUTE};text-align:center}}
</style>
<div class="k">ROAD TO THE TITLE</div>
<h1>3つのステージを、<br>勝ち上がる。</h1>
<div class="col">{it}</div>
<div class="nt">※準決勝・決勝の会場は未定（2026年11月10日時点）</div>""" + foot(4)

# 5 東京代表（縦3×横2）
def p5():
    P=[("funemizu","船水 雄太","キャプテン","ソフトテニス出身<br>日本人初のMLP選手"),
       ("hatakeyama","畠山 成冴","","テニスから<br>パデル日本代表へ"),
       ("fujiwara","藤原 里華","","元テニス日本代表<br>全仏ダブルス4強"),
       ("yoshitomi","吉冨 愛子","","元プロテニス選手<br>夫婦でPPAと契約"),
       ("moore","ダニエル・ムーア","アメリカ","大学テニス出身<br>子ども時代は日本"),
       ("kwon","ミヘ・クォン","韓国","大学までテニス<br>元テニスコーチ")]
    cards="".join(f'''<div class="cd"><img src="{U(f+".png")}"{' style="transform:scale(1.35);transform-origin:45% 15%"' if f=="funemizu" else ''}><i></i><div class="tx"><div class="n">{n}</div>{f'<span class="tg">{t}</span>' if t else ''}<div class="d">{d}</div></div></div>''' for f,n,t,d in P)
    return f"""<style>
.top{{position:absolute;left:64px;right:64px;top:124px;display:flex;align-items:center;gap:34px}}
.top .logo{{width:250px;height:150px;flex:none}}
.top h2{{font-size:62px;font-weight:900;line-height:1.22}}
.top p{{font-size:34px;color:{MUTE};margin-top:6px;font-weight:700}}
.g{{position:absolute;left:64px;right:64px;top:352px;display:grid;grid-template-columns:1fr 1fr;gap:22px}}
.cd{{background:{PANEL};border-radius:24px;padding:0 18px 0 196px;display:flex;align-items:center;height:254px;position:relative;overflow:hidden}}
.cd i{{position:absolute;inset:0;background:linear-gradient(270deg,{PANEL} 58%,rgba(19,32,54,.55) 63%,rgba(19,32,54,0) 74%)}}
.tx{{position:relative;text-shadow:0 2px 10px rgba(9,19,31,.7)}}
.cd img{{position:absolute;left:0;top:0;width:44%;height:100%;object-fit:cover;object-position:50% 18%}}
.n{{font-size:33px;font-weight:900;line-height:1.2;white-space:nowrap}}
.tg{{display:inline-block;font-size:24px;font-weight:900;background:{OR};color:{INK};padding:1px 14px;border-radius:20px;margin-top:8px}}
.d{{font-size:29px;font-weight:700;line-height:1.45;color:#C3CCDA;margin-top:8px;white-space:nowrap}}
.nt{{position:absolute;left:64px;right:64px;top:1182px;font-size:42px;font-weight:900}}
.nt b{{color:{OR}}}
</style>
<div class="k">TEAM TOKYO</div>
<div class="cr" style="right:64px;top:72px">写真：THE DOTS TOKYO</div>
<div class="top"><div class="logo"><img src="{U("logo_dots.png")}"></div>
<div><h2>東京代表は、<br>THE DOTS TOKYO</h2><p>TBSと電通グループが設立</p></div></div>
<div class="g">{cards}</div>
<div class="nt">6人全員が、<b>テニス・ソフトテニス出身。</b></div>""" + foot(5)

# 6 開幕戦（コートの写真を背景に透かす）
def p6():
    def m(tm, lg):
        return f'''<div class="m"><div class="tm en">{tm}</div>
<div class="logo s"><img src="{U("logo_dots.png")}"></div><span class="v en">VS</span>
<div class="logo s"><img src="{U(lg+".png")}"></div></div>'''
    return f"""<style>
.bg{{position:absolute;left:0;top:0;width:1080px;height:1000px;object-fit:cover;object-position:50% 55%;opacity:.55}}
.ov{{position:absolute;inset:0;background:linear-gradient(rgba(9,19,31,.6) 0%,rgba(9,19,31,.3) 34%,rgba(9,19,31,.85) 60%,{INK} 72%)}}
h1{{top:124px;font-size:96px;line-height:1.22;text-shadow:0 4px 30px rgba(0,0,0,.45)}}
.ven{{position:absolute;left:64px;right:64px;top:500px;text-shadow:0 2px 20px rgba(0,0,0,.6)}}
.ven .a{{font-size:46px;font-weight:900}} .ven .b{{font-size:36px;font-weight:700;color:#E2E8F1;margin-top:8px}}
.ms{{position:absolute;left:64px;right:64px;top:860px;display:grid;gap:28px}}
.m{{background:rgba(19,32,54,.94);border-radius:24px;padding:18px 30px;display:flex;align-items:center;gap:20px}}
.tm{{font-size:80px;color:{OR};width:236px;line-height:1}}
.s{{width:250px;height:126px;border-radius:18px}}
.v{{font-size:38px;color:{MUTE};width:64px;text-align:center}}
.cr2{{position:absolute;right:64px;top:806px;font-size:24px;color:#DCE3EE}}
</style>
<img class="bg" src="{U("court.png")}"><div class="ov"></div>
<div class="k">OPENING NIGHT · 11.13 FRI</div>
<h1>開幕戦は、<br><span class="or">池袋</span>から。</h1>
<div class="ven"><div class="a">Sansanピックルボールコート池袋</div><div class="b">東池袋駅から徒歩3分 ／ 17:00 開場</div></div>
<div class="cr2">写真：Sansanピックルボールコート池袋</div>
<div class="ms">{m("18:00","logo_helios")}{m("19:30","logo_stripes")}</div>""" + foot(6)

# 7 立ち会おう
def p7():
    return f"""<style>
h1{{font-size:96px;line-height:1.22}}
.lead{{position:absolute;left:64px;right:64px;top:430px;font-size:44px;line-height:1.55;font-weight:900}}
.lead span{{display:block;color:{MUTE};font-weight:700;font-size:38px;margin-top:6px}}
.tk{{position:absolute;left:64px;right:64px;top:600px;display:grid;grid-template-columns:1fr 1fr;gap:18px}}
.tk>div{{background:{PANEL};border-radius:24px;padding:30px 36px}}
.tk .a{{font-size:36px;color:{MUTE};font-weight:700}} .tk .p{{font-family:Anton;font-size:100px;line-height:1.1;margin-top:4px}}
.tk .p small{{font-family:'Noto Sans CJK JP';font-size:42px;font-weight:900;margin-left:6px}}
.tn{{position:absolute;left:64px;top:870px;font-size:32px;color:{MUTE};font-weight:700}}
.lk{{position:absolute;left:64px;right:64px;top:990px;background:{OR};border-radius:26px;padding:32px 44px;display:flex;justify-content:space-between;align-items:center;color:{INK}}}
.lk .a{{font-size:38px;font-weight:900}} .lk .u{{font-family:Anton;font-size:60px;letter-spacing:1px;margin-top:2px}}
.lk .ar{{font-family:Anton;font-size:72px}}
</style>
<div class="k">BE THERE</div>
<h1>アジア初の開幕戦に、<br><span class="or">立ち会おう。</span></h1>
<div class="lead">日本で見られるのは、この1日だけ。</div>
<div class="tk"><div><div class="a">コートサイド席</div><div class="p">3,000<small>円</small></div></div>
<div><div class="a">立見エリア</div><div class="p">1,000<small>円</small></div></div></div>
<div class="tn">TBSチケットで販売中（自由席・数に限りあり）</div>
<div class="lk"><div><div class="a">チケットは、プロフィールのリンクから</div><div class="u">PICKLEBALL-TOKYO.COM</div></div><div class="ar">→</div></div>""" + foot(7)

PAGES={1:p1,2:p2,3:p3,4:p4,5:p5,6:p6,7:p7}
async def main(ps):
    async with async_playwright() as p:
        b=await p.chromium.launch(); pg=await b.new_page(viewport={"width":1080,"height":1350})
        for n in ps:
            await pg.set_content(f"<html><head><meta charset='utf-8'><style>{CSS}</style></head><body>{PAGES[n]()}</body></html>")
            await pg.wait_for_timeout(300); await pg.screenshot(path=str(OUT/f"s{n}.png"))
        await b.close()
asyncio.run(main([int(x) for x in sys.argv[1:]] or list(range(1,N+1))))
