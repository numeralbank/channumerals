from pathlib import Path

import re

from bs4 import BeautifulSoup

from pynumerals.glottocode_matcher import GlottocodeMatcher


class NumeralbankHTML:
    """
    Programmatic access to Numeralbank HTM files.
    """

    # Pattern and pattern application taken from:
    # https://stackoverflow.com/questions/20157375/fuzzy-smart-number-parsing-in-python

    _pattern = r"""(?x)
        ^
        [^\d+-\.]*
        (?P<number>
            (?P<sign>[+-])?
            (?P<integer_part>
                \d{1,3}
                (?P<sep>
                    [ ,.]
                )
                \d{3}
                (?:
                    (?P=sep)
                    \d{3}
                )*
            |
                \d+
            )?
            (?P<decimal_part>
                (?P<point>
                    (?(sep)
                        (?!
                            (?P=sep)
                        )
                    )
                    [.,]
                )
                \d+
            )?
        )
        [^\d]*
        $
    """

    __table_identifier = 'MsoTableGrid'

    def __init__(self, htm_path):
        self.htm_path = Path(htm_path)
        self.base_name = self.htm_path.stem
        self.glcandidates = GlottocodeMatcher(self.base_name).candidates

        with open(htm_path, 'r') as numeralbank_htm:
            numeralbank_content = numeralbank_htm.read()

        numeralbank_res = BeautifulSoup(numeralbank_content, 'html.parser')

        self.numeralbank_tables = self.__get_tables__(numeralbank_res)

    # TODO: Use this for finding the numeral tables.
    def parse_number(self, text):
        match = re.match(self._pattern, text)
        if match is None or not (match.group("integer_part") or
                                 match.group("decimal_part")):
            raise ValueError("Couldn't find a number.")

        num_str = match.group("number")
        sep = match.group("sep")

        if sep:
            num_str = num_str.replace(sep, "")  # remove thousands separators

        if match.group("decimal_part"):
            point = match.group("point")
            if point != ".":
                # regularize decimal point
                num_str = num_str.replace(point, ".")
            return float(num_str)

        return int(num_str)

    def __get_tables__(self, soup_parse):
        return soup_parse.find_all('table', {'class': self.__table_identifier})

    def identify_tables(self, parsed_tables):
        pass
