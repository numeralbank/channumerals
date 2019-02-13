from fuzzywuzzy.fuzz import token_set_ratio
from pyglottolog.api import Glottolog
import attr

GL_API = Glottolog('/home/chrzyki/Repositories/clld/glottolog')


@attr.s
class GlottocodeMatcher:
    base_name = attr.ib(default=None)
    threshhold = attr.ib(default=90)
    candidates = attr.ib(init=False)

    def __attrs_post_init__(self):
        candidates = []

        for lang in GL_API.iso.languages:
            if token_set_ratio(lang.name, self.base_name) >= self.threshhold:
                candidates.append(lang)

        self.candidates = candidates
