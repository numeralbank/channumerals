import xlrd
from clldutils.path import Path

HEADER = [
    'name', 'country', 'iso', 'glotto_name', 'glotto_code', 'lg_link',
    'audio', 'source', 'nr_sets', 'variant'
]


def iter_sheet_rows(sname, fname):
    wb = xlrd.open_workbook(Path(fname))
    sheet = wb.sheet_by_name(sname)

    for i in range(sheet.nrows):
        if i > 0:  # Skip header by default.
            yield [col.value for col in sheet.row(i)]


def get_meta_data(meta_s_name, fname):  # FIXME: to arguments in command etc.
    meta = {}

    for row in iter_sheet_rows('META', 'numerals.xlsx'):
        row = dict(zip(HEADER, row))
        meta[(row['lg_link'], row['variant'])] = row

    print(meta)
    return meta


def get_numerals():
    pass


get_meta_data('', '')
