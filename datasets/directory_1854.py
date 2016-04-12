import luigi
from lib import histograph

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='1854-directory')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

class Import(histograph.Import):
    dataset = luigi.Parameter(default='1854-directory')
    max_age = luigi.IntParameter(default=24 * 30)
    types = luigi.Parameter(default='pits')

    def requires(self):
        return Transform()
