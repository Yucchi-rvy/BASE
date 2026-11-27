"""「気学手帳は1冊から送料無料」のバナー（BASEのメイン画像の比率 3691:2135）を作る。
01_表紙とバナー.py を先に実行して 01_表紙 を作っておくこと。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '元データ', '表紙見開き_気学手帳2027.png')
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
GOLD = (226, 190, 100); WHITE = (255, 255, 255)
BW = 1920; BH = round(BW * 2135 / 3691)

full = Image.open(SRC).convert('RGB')
K = (1944 - 55 + 1) / (905.612598 - 34.015748)
def px(x, y): return (round(55 + (x - 34.015748) * K), round(56 + (646.299213 - y) * K))
# background: the purple -> pink gradient from a thin strip along the top of the spread
# (above the cover's "2027" and the lamb), stretched to the banner and softened
a = px(42.52, 635.0); b = px(897.11, 595.0)
ban = full.crop((a[0], a[1], b[0], b[1])).resize((BW, BH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(24))
# keep the left side calm for the text
ov = Image.new('L', (BW, BH), 0); od = ImageDraw.Draw(ov)
for x in range(BW):
    od.line((x, 0, x, BH), fill=int(110 * max(0, 1 - x / 1300)))
ban.paste(Image.new('RGB', (BW, BH), (40, 10, 50)), (0, 0), ov)

# the front cover with a shadow on the right
cover = Image.open(os.path.join(OUT, '01_表紙_気学手帳2027.jpg')).convert('RGB')
ch = 900; cw = round(cover.width * ch / cover.height)
cx = BW - cw - 190; cy = (BH - ch) // 2
sh = Image.new('L', (BW, BH), 0)
ImageDraw.Draw(sh).rectangle((cx + 18, cy + 24, cx + cw + 18, cy + ch + 24), fill=150)
sh = sh.filter(ImageFilter.GaussianBlur(26))
ban.paste(Image.new('RGB', (BW, BH), (30, 5, 35)), (0, 0), sh)
ban.paste(cover.resize((cw, ch), Image.LANCZOS), (cx, cy))

d = ImageDraw.Draw(ban)
L = 160; T = BH // 2 - 330
d.text((L, T), '九星気学　気学手帳 2027年度版', font=F(SR, 50), fill=GOLD, anchor='ls')
d.text((L, T + 165), '1冊から', font=F(SB, 120), fill=WHITE, anchor='ls')
d.text((L, T + 330), '送料無料！', font=F(SB, 150), fill=WHITE, anchor='ls')
d.line((L, T + 395, L + 880, T + 395), fill=GOLD, width=4)
d.text((L, T + 480), 'ネット価格 2,800円（定価 3,000円）', font=F(SR, 50), fill=WHITE, anchor='ls')
d.text((L, T + 560), '2,800円以上のお買い上げで送料無料', font=F(SR, 40), fill=GOLD, anchor='ls')
d.text((L, T + 660), 'いのちの樹', font=F(SR, 39), fill=WHITE, anchor='ls')
ban.save(os.path.join(OUT, '11_バナー_気学手帳送料無料.jpg'), quality=92)
print('ok', ban.size)
