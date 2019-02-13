import attr

from pynumerals.glottocode_matcher import GlottocodeMatcher
from pynumerals.process_html import iterate_tables


@attr.s
class NumeralsEntry:
    base_name = attr.ib(default=None)
    tables = attr.ib(default=None)
    glottocode_candidates = attr.ib(init=False)
    number_tables = attr.ib(init=False)
    other_tables = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.glottocode_candidates =\
            GlottocodeMatcher(self.base_name).candidates

        self.number_tables, self.other_tables = iterate_tables(self.tables)
