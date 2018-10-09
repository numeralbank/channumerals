from bs4 import BeautifulSoup
from clldutils.path import walk
from number_parser import parse_number

TABLE_IDENTIFIER = 'MsoTableGrid'
SKIP = ['How-to-view-EN.htm', 'How-to-view-CH.htm']


def iterate_files():
    return [f if f.suffix == '.htm' and f.name not in SKIP else None for f in
            walk('raw/')]


def find_tables(files):
    for f in files:
        parsed = BeautifulSoup(f.read_text(), 'html.parser')

        # Returns (Language name, ResultSet) pairs. ResultSet is the set of
        # tables that have TABLE_IDENTIFIER.
        yield (f.stem, parsed.find_all('table', {'class': TABLE_IDENTIFIER}))


def parse_number_table(table):
    table_elements = table.find_all('tr')
    elements = []

    for row in table_elements:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        for ele in cols:
            if ele:
                elements.append(ele)

    return elements


def find_number_table(tables):
        for table in tables:
            for element in table:
                try:
                    parse_number(element)
                except ValueError:
                    continue
