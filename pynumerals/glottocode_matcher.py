from fuzzywuzzy.fuzz import token_set_ratio
from pyglottolog.api import Glottolog

GL_API = Glottolog('/home/chrzyki/Repositories/clld/glottolog')


class GlottocodeMatcher:
    def __init__(self, base_name, threshhold=90):
        self.base_name = base_name
        self.threshhold = threshhold
        self.candidates = self.__get_candidates__()

    def __get_candidates__(self):
        candidates = []

        for lang in GL_API.iso.languages:
            if token_set_ratio(lang.name, self.base_name) >= self.threshhold:
                candidates.append(lang)

        return candidates
