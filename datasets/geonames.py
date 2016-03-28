import luigi
import histograph

class Download(histograph.Data):
    dataset = luigi.Parameter(default='geonames')
    step = luigi.Parameter(default='download')
    max_age = luigi.IntParameter(default=24)

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='geonames')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield Download()

class Import(histograph.Import):
    dataset = luigi.Parameter(default='geonames')
    max_age = luigi.IntParameter(default=24)

    def requires(self):
        yield Transform()
