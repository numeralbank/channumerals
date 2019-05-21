import attr

from pynumerals.glottocode_matcher import GlottocodeMatcher
from pynumerals.process_html import iterate_tables, find_ethnologue_codes
from pynumerals.number_parser import parse_number


@attr.s
class NumeralsEntry:
    base_name = attr.ib(default=None)
    tables = attr.ib(default=None)
    codes = attr.ib(default=None)
    iso = attr.ib(default=None)

    number_tables = attr.ib(init=False)
    other_tables = attr.ib(init=False)
    ethnologue_codes = attr.ib(init=False)
    glottocodes = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.number_tables, self.other_tables = iterate_tables(self.tables)
        self.ethnologue_codes = find_ethnologue_codes(self.other_tables)
        self.glottocodes = GlottocodeMatcher(
            self.base_name,
            ethnologue_codes=self.ethnologue_codes,
            codes=self.codes,
            iso=self.iso,
        ).candidates

    def get_numeral_lexemes(self):
        varieties = []

        for number_table in self.number_tables:
            n = {}

            for entry in number_table:
                try:
                    parsed_entry = parse_number(entry)
                except ValueError:  # Most likely runaway tables.
                    continue

                split_str = str(parsed_entry) + "."
                lex = list(filter(None, entry.split(split_str)))
                n[parsed_entry] = [clean.strip() for clean in lex]

            varieties.append(n)

        return varieties
