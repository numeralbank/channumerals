from bs4 import BeautifulSoup
from clldutils.path import walk
from pynumerals.number_parser import parse_number

TABLE_IDENTIFIER = 'MsoTableGrid'
SKIP = ['How-to-view-EN.htm', 'How-to-view-CH.htm']


def get_file_paths(raw_htmls):
    """
    Build a list of PosixPath() objects for all files in the specified
    directory, e.g. numerals/raw/, skipping files defined in SKIP.
    :param raw_htmls: Path to raw numerals HTML files.
    :return: A list of PosixPath() objects with path information for the files.
    """
    return [f if f.suffix == '.htm' and f.name not in SKIP
            else None for f in walk(raw_htmls)]


def find_tables(file_paths):
    """
    Find all tables defined by TABLE_IDENTIFIER in file_paths.
    :param file_paths: A list of PosixPath() objects containing path information
    for the numerals HTML files.
    :return: A generator with pairs of (LanguageName, ResultSet). If ResultSet
    is empty, there was no table defined in TABLE_IDENTIFIER in the
    corresponding HTML file.
    """
    for f in file_paths:
        if f:
            parsed = BeautifulSoup(f.read_text(), 'html.parser')
            yield (f.stem,
                   parsed.find_all('table', {'class': TABLE_IDENTIFIER}))


def find_number_table(table):
    """
    A helper function to identify tables containing number information so that
    we don't have to rely on the (implicit) ordering of tables within the HTML
    files.
    :param table: The tables from a ResultSet to be processed.
    :return: True if number table (>= 10 numerals), False otherwise.
    """
    numbers = []

    for element in table:
        try:
            # We collect all potential numbers in a list and simply check
            # the length of the list at the end.
            numbers.append(parse_number(element))
        except ValueError:  # TODO: Log exceptions and/or potential problems.
            continue

    # TODO: Check the sanity of this assumption.
    # We assume that we've found a number table if the list of numbers is >= 10.
    if len(numbers) >= 10:
        return True
    else:
        return False


def parse_table(table):
    """
    A helper function to parse tables into a list of strings. This used to
    make identifying tables containing numerals easier.
    :param table: A numerals HTML table.
    :return: A list of strings with the elements and other literal information.
    """
    table_elements = table.find_all('tr')
    elements = []

    for row in table_elements:
        cols = row.find_all('td')
        cols = [ele.text.strip() for ele in cols]

        for ele in cols:
            if ele:
                elements.append(ele)

    return elements


def iterate_tables(tables):
    for table in tables:
        parsed_table = parse_table(table)

        if find_number_table(parsed_table) is True:
            _ = parse_table(table)
