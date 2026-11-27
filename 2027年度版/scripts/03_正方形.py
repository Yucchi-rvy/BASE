"""正方形の商品画像（02, 05, 08, 09, 10）を同じひな形で作る。01 と 04 を先に作っておくこと。"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '画像')
POSTER = os.path.join(OUT, '04_ポスター全体_邂逅2027.jpg')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
PURPLE = (74, 32, 92); GOLD = (196, 152, 52); BG = (247, 240, 244)
S = 1200
TOP, BOTTOM = 60, 950          # common area for the product picture
TITLE_Y, SUB_Y, LABEL_Y = 1035, 1105, 985
TITLE_F, SUB_F, LABEL_F = F(SB, 48), F(SR, 36), F(SR, 30)
cover = Image.open(f'{OUT}/01_表紙_気学手帳2027.jpg').convert('RGB')
poster = Image.open(POSTER).convert('RGB')

def new(): return Image.new('RGB', (S, S), BG)
def items(bg, placed):
    """placed: list of (img, x, y, h) — draw all shadows first, then images."""
    sh = Image.new('L', (S, S), 0); sd = ImageDraw.Draw(sh); out = []
    for img, x, y, h in placed:
        w = round(img.width * h / img.height)
        sd.rectangle((x + 10, y + 14, x + w + 10, y + h + 14), fill=110); out.append((img.resize((w, h), Image.LANCZOS), x, y))
    sh = sh.filter(ImageFilter.GaussianBlur(16))
    bg.paste(Image.new('RGB', (S, S), (120, 90, 110)), (0, 0), sh)
    for c, x, y in out: bg.paste(c, (x, y))
def text(bg, title, sub):
    d = ImageDraw.Draw(bg)
    d.text((S // 2, TITLE_Y), title, font=TITLE_F, fill=PURPLE, anchor='mm')
    d.text((S // 2, SUB_Y), sub, font=SUB_F, fill=PURPLE, anchor='mm')
    return d
wof = lambda img, h: round(img.width * h / img.height)
H = BOTTOM - TOP

# 02 notebook
bg = new(); items(bg, [(cover, (S - wof(cover, H)) // 2, TOP, H)])
text(bg, '気学手帳　2027年度版', 'A5サイズ　未年にちなんだ子羊の表紙です')
bg.save(f'{OUT}/02_正方形_気学手帳2027.jpg', quality=92)

# 08 pocket
bg = new(); items(bg, [(cover, (S - wof(cover, H)) // 2, TOP, H)])
text(bg, '気学手帳ポケット版　2027年度版', 'A6サイズ　持ち歩きに便利です')
bg.save(f'{OUT}/08_正方形_ポケット版2027.jpg', quality=92)

# 05 poster
bg = new(); items(bg, [(poster, (S - wof(poster, H)) // 2, TOP, H)])
text(bg, '2027年 ポスターカレンダー「邂逅」', '富永成風　B2サイズの一枚ものです')
bg.save(f'{OUT}/05_正方形_ポスター邂逅2027.jpg', quality=92)

# 09 notebook + pocket (real A5:A6 ratio, bottoms aligned)
yb = TOP + H - 50; hA5 = 770; hA6 = round(hA5 * 0.707); gap = 70
wA5, wA6 = wof(cover, hA5), wof(cover, hA6); x0 = (S - (wA5 + gap + wA6)) // 2
bg = new(); items(bg, [(cover, x0, yb - hA5, hA5), (cover, x0 + wA5 + gap, yb - hA6, hA6)])
d = text(bg, '気学手帳＆ポケット版セット　2027年度版', 'セット価格 4,800円、定価より700円お得です')
d.text((x0 + wA5 // 2, yb + 45), '気学手帳（A5）', font=LABEL_F, fill=PURPLE, anchor='mm')
d.text((x0 + wA5 + gap + wA6 // 2, yb + 45), 'ポケット版（A6）', font=LABEL_F, fill=PURPLE, anchor='mm')
bg.save(f'{OUT}/09_正方形_手帳ポケット版セット2027.jpg', quality=92)

# 10 five plus one
gy = 50; h = (H - gy) // 2; w = wof(cover, h); gx = 60
x0 = (S - (3 * w + 2 * gx)) // 2
pos = [(x0 + i % 3 * (w + gx), TOP + i // 3 * (h + gy)) for i in range(6)]
bg = new(); items(bg, [(cover, x, y, h) for x, y in pos])
d = text(bg, '気学手帳 5冊＋1冊プレゼント　2027年度版', '5冊分のお値段で6冊、14,000円です')
x, y = pos[5]; r = 80; cx, cy = x + w, y + h - r - 30   # half outside the right edge of the 6th book
d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD, outline=(255, 255, 255), width=5)
d.text((cx, cy - 19), '＋1冊', font=F(SB, 36), fill=(255, 255, 255), anchor='mm')
d.text((cx, cy + 25), 'プレゼント', font=F(SB, 24), fill=(255, 255, 255), anchor='mm')
bg.save(f'{OUT}/10_正方形_手帳5冊プラス1冊2027.jpg', quality=92)
print('ok', x0, w, S - (pos[5][0] + w))
