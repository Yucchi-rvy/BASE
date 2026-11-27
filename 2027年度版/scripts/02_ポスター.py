"""ポスターのPDFから 04_ポスター全体 と 06/07_作品アップ を作る（pdftoppm が必要）。"""
import sys
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os, subprocess, tempfile
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PDF = os.path.join(ROOT, '元データ', 'ポスター_邂逅2027_ver3.pdf')
OUT = os.path.join(ROOT, '画像')
tmp = tempfile.mkdtemp()
subprocess.run(['pdftoppm', '-r', '200', '-png', '-singlefile', PDF, os.path.join(tmp, 'poster')], check=True)
src = os.path.join(tmp, 'poster.png')
SB = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Bold.ttc'
SR = '/usr/share/fonts/opentype/noto/NotoSerifCJK-Regular.ttc'
F = lambda p, n: ImageFont.truetype(p, n, index=0)
im = Image.open(src).convert('RGB')
k = im.width / 1615.75
pt = lambda v: round(v * k)
# B2 trim (515x728mm) centred on the page
poster = im.crop((pt(77.97), pt(102.06), pt(1537.80), pt(2165.66)))
p = poster.copy(); p.thumbnail((1600, 2300), Image.LANCZOS)
p.save(f'{OUT}/04_ポスター全体_邂逅2027.jpg', quality=92)

# detail crops of the artwork (preview coords at 900px width -> full)
s = im.width / 900
for name, (x0, y0, side) in {'06_作品アップ1_邂逅.jpg': (275, 100, 350), '07_作品アップ2_邂逅.jpg': (232, 385, 435)}.items():
    c = im.crop((round(x0 * s), round(y0 * s), round((x0 + side) * s), round((y0 + side) * s)))
    c = c.resize((1200, 1200), Image.LANCZOS)
    c.save(f'{OUT}/{name}', quality=92)
print(poster.size)
