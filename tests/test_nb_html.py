from pytest import raises, approx
from pathlib import Path
from pyglottolog import Glottolog

from pynumerals.numerals_html import NumeralsEntry
from pynumerals.number_parser import parse_number
from pynumerals.process_html import find_tables

raw_htmls = Path(__file__).parent / '../' / 'raw'

gl_repos = Path(__file__).parent / '../..' / 'glottolog'
glottolog = Glottolog(gl_repos)

gc_codes = glottolog.languoids_by_code()
gc_iso = glottolog.iso.languages

def test_find_tables():
    d = list(find_tables([raw_htmls / 'Abui.htm']))[0]
    assert len(d) == 7

def test_numeral_tables():
    d = list(find_tables([raw_htmls / 'Abui.htm']))[0]
    entry = NumeralsEntry(
        base_name=d[0],
        tables=d[1],
        file_name=d[2],
        title_name=d[3],
        codes=gc_codes,
        iso=gc_iso,
        source=d[4],
        base=d[5],
        comment=d[6],
    )
    assert len(entry.tables) == 8


def test_base_name():
    for f in [raw_htmls / 'Abui.htm', raw_htmls / 'Zoque-Copainala.htm', raw_htmls / 'Yimchungru-Naga.htm']:
        d = list(find_tables([f]))[0]
        entry = NumeralsEntry(
            base_name=d[0],
            tables=d[1],
            file_name=d[2],
            title_name=d[3],
            codes=gc_codes,
            iso=gc_iso,
            source=d[4],
            base=d[5],
            comment=d[6],
        )
        assert entry.base_name == Path(f).stem



def test_parse_number():
    with raises(ValueError):
        parse_number("No number in here!")
    with raises(ValueError):
        parse_number("1 foo")

    assert parse_number("1 ː") == 1
    assert parse_number("1,000.") == 1000
    assert parse_number("1,000.15 .") == 1000.15
    assert approx(parse_number("1,22:")) == 1.22


def test_fuzzy_number_matching():
    d = list(find_tables([raw_htmls / 'Aari.htm']))[0]
    entry = NumeralsEntry(
        base_name=d[0],
        tables=d[1],
        file_name=d[2],
        title_name=d[3],
        codes=gc_codes,
        iso=gc_iso,
        source=d[4],
        base=d[5],
        comment=d[6],
    )
    numeral_table = entry.tables[1]
    table_elements = numeral_table.find_all('tr')
    cell_content = []

    for row in table_elements:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]
        cell_content.append([ele for ele in cols if ele])

    # Table is roughly structured like this:
    # 1 | 21
    # 2 | 22
    # 3 | 23
    # ...
    # 10 | 30
    # ..
    # 20 | 2000

    assert parse_number(cell_content[0][0]) == 1
    assert parse_number(cell_content[0][1]) == 21
    assert parse_number(cell_content[9][0]) == 10
    assert parse_number(cell_content[19][1]) == 2000
