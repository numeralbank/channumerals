from fuzzywuzzy.fuzz import token_set_ratio as ts_ratio
from pyglottolog.api import Glottolog
import attr
import logging

GL_API = Glottolog('/home/chrzyki/Repositories/clld/glottolog')
CODES = GL_API.languoids_by_code()


@attr.s
class GlottocodeMatcher:
    base_name = attr.ib(default=None)
    threshhold = attr.ib(default=85)
    ethnologue_codes = attr.ib(default=None)
    candidates = attr.ib(init=False)

    def __attrs_post_init__(self):
        candidates = []

        if self.ethnologue_codes:
            candidates.append(CODES[self.ethnologue_codes[0]].glottocode)
        else:
            for lang in GL_API.iso.languages:
                if ts_ratio(lang.name, self.base_name) >= self.threshhold:
                    try:
                        candidates.append(CODES[lang.code].glottocode)
                    except KeyError:
                        logging.warning("Couldn't map: " + lang.code)
                        pass

        self.candidates = candidates
