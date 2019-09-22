import re

import attr
from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Lexeme

from pynumerals.helper import int_to_en
from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables
from pynumerals.value_parser import value_parser

from pynumerals.errorcheck import errorchecks


@attr.s
class NumeralsLexeme(Lexeme):
    SourceFile = attr.ib(default=None)
    Problematic = attr.ib(init=False)
    Other_Form = attr.ib(default=None)
    Variant_ID = attr.ib(default=1)

    def __attrs_post_init__(self):
        self.Problematic = False
        for check in errorchecks:
            if check(self.Value):
                self.Problematic = True
                break
        if not self.Problematic and self.Other_Form and '<' in self.Other_Form:
            self.Problematic = True


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
                        for var_id, var in variety.items():
                            for k, vs in var.items():
                                meaning_n = str(k)
                                for v in vs:
                                    if meaning_n not in meaning_map:
                                        meaning_map[meaning_n] = str(k)

                                        ds.add_concept(
                                            ID=meaning_map[meaning_n],
                                            Name=meaning_n,
                                            Concepticon_ID=concept_map.get(int_to_en(k).upper()),
                                        )
                                    else:
                                        ds.add_concept(
                                            ID=meaning_map[meaning_n],
                                            Name=meaning_n,
                                            Concepticon_ID=concept_map.get(int_to_en(k).upper()),
                                        )

                                    if v:
                                        value = v.replace("\n", "").replace("\t", "")
                                        # after 2 or more non break spaces follows a comment
                                        if '(' not in value:
                                            value = re.sub(r'^(.*?) {2,}(.*)$', '\\1 (\\2)', value)
                                        # after an em dash follows a comment
                                        if '(' not in value:
                                            value = re.sub(r'^(.*?)\s*–\s*(.*)$', '\\1 (\\2)', value)
                                        # replace non break space by spaces
                                        value = value.replace(" ", " ")
                                        # put single string 'foo = IPA' into brackets
                                        if '=' in value and not '(' in value:
                                            value = re.sub(r'^(.*?)\s(\S+\s*=\s*IPA.*)$', '\\1 (\\2)', value)

                                        value, comment, other_form, loan = value_parser(value)

                                        if value:
                                            ds.add_lexemes(
                                                Value=value,
                                                Parameter_ID=meaning_n,
                                                Variant_ID = (var_id+1),
                                                Language_ID=entry.glottocodes[0],
                                                Comment=comment,
                                                SourceFile=entry.file_name,
                                                Other_Form = other_form,
                                                Loan = loan
                                            )
