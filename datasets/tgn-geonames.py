import luigi
import histograph

import geonames
import tgn

class Infer(histograph.Data):
    dataset = luigi.Parameter(default='tgn-geonames')
    step = luigi.Parameter(default='infer')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield [
            geonames.Import(),
            tgn.Import()
        ]

class Import(histograph.Import):
    dataset = luigi.Parameter(default='tgn-geonames')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield Infer
