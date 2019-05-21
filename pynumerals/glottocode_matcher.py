from fuzzywuzzy.fuzz import token_set_ratio as ts_ratio
import attr


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

        if self.ethnologue_codes and self.ethnologue_codes[0] in self.codes:
            candidates.append(self.codes[self.ethnologue_codes[0]].glottocode)
        else:
            candidates = [
                (
                    self.codes[l.code].glottocode,
                    ts_ratio(l.name, self.base_name),
                )
                for l in self.iso
                if l.code in self.codes
            ]

            candidates = sorted(
                [c for c in candidates if c[1] >= self.threshhold],
                key=lambda c: -c[1],
            )

            if candidates:
                candidates = [candidates[0][0]]

        self.candidates = candidates
