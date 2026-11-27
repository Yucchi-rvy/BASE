"""気学カレンダーと、カレンダー入りのセットの正方形画像（18〜22）と、1・6・9月のサンプル（23〜25）を作る。
文字の位置・大きさは 03_正方形.py と同じ。01_表紙とバナー.py を先に実行しておくこと。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(ROOT, '元データ', 'カレンダー')
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
PURPLE = (74, 32, 92); BG = (247, 240, 244)
S = 1200; TOP, BOTTOM = 60, 950; H = BOTTOM - TOP
TITLE_Y, SUB_Y = 1035, 1105
TITLE_F, SUB_F, LABEL_F = F(SB, 48), F(SR, 36), F(SR, 30)

cal = Image.open(os.path.join(CAL, '表紙.png')).convert('RGB')
months = [Image.open(os.path.join(CAL, m)).convert('RGB') for m in ('01月.png', '06月.png', '09月.png')]
book = Image.open(os.path.join(OUT, '01_表紙_気学手帳2027.jpg')).convert('RGB')
wof = lambda img, h: round(img.width * h / img.height)

def canvas(): return Image.new('RGB', (S, S), BG)
def items(bg, placed):
    sh = Image.new('L', (S, S), 0); sd = ImageDraw.Draw(sh); out = []
    for img, x, y, h in placed:
        w = wof(img, h)
        sd.rectangle((x + 10, y + 14, x + w + 10, y + h + 14), fill=110)
        out.append((img.resize((w, h), Image.LANCZOS), x, y))
    bg.paste(Image.new('RGB', (S, S), (120, 90, 110)), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
    for c, x, y in out: bg.paste(c, (x, y))
def text(bg, title, sub):
    d = ImageDraw.Draw(bg)
    d.text((S // 2, TITLE_Y), title, font=TITLE_F, fill=PURPLE, anchor='mm')
    d.text((S // 2, SUB_Y), sub, font=SUB_F, fill=PURPLE, anchor='mm')
    return d
def save(bg, name): bg.save(os.path.join(OUT, name), quality=92)

# 18: calendar cover
bg = canvas(); items(bg, [(cal, (S - wof(cal, H)) // 2, TOP, H)])
text(bg, '気学カレンダー　2027年度版', 'A3サイズ　ネット販売は20部限定です'); save(bg, '18_正方形_気学カレンダー2027.jpg')

# 19: three months side by side
gap = 40; w = (S - 120 - 2 * gap) // 3; h = round(w * months[0].height / months[0].width); x0 = (S - (3 * w + 2 * gap)) // 2; y = TOP + (H - h) // 2
bg = canvas(); items(bg, [(m, x0 + i * (w + gap), y, h) for i, m in enumerate(months)])
d = text(bg, '毎月ちがう蓮の写真', '九紫火星にちなんだテーマは「麗しく」です')
for i, lab in enumerate(['1月', '6月', '9月']):
    d.text((x0 + i * (w + gap) + w // 2, y + h + 45), lab, font=LABEL_F, fill=PURPLE, anchor='mm')
save(bg, '19_中身_カレンダー毎月の写真.jpg')

# 20: close-up of the January day column (dark panel)
jan = months[0]
zoom = jan.crop((1090, 40, 1423, 692))          # month boards + first days
bg = canvas(); items(bg, [(zoom, (S - wof(zoom, H)) // 2, TOP, H)])
text(bg, '毎日の遁甲盤入り', '節がわりや土用、満月・新月もわかります'); save(bg, '20_中身_カレンダー毎日の遁甲盤.jpg')

# 21: notebook + calendar (real A5 : A3 height ratio = 210 : 420)
yb = TOP + H - 50; hc = H - 50; hb = round(hc * 210 / 420); gap = 70
wc, wb = wof(cal, hc), wof(book, hb); x0 = (S - (wb + gap + wc)) // 2
bg = canvas(); items(bg, [(book, x0, yb - hb, hb), (cal, x0 + wb + gap, yb - hc, hc)])
d = text(bg, '気学手帳＆カレンダーセット　2027年度版', 'セット価格 5,300円、定価より700円お得です')
d.text((x0 + wb // 2, yb + 45), '気学手帳（A5）', font=LABEL_F, fill=PURPLE, anchor='mm')
d.text((x0 + wb + gap + wc // 2, yb + 45), '気学カレンダー（A3）', font=LABEL_F, fill=PURPLE, anchor='mm')
save(bg, '21_正方形_手帳カレンダーセット2027.jpg')

# 22: full set (A5 / A6 / A3), scaled down to keep 60px side margins
gap = 55
k = min(1, (S - 120 - 2 * gap) / (wof(book, hb) + wof(book, round(hb * 0.707)) + wof(cal, hc)))
hc, hb = round(hc * k), round(hb * k); hp = round(hb * 0.707)
wc, wb, wp = wof(cal, hc), wof(book, hb), wof(book, hp)
x0 = (S - (wb + gap + wp + gap + wc)) // 2
bg = canvas(); items(bg, [(book, x0, yb - hb, hb), (book, x0 + wb + gap, yb - hp, hp), (cal, x0 + wb + gap + wp + gap, yb - hc, hc)])
d = text(bg, '気学グッズフルセット　2027年度版', 'セット価格 7,300円、定価より1,200円お得です')
d.text((x0 + wb // 2, yb + 45), '手帳（A5）', font=LABEL_F, fill=PURPLE, anchor='mm')
d.text((x0 + wb + gap + wp // 2, yb + 45), 'ポケット版', font=LABEL_F, fill=PURPLE, anchor='mm')
d.text((x0 + wb + gap + wp + gap + wc // 2, yb + 45), 'カレンダー（A3）', font=LABEL_F, fill=PURPLE, anchor='mm')
save(bg, '22_正方形_フルセット2027.jpg')
print('ok')

# 23-25: sample pages (January / June / September) — the page itself, no background or text
for i, mon in enumerate(['1月', '6月', '9月']):
    months[i].save(os.path.join(OUT, f'{23 + i}_サンプル_カレンダー{mon}.jpg'), quality=92)
print('samples ok')
