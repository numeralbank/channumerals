from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables


class Dataset(BaseDataset):
    id = 'numerals'
    dir = Path(__file__).parent.parent

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):
        html_files = get_file_paths(self.raw)
        tables = find_tables(html_files)

        entries = []

        for table_set in tables:
            entry = NumeralsEntry(base_name=table_set[0], tables=table_set[1])
            entries.append(entry)

        with self.cldf as ds:
            meaning_map = {}

            for entry in entries:
                if entry.glottocodes:
                    ds.add_language(
                        ID=entry.glottocodes[0],
                        Name=entry.base_name,
                        Glottocode=entry.glottocodes[0]
                    )

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
                                    Name=str(k)
                                )
                            else:
                                ds.add_concept(
                                    ID=meaning_map[meaning_n],
                                    Name=str(k)
                                )

                            if v:
                                clean = v[0].replace('\n', '').replace('\t', '')
                                ds.add_lexemes(
                                    Value=clean,
                                    Parameter_ID=str(k),
                                    Language_ID=entry.glottocodes[0]
                                )
