from bs4 import BeautifulSoup
from clldutils.path import walk
from pynumerals.number_parser import parse_number
import re

TABLE_IDENTIFIER = ["MsoTableGrid", "a"]
SKIP = [
    "How-to-view-EN.htm",
    "How-to-view-CH.htm",
    "problem.html",
    "index.html",
    "index_old.html",
    "eugenechan.htm",
    "home-Chinese.html",
    "home.html",
    "Comments-6-Oct-2008.htm",
    "blank.html",
    # all files which have <ol type="A"> are overview pages:
    "African-Others.htm",
    "Afro-Asiatic.htm",
    "Algic.htm",
    "Altaic.htm",
    "American-North-Cent-Others.htm",
    "American-Others.htm",
    "American-South-Others.htm",
    "Arawakan.htm",
    "Australian.htm",
    "AustroAsiatic.htm",
    "Austronesian-Central.htm",
    "Austronesian-Eastern.htm",
    "Austronesian-Western.htm",
    "Austronesian.htm",
    "Barbacoan.htm",
    "Carib.htm",
    "Caucasian.htm",
    "Central-South-NewGuinea-Kutubuan.htm",
    "Chibchan.htm",
    "Choco.htm",
    "Dravidian.htm",
    "East-New-Guinea-Highlands.htm",
    "East-Papuan.htm",
    "Easternl Austronesian.htm",
    "Eskimo-Aleut.htm",
    "Euro-Asian-Others.htm",
    "Eyak-Athabaskan.htm",
    "Geelvink-Bay.htm",
    "Hokan.htm",
    "Huon-Finisterre.htm",
    "Indoeuro.htm",
    "Iroquoian.htm",
    "Jean-Ge.htm",
    "Kainantu-Goroka.htm",
    "Khoisan.htm",
    "Macro-Ge.htm",
    "Madang-Adelbert-Range.htm",
    "Mataco-Guaicuru.htm",
    "Matacoan.htm",
    "Mayan.htm",
    "Miao-Yao.htm",
    "Mixe-Zoque.htm",
    "Muskogean.htm",
    "Na-Dene.htm",
    "Niger-Congo-Adamawa.htm",
    "Niger-Congo-Atlantic.htm",
    "Niger-Congo-Benue-Congo.htm",
    "Niger-Congo-Grassfield.htm",
    "Niger-Congo-Gur.htm",
    "Niger-Congo-Kwa.htm",
    "Niger-Congo-Mande.htm",
    "Niger-Congo-Narrow-Bantu.htm",
    "Niger-Congo.htm",
    "Nilo-Saharan.htm",
    "Ok-Awyu.htm",
    "Oto-Manguean.htm",
    "Paezan.htm",
    "Panoan.htm",
    "Papuan-Others.htm",
    "Penutian.htm",
    "Quechuan.htm",
    "Ramu-Lower-Sepik.htm",
    "Salishan.htm",
    "Sepi-Ramu.htm",
    "Sepik-New.htm",
    "Sino-Tibetan.htm",
    "Siouan.htm",
    "South-Birds-Head-Timor-Alor-Pantar.htm",
    "Southeast-Papuan.htm",
    "Tacanan.htm",
    "Tai-Kadai.htm",
    "Torricelli.htm",
    "Totonacan.htm",
    "Trans-Fly-Bulaka-River.htm",
    "Trans-New Guinea.htm",
    "Tucanoan.htm",
    "Tupi.htm",
    "Uralic.htm",
    "Uto-Aztecan.htm",
    "West-Papuan.htm",
    "West-Timor-Alor-Pantar.htm",
    "Westpapuan-Timor-Alor-Pantar.htm",
    "Witotoan.htm",
    "Yuman.htm",
    ]
SKIP_RE = re.compile(r"(?i)question")

ETHNOLOGUE = re.compile(r"(:?(http[s]?://)?www|archive)\.ethnologue\.(?:com|org)/", re.IGNORECASE)

CODE_PATTERNS = [
    re.compile("code=(?P<code>[a-zA-Z]{3})"),
    re.compile("language/(?P<code>[a-zA-Z]{3})"),
]


def get_file_paths(raw_htmls, n=None):
    """
    Build a sorted list of PosixPath() objects for all files in the specified
    directory, e.g. numerals/raw/, skipping files defined in SKIP and as SKIP_RE.
    :param raw_htmls: Path to raw numerals HTML files.
    :param n: How many HTML files to process, useful for debugging.
    :return: A list of PosixPath() objects with path information for the files.
    """
    if n:
        return sorted(
            [f for f in walk(raw_htmls) if\
                f.suffix.startswith(".htm") and\
                f.name not in SKIP and\
                not re.search(SKIP_RE, f.name)]
        )[:n]
    else:
        return sorted(
            [f for f in walk(raw_htmls) if\
                f.suffix.startswith(".htm") and\
                f.name not in SKIP and\
                not re.search(SKIP_RE, f.name)]
        )


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
        parsed = BeautifulSoup(f.read_text(), "html.parser")
        yield (f.stem, parsed.find_all("table", {"class": TABLE_IDENTIFIER}), f.name)


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
        except ValueError:
            pass

    if len(numbers):
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
    table_elements = table.find_all("tr")
    elements = []

    for row in table_elements:
        cols = row.find_all("td")
        cols = [ele.text.strip() for ele in cols]

        for ele in cols:
            if ele:
                elements.append(ele)

    return elements


def iterate_tables(tables):
    number_tables = []
    other_tables = []

    for table in tables:
        parsed_table = parse_table(table)

        if find_number_table(parsed_table) is True:
            number_tables.append(parsed_table)
        else:
            other_tables.append(table)

    return number_tables, other_tables


def find_ethnologue_codes(tables):
    """
    Takes a set of tables (preferably other_tables from a NumeralsEntry object)
    and tries to find Ethnologue links and their corresponding codes for better
    matching of Glottocodes.
    :param tables: A set of tables (or a single table) from parsing a numerals
    HTML entry.
    :return: A list of Ethnologue codes found on the respective site.
    """
    ethnologue_codes = []

    for table in tables:
        link = table.find("a", href=ETHNOLOGUE)
        if link:
            for pattern in CODE_PATTERNS:
                m = pattern.search(link["href"])
                if m:
                    ethnologue_codes.append(m.group("code").lower())
                    break
            else:
                print(link["href"])

    return ethnologue_codes
