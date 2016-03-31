import luigi
import histograph

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='centerlines')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

class Import(histograph.Import):
    dataset = luigi.Parameter(default='centerlines')
    max_age = luigi.IntParameter(default=24 * 30)
    types = luigi.Parameter(default='pits')

    def requires(self):
        yield Transform()
