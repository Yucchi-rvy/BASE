"""「どれを選べばいい？」の選び方ガイド（正方形 1200×1200）を作る。"""
import os
from PIL import Image, ImageDraw, ImageFont
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
PURPLE = (74, 32, 92); GOLD = (196, 152, 52); BG = (247, 240, 244); CARD = (255, 255, 255)
S = 1200

ROWS = [
    ('気学を始めたばかりの方・持ち歩きたい方', '気学手帳ポケット版', '2,300円'),
    ('日盤吉方も一年の運気もしっかり見たい方', '気学手帳（1冊から送料無料）', '2,800円'),
    ('家では手帳、外ではポケット版を使いたい方', '気学手帳＆ポケット版セット', '4,800円'),
    ('壁に掛けて毎日の日盤をひと目で見たい方', '気学手帳＆カレンダーセット', '5,300円'),
    ('全部そろえたい方', '気学グッズフルセット', '7,300円'),
    ('教室・勉強会・ご家族の分をまとめて', '気学手帳 5冊＋1冊プレゼント', '14,000円'),
]

im = Image.new('RGB', (S, S), BG)
d = ImageDraw.Draw(im)
d.text((S // 2, 95), 'どれを選べばいい？', font=F(SB, 64), fill=PURPLE, anchor='mm')
d.text((S // 2, 170), '2027年度版 気学グッズの選び方', font=F(SR, 36), fill=GOLD, anchor='mm')

M = 70; top = 225; rh = 140; gap = 18
for i, (who, item, price) in enumerate(ROWS):
    y = top + i * (rh + gap)
    d.rounded_rectangle((M, y, S - M, y + rh), radius=14, fill=CARD)
    d.rectangle((M, y + 14, M + 8, y + rh - 14), fill=GOLD)
    d.text((M + 40, y + 48), who, font=F(SR, 32), fill=PURPLE, anchor='lm')
    d.text((M + 40, y + 102), '→ ' + item, font=F(SB, 38), fill=PURPLE, anchor='lm')
    d.text((S - M - 36, y + 102), price, font=F(SB, 40), fill=GOLD, anchor='rm')

im.save(os.path.join(OUT, '12_正方形_選び方ガイド.jpg'), quality=92)
print('ok', top + 6 * (rh + gap) - gap)
