from fuzzywuzzy.fuzz import token_set_ratio as ts_ratio
import attr
import logging


@attr.s
class GlottocodeMatcher:
    base_name = attr.ib(default=None)
    threshhold = attr.ib(default=85)
    ethnologue_codes = attr.ib(default=None)
    codes = attr.ib(default=None)
    iso = attr.ib(default=None)
    candidates = attr.ib(init=False)

    def __attrs_post_init__(self):
        candidates = []

        if self.ethnologue_codes:
            candidates.append(self.codes[self.ethnologue_codes[0]].glottocode)
        else:
            for lang in self.iso:
                if ts_ratio(lang.name, self.base_name) >= self.threshhold:
                    try:
                        candidates.append(self.codes[lang.code].glottocode)
                    except KeyError:
                        logging.warning("Couldn't map: " + lang.code)

        self.candidates = candidates
