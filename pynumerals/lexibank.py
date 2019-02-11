from clldutils.path import Path
from pylexibank.dataset import Dataset as BaseDataset


class Dataset(BaseDataset):
    id = 'numerals'
    dir = Path(__file__).parent.parent

    def cmd_download(self, **kw):
        pass

    def cmd_install(self, **kw):
        with self.cldf as ds:
            _ = ds
