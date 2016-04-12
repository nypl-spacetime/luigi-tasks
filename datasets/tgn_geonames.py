import luigi
from lib import histograph

from datasets import geonames
from datasets import tgn

class Infer(histograph.Data):
    dataset = luigi.Parameter(default='tgn-geonames')
    step = luigi.Parameter(default='infer')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return [
            geonames.Import(),
            tgn.Import()
        ]

class Import(histograph.Import):
    dataset = luigi.Parameter(default='tgn-geonames')
    max_age = luigi.IntParameter(default=24 * 30)
    types = luigi.Parameter(default='relations')

    def requires(self):
        return Infer()
