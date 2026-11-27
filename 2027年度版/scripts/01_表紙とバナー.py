"""表紙の見開き画像から 01_表紙 と 03_バナー を作る。"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '元データ', '表紙見開き_気学手帳2027.png')
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
def font(p, size): return ImageFont.truetype(p, size, index=0)
GOLD = (226, 190, 100); WHITE = (255, 255, 255); PURPLE = (74, 32, 92)

full = Image.open(SRC).convert('RGB')
# pixel position of the bleed box (34.0..905.6pt) in the PNG spread
K = (1944 - 55 + 1) / (905.612598 - 34.015748)
def px(x, y): return (round(55 + (x - 34.015748) * K), round(56 + (646.299213 - y) * K))
fa = px(897.108661 - 419.527559, 637.795276); fb = px(897.108661, 42.519685)
front = full.crop((fa[0], fa[1], fb[0], fb[1]))

# ---- 1. front cover (web size) ----
fc = front.copy()
fc.save(f'{OUT}/01_表紙_気学手帳2027.jpg', quality=92)

# ---- 3. banner (BASE main image ratio 3691:2135): notebook + lotus calendar ----
BW = 1920; BH = round(BW * 2135 / 3691)   # 1920 x 1111
# background: the purple -> pink gradient from a thin strip along the top of the cover spread
a = px(42.52, 635.0); b = px(897.11, 595.0)
ban = full.crop((a[0], a[1], b[0], b[1])).resize((BW, BH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))
ov = Image.new('L', (BW, BH), 0); od = ImageDraw.Draw(ov)
for x in range(BW):
    od.line((x, 0, x, BH), fill=int(110 * max(0, 1 - x / 1300)))
ban.paste(Image.new('RGB', (BW, BH), (40, 10, 50)), (0, 0), ov)

# products on the right: the calendar behind, the notebook in front of its upper-left part
# (kept above the calendar's title at the bottom)
cal = Image.open(os.path.join(ROOT, '元データ', 'カレンダー', '表紙.png')).convert('RGB')
def put(img, x, y, h):
    w = round(img.width * h / img.height)
    sh = Image.new('L', (BW, BH), 0)
    ImageDraw.Draw(sh).rectangle((x + 16, y + 22, x + w + 16, y + h + 22), fill=150)
    ban.paste(Image.new('RGB', (BW, BH), (30, 5, 35)), (0, 0), sh.filter(ImageFilter.GaussianBlur(24)))
    ban.paste(img.resize((w, h), Image.LANCZOS), (x, y))
CY = (BH - 900) // 2
put(cal, 1180, CY, 900)
put(front, 1045, CY + 70, 520)

d = ImageDraw.Draw(ban)
L = 160; T = BH // 2 - 325   # text block (650px tall) centred vertically
d.text((L, T), '九星気学グッズ', font=font(SR, 52), fill=GOLD, anchor='ls')
d.text((L, T + 156), '2027年度版', font=font(SB, 125), fill=WHITE, anchor='ls')
d.text((L, T + 305), '販売開始', font=font(SB, 125), fill=WHITE, anchor='ls')
d.line((L, T + 364, L + 830, T + 364), fill=GOLD, width=4)
d.text((L, T + 448), '気学手帳・ポケット版・気学カレンダー', font=font(SR, 46), fill=WHITE, anchor='ls')
d.text((L, T + 540), 'ネット限定価格　｜　手帳は1冊から送料無料', font=font(SR, 40), fill=GOLD, anchor='ls')
d.text((L, T + 650), 'いのちの樹', font=font(SR, 39), fill=WHITE, anchor='ls')
ban.save(f'{OUT}/03_バナー_2027販売開始.jpg', quality=92)
print('ok')
