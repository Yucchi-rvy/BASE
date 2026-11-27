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

# ---- 3. banner 1920x720 from the cover spread ----
# hide the barcode: blend each column between the rows just above and below it
bx0, by0 = px(326, 178); bx1, by1 = px(416, 90)
import numpy as np
arr = np.asarray(full).astype(np.float32).copy()
top = arr[by0 - 3:by0].mean(axis=0); bot = arr[by1:by1 + 3].mean(axis=0)
n = by1 - by0
for i in range(n):
    t = i / max(1, n - 1)
    arr[by0 + i, bx0:bx1] = top[bx0:bx1] * (1 - t) + bot[bx0:bx1] * t
full = Image.fromarray(arr.clip(0, 255).astype('uint8'))
# crop: x trim 42.52..897.11, height to 1920:720
x0 = 42.52; x1 = 897.11; hpt = (x1 - x0) * 720 / 1920
yc = 304.5; ya = yc + hpt / 2; yb = yc - hpt / 2
a = px(x0, ya); b = px(x1, yb)
ban = full.crop((a[0], a[1], b[0], b[1])).resize((1920, 720), Image.LANCZOS)
# darken left side slightly for legibility
ov = Image.new('L', (1920, 720), 0); od = ImageDraw.Draw(ov)
for x in range(1100):
    od.line((x, 0, x, 720), fill=int(90 * (1 - x / 1100)))
ban.paste(Image.new('RGB', (1920, 720), (40, 10, 50)), (0, 0), ov)
d = ImageDraw.Draw(ban)
L = 130
d.text((L, 150), '九星気学グッズ', font=font(SR, 40), fill=GOLD, anchor='ls')
d.text((L, 270), '2027年度版', font=font(SB, 96), fill=WHITE, anchor='ls')
d.text((L, 385), '販売開始', font=font(SB, 96), fill=WHITE, anchor='ls')
d.line((L, 430, L + 640, 430), fill=GOLD, width=3)
d.text((L, 495), '気学手帳・ポケット版・気学カレンダー', font=font(SR, 40), fill=WHITE, anchor='ls')
d.text((L, 565), 'ネット限定価格　｜　お得なセットは送料無料', font=font(SR, 32), fill=GOLD, anchor='ls')
d.text((L, 650), 'いのちの樹', font=font(SR, 30), fill=WHITE, anchor='ls')
ban.save(f'{OUT}/03_バナー_2027販売開始.jpg', quality=92)
print('ok')
