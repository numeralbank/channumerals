import re

import attr
from clldutils.path import Path
from clldutils.text import split_text_with_context
from pylexibank.dataset import Dataset as BaseDataset
from pylexibank.models import Lexeme, Language
from pylexibank.forms import FormSpec
from pylexibank.util import progressbar

from helper import int_to_en
from numerals_html import NumeralsEntry
from process_html import get_file_paths, find_tables
from value_parser import value_parser

from errorcheck import errorchecks


@attr.s
class NumeralsLanguage(Language):
    SourceFile = attr.ib(default=None)
    Contributor = attr.ib(default=None)
    Base = attr.ib(default=None)
    Comment = attr.ib(default=None)


@attr.s
class NumeralsLexeme(Lexeme):
    Problematic = attr.ib(
            init=False,
            validator=attr.validators.optional(attr.validators.instance_of(bool)))
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

    id = "channumerals"
    dir = Path(__file__).parent.parent

    lexeme_class = NumeralsLexeme
    language_class = NumeralsLanguage

    form_spec = FormSpec(
        brackets={
            "(": ")",
            "{": "}",
            "[": "]",
            "（": "）",
            "【": "】",
            "『": "』",
            "«": "»",
            "⁽": "⁾",
            "₍": "₎"
        },
        replacements=[],
        separators=(";", "/", ","),
        missing_data=('?', '-'),
        strip_inside_brackets=False,
        first_form_only=False,
        normalize_whitespace=True,
        normalize_unicode=None,
    )

    def cmd_download(self, args):
        pass

    def cmd_makecldf(self, args):

        unknown_gc_cnt = 0

        html_files = get_file_paths(self.raw_dir)
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

        # with args.writer.cldf as ds:
        meaning_map = {}

        args.writer.add_sources(*self.raw_dir.read_bib())
        args.writer.cldf['FormTable', 'Problematic'].datatype.base = 'boolean'

        # remove newly added columns in order to get a good diff
        args.writer.cldf['FormTable'].tableSchema.columns = [
            c for c in args.writer.cldf['FormTable'].tableSchema.columns
            if c.name != 'Graphemes' and c.name != 'Profile']

        # map old lang_ids (without 'MsoNormalTable' table class)
        # against new ones to minimize diffs
        lang_id_map = {
            "hupd1244-4": ["hupd1244-2", 2-1],
            "hupd1244-2": ["hupd1244-3", 3-1],
            "hupd1244-3": ["hupd1244-4", 4-1],

            "nucl1440-2": ["nucl1440-1", 1-1],
            "nucl1440-3": ["nucl1440-2", 2-1],
            "nucl1440-1": ["nucl1440-3", 3-1],

            "poum1235-2": ["poum1235-1", 1-1],
            "poum1235-1": ["poum1235-2", 2-1],

            "wayu1241-1": ["wayu1241-2", 2-1],
            "wayu1241-2": ["wayu1241-1", 1-1],

            "port1283-1": ["port1283-2", 2-1],
            "port1283-2": ["port1283-1", 1-1],
        }

        for entry in progressbar(entries, desc="makecldf"):
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

                    # map 'old' glottocodes against new one
                    # to minimize diff
                    if lg_name == 'Enlhet (Lengua), Paraguay':
                        entry.glottocodes = ['leng1262']
                    if lg_name == 'Gerai, Indonesia':
                        entry.glottocodes = ['sema1269']

                    if not entry.glottocodes:
                        unknown_gc_cnt += 1
                        gc = ''
                        lang_id_prefix = 'xxxx%04d' % (unknown_gc_cnt)
                    else:
                        lang_id_prefix = entry.glottocodes[0]
                        gc = lang_id_prefix

                    if lg_name not in seen_lg_names:
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

                    if lang_id_prefix not in lg_variant_counter:
                        lg_variant_counter[lang_id_prefix] = 0
                    lg_variant_counter[lang_id_prefix] += 1
                    c_lang_id = "%s-%i" % (
                        lang_id_prefix, lg_variant_counter[lang_id_prefix])

                    # map according to old table parser without 'MsoNormalTable'
                    if c_lang_id in lang_id_map:
                        c_lang_id, var_id = lang_id_map[c_lang_id]

                    args.writer.add_language(
                        ID=c_lang_id,
                        Name=lg_name,
                        Glottocode=gc,
                        ISO639P3code=entry.ethnologue_codes[0],
                        SourceFile=entry.file_name,
                        Latitude="",
                        Longitude="",
                        Macroarea="",
                        Family="",
                        Glottolog_Name="",
                        Contributor=contrib,
                        Base=base,
                        Comment=com,
                    )

                    for k, vs in var.items():
                        meaning_n = str(k)
                        for v in vs:

                            if meaning_n not in meaning_map:
                                meaning_map[meaning_n] = str(k)
                            args.writer.add_concept(
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
                                if '=' in value and '(' not in value:
                                    value = re.sub(
                                        r'^(.*?)\s(\S+\s*=\s*IPA.*)$', '\\1 (\\2)', value)

                                value, comment, other_form, loan = value_parser(value)

                                if value:
                                    args.writer.add_forms_from_value(
                                        Value=value,
                                        Parameter_ID=meaning_n,
                                        Variant_ID=(var_id+1),
                                        Language_ID=c_lang_id,
                                        Comment=comment,
                                        Source="chan2019",
                                        Other_Form=other_form,
                                        Loan=loan,
                                    )

            def _x(s):
                try:
                    return int(s)
                except ValueError:
                    return s

            args.writer.objects['FormTable'] = sorted(
                args.writer.objects['FormTable'],
                key=lambda item: ([_x(i) for i in item['ID'].split('-')]))
            args.writer.objects['LanguageTable'] = sorted(
                args.writer.objects['LanguageTable'],
                key=lambda item: ([_x(i) for i in item['ID'].split('-')]))
            args.writer.objects['ParameterTable'] = sorted(
                args.writer.objects['ParameterTable'],
                key=lambda item: _x(item['ID']))
