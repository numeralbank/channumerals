from setuptools import setup
import sys
import json


with open('metadata.json', {'encoding': 'utf-8'}) as fp:
    metadata = json.load(fp)


setup(
    name='lexibank_numerals',
    description=metadata['title'],
    license=metadata.get('license', ''),
    url=metadata.get('url', ''),
    py_modules=['lexibank_numerals'],
    include_package_data=True,
    zip_safe=False,
    entry_points={
        'lexibank.dataset': [
            'numerals=pynumerals.lexibank:Dataset',
        ]
    },
    install_requires=[
        'cldfbench>=1.0.0',
        'clldutils>=3.5.0',
        'pylexibank>=2.1',
        'pyglottolog>=3.1.0',
        'beautifulsoup4>=4.6.3',
        'fuzzywuzzy',
        'pytest',
        'xlrd',
        'attrs',
    ]
)
