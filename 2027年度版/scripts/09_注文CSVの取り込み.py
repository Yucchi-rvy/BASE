"""BASEの注文CSV（Shift-JIS）から、販売管理表の「注文明細」に貼る行を作る。

お客様の名前・住所・電話・メールは読み出さない。2027年度版の8商品だけを対象にする。
使い方:  python3 09_注文CSVの取り込み.py <BASEの注文CSV>
出力は タブ区切り（注文日, 注文ID, 商品, 数量, 単価, 発送状況, メモ=支払い方法）。
"""
import csv, io, sys

ITEMS = {
    '167191732': '気学手帳',
    '167191785': '気学手帳ポケット版',
    '167191758': '気学カレンダー',
    '167191795': '手帳＆ポケット版セット',
    '167191767': '手帳＆カレンダーセット',
    '167191806': '気学グッズフルセット',
    '167191747': '手帳5冊＋1冊プレゼント',
    '167191722': 'ポスターカレンダー「邂逅」',
}
STATUS = {'未発送': '未発送', '発送済み': '発送済み', 'キャンセル': 'キャンセル'}

raw = open(sys.argv[1], 'rb').read().decode('cp932')
rows = list(csv.reader(io.StringIO(raw)))
h = rows[0]
col = {k: h.index(k) for k in ['注文ID', '注文日時', '商品ID', '数量', '価格', '発送状況', '支払い方法']}
skipped = 0
for r in rows[1:]:
    if not r:
        continue
    name = ITEMS.get(r[col['商品ID']])
    if not name:
        skipped += 1
        continue
    date = r[col['注文日時']][:10].replace('-', '/')
    print('\t'.join([date, r[col['注文ID']], name, r[col['数量']], r[col['価格']],
                     STATUS.get(r[col['発送状況']], r[col['発送状況']]), r[col['支払い方法']]]))
print(f'# 対象外の行（2027年度版以外の商品）: {skipped}', file=sys.stderr)
