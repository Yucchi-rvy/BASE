"""手帳の中身のPDFから、中身を紹介する正方形の画像（13〜17）を作る。
文字の位置・大きさは 03_正方形.py と同じ。pdftoppm が必要。"""
import os, subprocess, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageFilter
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SRC = os.path.join(ROOT, '元データ', '中身')
OUT = os.path.join(ROOT, '画像')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
PURPLE = (74, 32, 92); GOLD = (196, 152, 52); BG = (247, 240, 244)
S = 1200; TOP, BOTTOM = 60, 950; H = BOTTOM - TOP
TITLE_Y, SUB_Y = 1035, 1105
TITLE_F, SUB_F = F(SB, 48), F(SR, 36)
PREV = 1391 / 2520          # crop boxes below are measured on a 1391px-wide preview

tmp = tempfile.mkdtemp()
def render(name):
    base = os.path.join(tmp, 'p')
    subprocess.run(['pdftoppm', '-r', '200', '-png', '-singlefile', os.path.join(SRC, name), base], check=True)
    return Image.open(base + '.png').convert('RGB')     # 2520 x 1812
def crop(im, box):
    return im.crop(tuple(round(v / PREV) for v in box))

def square(page, title, sub, out):
    bg = Image.new('RGB', (S, S), BG)
    scale = min(H / page.height, (S - 120) / page.width)
    w, h = round(page.width * scale), round(page.height * scale)
    x, y = (S - w) // 2, TOP + (H - h) // 2
    sh = Image.new('L', (S, S), 0)
    ImageDraw.Draw(sh).rectangle((x + 10, y + 14, x + w + 10, y + h + 14), fill=90)
    bg.paste(Image.new('RGB', (S, S), (120, 90, 110)), (0, 0), sh.filter(ImageFilter.GaussianBlur(16)))
    bg.paste(page.resize((w, h), Image.LANCZOS), (x, y))
    d = ImageDraw.Draw(bg)
    d.text((S // 2, TITLE_Y), title, font=TITLE_F, fill=PURPLE, anchor='mm')
    d.text((S // 2, SUB_Y), sub, font=SUB_F, fill=PURPLE, anchor='mm')
    bg.save(os.path.join(OUT, out), quality=92)
    return bg, (x, y, scale)

def badge(d, cx, cy, text, r=58):
    d.ellipse((cx - r, cy - r, cx + r, cy + r), fill=GOLD, outline=(255, 255, 255), width=4)
    d.text((cx, cy), text, font=F(SB, 34), fill=(255, 255, 255), anchor='mm')

# 13: one month on a spread (Nov 2026) / 14: close-up of the daily boards
calpage = render('p20-21_2026年11月.pdf')
square(crop(calpage, (90, 84, 1298, 928)), '見開きで1か月', '毎日の日盤と月盤・年盤が載っています', '13_中身_1か月の見開き.jpg')
square(crop(calpage, (92, 84, 655, 654)), '毎日の日盤がひと目で', '六曜・満月新月・線路の日の印つきです', '14_中身_毎日の日盤.jpg')

# 15: honmeisei list with the new 納音 column outlined
lst = crop(render('p6-7_本命星一覧.pdf'), (74, 68, 674, 560))
k = 1 / PREV; dl = ImageDraw.Draw(lst)
dl.rounded_rectangle((round((516 - 74) * k), round((118 - 68) * k), round((594 - 74) * k), lst.height - 6),
                     radius=18, outline=GOLD, width=10)
bg, (x, y, sc) = square(lst, '本命星一覧に「納音」を追加', '生まれ年から本命星と納音がすぐわかります', '15_中身_本命星一覧と納音.jpg')
d = ImageDraw.Draw(bg)
badge(d, x + round((555 - 74) * k * sc), y + round(lst.height * sc), 'NEW')   # below the 納音 column
bg.save(os.path.join(OUT, '15_中身_本命星一覧と納音.jpg'), quality=92)

# 16: 2027 year board
nen = crop(render('p18-19_交友メモと年盤.pdf'), (858, 138, 1200, 722))
square(nen, '2027年の年盤', '土用の期間や三合の方位も載っています', '16_中身_2027年の年盤.jpg')

# 17: fortune page — intro and 一白水星 readable, the rest softened (read it in the book)
un = crop(render('p102-103_あなたの運気.pdf'), (84, 62, 682, 930))
cut = round((405 - 62) / PREV)
lower = un.crop((0, cut, un.width, un.height)).filter(ImageFilter.GaussianBlur(9))
veil = Image.new('RGB', lower.size, (255, 255, 255))
un.paste(Image.blend(lower, veil, 0.35), (0, cut))
du = ImageDraw.Draw(un)
du.text((un.width // 2, cut + (un.height - cut) // 2), '続きは気学手帳で', font=F(SB, 70), fill=PURPLE, anchor='mm')
square(un, '2027年 あなたの運気', '九つの星ごとに、一年の運気とアドバイスです', '17_中身_2027年あなたの運気.jpg')
print('ok')
