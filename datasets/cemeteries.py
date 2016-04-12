import luigi
from lib import histograph

class Download(histograph.Data):
    dataset = luigi.Parameter(default='cemeteries')
    step = luigi.Parameter(default='download')
    max_age = luigi.IntParameter(default=24 * 30)

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='cemeteries')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return Download()

class Import(histograph.Import):
    dataset = luigi.Parameter(default='cemeteries')
    max_age = luigi.IntParameter(default=24 * 30)
    types = luigi.Parameter(default='pits')

    def requires(self):
        return Transform()
