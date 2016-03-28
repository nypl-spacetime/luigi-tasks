import luigi
import histograph

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='wards')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield Download()

class Import(histograph.Import):
    dataset = luigi.Parameter(default='wards')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield Transform()
