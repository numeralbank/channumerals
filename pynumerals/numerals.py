from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables
import logging


def main():
    html_files = get_file_paths('raw/')
    tables = find_tables(html_files)

    logging.basicConfig(filename='numerals.log', level=logging.DEBUG)

    for table_set in tables:
        entry = NumeralsEntry(base_name=table_set[0])
        logging.info("Base name: " + entry.base_name)
        logging.info(entry.glottocode_candidates)


if __name__ == '__main__':
    main()
