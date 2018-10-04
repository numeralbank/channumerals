# coding=utf-8
from __future__ import unicode_literals, print_function

from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset
from subprocess import call


class Dataset(BaseDataset):
    dir = Path(__file__).parent
    id = 'numerals'

    def cmd_download(self, **kw):
        call(["wget", "--mirror", "--convert-links", "--adjust-extension",
              "--page-requisites", "-P", "raw", '-nd', '-q',
              "https://mpi-lingweb.shh.mpg.de/numeral/"])

    def cmd_install(self, **kw):
        with self.cldf as _:
            pass
