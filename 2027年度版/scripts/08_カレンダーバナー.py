"""気学カレンダーだけのバナー（BASEのメイン画像の比率 3691:2135）を作る。"""
import os
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAL = os.path.join(ROOT, '元データ', 'カレンダー')
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
GOLD = (226, 190, 100); WHITE = (255, 255, 255)
BW = 1920; BH = round(BW * 2135 / 3691)

cover = Image.open(os.path.join(CAL, '表紙.png')).convert('RGB')
# background: the lotus photo of the cover (above its title), softly blurred
ch = round(cover.width * BH / BW)
ban = cover.crop((0, 120, cover.width, 120 + ch)).resize((BW, BH), Image.LANCZOS).filter(ImageFilter.GaussianBlur(14))
# deep purple veil, strongest on the left where the text sits
ov = Image.new('L', (BW, BH), 0); od = ImageDraw.Draw(ov)
for x in range(BW):
    od.line((x, 0, x, BH), fill=int(70 + 150 * max(0, 1 - x / 1250)))
ban.paste(Image.new('RGB', (BW, BH), (45, 15, 60)), (0, 0), ov)

# the calendar cover on the right
h = 900; w = round(cover.width * h / cover.height); x = BW - w - 190; y = (BH - h) // 2
sh = Image.new('L', (BW, BH), 0)
ImageDraw.Draw(sh).rectangle((x + 18, y + 24, x + w + 18, y + h + 24), fill=160)
ban.paste(Image.new('RGB', (BW, BH), (20, 5, 25)), (0, 0), sh.filter(ImageFilter.GaussianBlur(26)))
ban.paste(cover.resize((w, h), Image.LANCZOS), (x, y))

d = ImageDraw.Draw(ban)
L = 160; T = BH // 2 - 325
d.text((L, T), '2027年度版　毎日の運気アップのための', font=F(SR, 46), fill=GOLD, anchor='ls')
d.text((L, T + 156), '九星気学', font=F(SB, 125), fill=WHITE, anchor='ls')
d.text((L, T + 305), 'カレンダー', font=F(SB, 125), fill=WHITE, anchor='ls')
d.line((L, T + 364, L + 880, T + 364), fill=GOLD, width=4)
d.text((L, T + 448), '九紫火星にちなんだテーマ「麗しく」', font=F(SR, 46), fill=WHITE, anchor='ls')
d.text((L, T + 540), '毎日の遁甲盤入り　｜　ネット販売20部限定', font=F(SR, 40), fill=GOLD, anchor='ls')
d.text((L, T + 650), 'いのちの樹', font=F(SR, 39), fill=WHITE, anchor='ls')
ban.save(os.path.join(OUT, '26_バナー_気学カレンダー.jpg'), quality=92)
print('ok', ban.size)
