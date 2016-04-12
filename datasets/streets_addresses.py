import luigi
from lib import histograph

from datasets import directory_1854
from datasets import centerlines
from datasets import building_inspector

title = 'Honden!!!!'

class Infer(histograph.Data):
    dataset = luigi.Parameter(default='streets-addresses')
    step = luigi.Parameter(default='infer')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return [
            building_inspector.Import(),
            centerlines.Import(),
            directory_1854.Import()
        ]

class Import(histograph.Import):
    dataset = luigi.Parameter(default='streets-addresses')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return Infer()
