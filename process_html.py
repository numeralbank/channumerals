from bs4 import BeautifulSoup
from clldutils.path import walk

TABLE_IDENTIFIER = 'MsoTableGrid'
SKIP = ['How-to-view-EN.htm', 'How-to-view-CH.htm']


def iterate_files():
    return [f if f.suffix == '.htm' and f.name not in SKIP else None for f in
            walk('raw/')]


def find_tables(files):
    for f in files:
        parsed = BeautifulSoup(f.read_text())
        yield (f.name, parsed.find_all('table', {'class': TABLE_IDENTIFIER}))

