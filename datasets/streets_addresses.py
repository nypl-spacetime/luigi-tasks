import luigi
import histograph

import directory_1854
import centerlines
import building_inspector

class Infer(histograph.Data):
    dataset = luigi.Parameter(default='streets-addresses')
    step = luigi.Parameter(default='infer')
    max_age = luigi.IntParameter(default=24 * 7)

    def requires(self):
        yield [
            building_inspector.Import(),
            centerlines.Import(),
            directory_1854.Import()
        ]

class Import(histograph.Import):
    dataset = luigi.Parameter(default='streets-addresses')
    max_age = luigi.IntParameter(default=24 * 7)

    def requires(self):
        yield Infer()
