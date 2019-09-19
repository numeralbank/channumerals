import re

import attr
from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Lexeme

from pynumerals.helper import int_to_en
from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables

from errorcheck import errorchecks


@attr.s
class NumeralsLexeme(Lexeme):
    SourceFile = attr.ib(default=None)
    Problematic = attr.ib(init=False)

    def __attrs_post_init__(self):
        self.Problematic = False
        for check in errorchecks:
            if check(self.Value):
                self.Problematic = True
                break
        
        
        

class Dataset(BaseDataset):
    # TODO: Change splitting class.

    id = "channumerals"
    dir = Path(__file__).parent.parent

    lexeme_class = NumeralsLexeme

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):
        html_files = get_file_paths(self.raw)
        tables = find_tables(html_files)
        glottolog_codes = self.glottolog.languoids_by_code()
        glottolog_iso = self.glottolog.iso.languages
        concept_map = {cs.gloss: cs.id for cs in self.concepticon.conceptsets.values()}

        for concept in self.concepts:
            concept_map[concept["GLOSS"]] = concept["CONCEPTICON_ID"]

        entries = []

        for table_set in tables:
            entry = NumeralsEntry(
                base_name=table_set[0],
                tables=table_set[1],
                file_name=table_set[2],
                codes=glottolog_codes,
                iso=glottolog_iso,
            )
            entries.append(entry)

        with self.cldf as ds:
            meaning_map = {}

            for entry in entries:
                if entry.glottocodes:
                    ds.add_language(
                        ID=entry.glottocodes[0],
                        Name=entry.base_name,
                        Glottocode=entry.glottocodes[0],
                    )
                else:
                    if len(entry.get_numeral_lexemes()):
                        print("No glottocode for %s" % (entry.base_name))

            for entry in entries:
                number_lexemes = entry.get_numeral_lexemes()

                for variety in number_lexemes:
                    if entry.glottocodes:
                        for k, v in variety.items():
                            meaning_n = str(k)

                            if meaning_n not in meaning_map:
                                meaning_map[meaning_n] = str(k)

                                ds.add_concept(
                                    ID=meaning_map[meaning_n],
                                    Name=str(k),
                                    Concepticon_ID=concept_map.get(int_to_en(k).upper()),
                                )
                            else:
                                ds.add_concept(
                                    ID=meaning_map[meaning_n],
                                    Name=str(k),
                                    Concepticon_ID=concept_map.get(int_to_en(k).upper()),
                                )

                            if v:
                                value = v[0].replace("\n", "").replace("\t", "")
                                m = re.search(r'\(([^)]+)', value)

                                if m:
                                    comment = m.group(1).strip()
                                    value = value.split("(")
                                    value = value[0]
                                else:
                                    comment = None

                                ds.add_lexemes(
                                    Value=value,
                                    Parameter_ID=str(k),
                                    Language_ID=entry.glottocodes[0],
                                    Comment=comment,
                                    SourceFile=entry.file_name,
                                    Problematic=check(value)
                                )
