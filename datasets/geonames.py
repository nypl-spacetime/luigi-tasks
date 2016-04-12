import luigi
from lib import histograph

class Download(histograph.Data):
    dataset = luigi.Parameter(default='geonames')
    step = luigi.Parameter(default='download')
    max_age = luigi.IntParameter(default=24 * 30)

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='geonames')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return Download()

class Import(histograph.Import):
    dataset = luigi.Parameter(default='geonames')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return Transform()
