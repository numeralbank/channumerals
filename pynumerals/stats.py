"""
Calculate some informative stats about the origina Numeralbank HTM files.
"""

import os
import sys
from collections import Counter

from pynumerals.numerals_html import NumeralbankHTML

SKIP = ['How-to-view-EN.htm', 'How-to-view-CH.htm']


# 4556
def num_htm_files():
    htm_files = []

    for _, _, files in os.walk(sys.argv[1]):
        for f in files:
            if f.endswith('.htm') and f not in SKIP:
                htm_files.append(f)

    print(len(htm_files))


def num_tables():
    count_dict = {}

    for dirpath, _, files in os.walk(sys.argv[1]):
        for f in files:
            if f.endswith('.htm') and f not in SKIP:
                p = os.path.join(dirpath, f)
                nb_htm = NumeralbankHTML(p)
                count_dict[nb_htm.base_name] = len(nb_htm.numeralbank_tables)

    c = Counter(count_dict)
    print(c)


num_tables()
