import re

import attr
from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.dataset import Lexeme, Language

from pynumerals.helper import int_to_en
from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables
from pynumerals.value_parser import value_parser

from pynumerals.errorcheck import errorchecks


@attr.s
class NumeralsLanguage(Language):
    SourceFile = attr.ib(default=None)
    Contributor = attr.ib(default=None)
    Base = attr.ib(default=None)
    Comment = attr.ib(default=None)

@attr.s
class NumeralsLexeme(Lexeme):
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
    language_class = NumeralsLanguage

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):

        unknown_gc_cnt = 0

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
                title_name=table_set[3],
                source=table_set[4],
                base=table_set[5],
                comment=table_set[6],
            )
            entries.append(entry)

        seen_lg_names = {}
        lg_variant_counter = {}

        with self.cldf as ds:
            meaning_map = {}

            for entry in entries:
                number_lexemes = entry.get_numeral_lexemes()

                for variety in number_lexemes:

                    for var_id, var in variety.items():

                        # build language name
                        if var_id < len(entry.title_name):
                            lg_name = entry.title_name[var_id]
                        elif len(entry.title_name):
                            lg_name = entry.title_name[0]
                        else:
                            lg_name = entry.base_name

                        if not entry.ethnologue_codes:
                            entry.ethnologue_codes = ['']

                        if not entry.glottocodes:
                            unknown_gc_cnt += 1
                            gc = ''
                            lang_id_prefix = 'xxxx%04d' % (unknown_gc_cnt)
                        else:
                            lang_id_prefix = entry.glottocodes[0]
                            gc = lang_id_prefix

                        if not lg_name in seen_lg_names:
                            seen_lg_names[lg_name] = []
                        seen_lg_names[lg_name].append(entry.file_name)

                        # build Contributor name
                        if var_id < len(entry.source):
                            contrib = entry.source[var_id]
                        else:
                            contrib = None

                        # build Base
                        if var_id < len(entry.base):
                            base = entry.base[var_id]
                        else:
                            base = None

                        # build Comment
                        if var_id < len(entry.comment):
                            com = entry.comment[var_id]
                        else:
                            com = ''

                        if len(set(seen_lg_names[lg_name])) > 1:
                            com = "CHECK with %s: %s" % (entry.file_name, com)

                        if not lang_id_prefix in lg_variant_counter:
                            lg_variant_counter[lang_id_prefix] = 0
                        lg_variant_counter[lang_id_prefix] += 1

                        ds.add_language(
                            ID="%s-%i" % (lang_id_prefix, lg_variant_counter[lang_id_prefix]),
                            Name=lg_name,
                            Glottocode=gc,
                            ISO639P3code=entry.ethnologue_codes[0],
                            SourceFile=entry.file_name,
                            Contributor=contrib,
                            Base=base,
                            Comment=com,
                        )

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
                                            Language_ID="%s-%i" % (lang_id_prefix, lg_variant_counter[lang_id_prefix]),
                                            Comment=comment,
                                            Other_Form = other_form,
                                            Loan = loan,
                                        )

            def _x(s):
                try:
                    return int(s)
                except:
                    return s

            ds.objects['FormTable'] = sorted(ds.objects['FormTable'],
                    key=lambda item: ([_x(i) for i in item['ID'].split('-')]))
            ds.objects['LanguageTable'] = sorted(ds.objects['LanguageTable'],
                    key=lambda item: ([_x(i) for i in item['ID'].split('-')]))
            ds.objects['ParameterTable'] = sorted(ds.objects['ParameterTable'],
                    key=lambda item: _x(item['ID']))
