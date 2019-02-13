import attr

from pynumerals.glottocode_matcher import GlottocodeMatcher


@attr.s
class NumeralsEntry:
    base_name = attr.ib(default=None)
    glottocode_candidates = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.glottocode_candidates =\
            GlottocodeMatcher(self.base_name).candidates
