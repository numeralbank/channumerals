from pytest import raises, approx

from pynumerals.numerals_html import NumeralbankHTML


def test_table_number():
    # FIXME: non-static path
    html = NumeralbankHTML('original_htm_files/Abui.htm')

    assert len(html.numeralbank_tables) == 4


def test_base_name():
    html_abui = NumeralbankHTML('original_htm_files/Abui.htm')
    html_zoque = NumeralbankHTML('original_htm_files/Zoque-Copainala.htm')
    html_yim = NumeralbankHTML('original_htm_files/Yimgchungru Naga.htm')

    assert html_abui.base_name == 'Abui'
    assert html_zoque.base_name == 'Zoque-Copainala'
    assert html_yim.base_name == 'Yimgchungru Naga'


def test_fuzzy_number_matching():
    html_aari = NumeralbankHTML('original_htm_files/Aari.htm')
    numeral_table = html_aari.numeralbank_tables[1]
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

    assert html_aari.parse_number(cell_content[0][0]) == 1
    assert html_aari.parse_number(cell_content[0][1]) == 21
    assert html_aari.parse_number(cell_content[9][0]) == 10
    assert html_aari.parse_number(cell_content[19][1]) == 2000

    with raises(ValueError):
        html_aari.parse_number("No number in here!")

    assert html_aari.parse_number("1,000") == 1000
    assert html_aari.parse_number("1,000.15") == 1000.15
    assert approx(html_aari.parse_number("1,22")) == 1.22


def test_identify_tables():
    html_aari = NumeralbankHTML('original_htm_files/Aari.htm')
    html_aari.identify_tables(html_aari.numeralbank_tables)
