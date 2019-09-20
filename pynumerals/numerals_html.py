import attr
import re

from pynumerals.glottocode_matcher import GlottocodeMatcher
from pynumerals.process_html import iterate_tables, find_ethnologue_codes
from pynumerals.number_parser import parse_number
from clldutils.text import split_text_with_context

_BRACKETS = {
    "(": ")",
    "{": "}",
    "[": "]",
    "‘": "’",
}

@attr.s
class NumeralsEntry:
    base_name = attr.ib(default=None)
    file_name = attr.ib(default=None)
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

        # Clean-up
        del self.ethnologue_codes
        del self.codes
        del self.iso

    def get_numeral_lexemes(self):
        varieties = []

        for i, number_table in enumerate(self.number_tables):
            n = {}
            n[i] = {}
            for entry in number_table:
                try:
                    parsed_entry = parse_number(entry)
                except ValueError:  # Most likely runaway tables.
                    continue

                p = re.compile("%s\s*\.\s*" % (str(parsed_entry)))
                e = p.sub('', entry)
                e = re.sub('\s~\s', '/', e) # split alternative forms
                e = re.sub('/n$', '(n)', e)
                lex = list(filter(None, split_text_with_context(e, separators='/,;', brackets=_BRACKETS)))
                n[i][parsed_entry] = [clean.strip() for clean in lex]

            varieties.append(n)

        return varieties
