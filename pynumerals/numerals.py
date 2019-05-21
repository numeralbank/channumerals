from pynumerals.numerals_html import NumeralsEntry
from pynumerals.process_html import get_file_paths, find_tables
import logging


def main():
    html_files = get_file_paths("raw/")
    # Get a generator for (BaseName, ResultSet) tuples.
    tables = find_tables(html_files)

    logging.basicConfig(filename="numerals.log", level=logging.DEBUG)

    for table_set in tables:
        entry = NumeralsEntry(base_name=table_set[0], tables=table_set[1])
        logging.info("Base name: " + entry.base_name)
        logging.info("Glottocodes:")
        logging.info(entry.glottocodes)
        logging.info("Numeral lexemes:")
        logging.info(entry.get_numeral_lexemes())
        logging.info("Other tables:")
        logging.info(entry.other_tables)
        logging.info("--------------------------------------------------------")


if __name__ == "__main__":
    main()
