from playwright.sync_api import sync_playwright
from PIL import Image
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/opt/pw-browsers/chromium-1194/chrome-linux/chrome')
    pg=b.new_page(viewport={'width':390,'height':844},device_scale_factor=1)
    shots=[]
    for i,u in enumerate(['/events/','/events/tocho-challenge-days-2026/']):
        pg.goto('http://localhost:4321'+u); pg.wait_for_timeout(800)
        f=f's{i}.png'; pg.screenshot(path=f,full_page=True); shots.append(f)
    pg.goto('http://localhost:4321/'); pg.wait_for_timeout(800)
    el=pg.query_selector('#events'); el.screenshot(path='s2.png'); shots.append('s2.png')
    b.close()
ims=[Image.open(f) for f in shots]
h=min(max(i.height for i in ims),1800)
out=Image.new('RGB',(sum(i.width for i in ims)+20*len(ims),h),'white')
x=0
for i in ims: out.paste(i.crop((0,0,i.width,min(i.height,h))),(x,0)); x+=i.width+20
out.save('events.png')
