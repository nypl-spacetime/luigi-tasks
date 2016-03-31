import luigi
import histograph

class Download(histograph.Data):
    dataset = luigi.Parameter(default='building-inspector')
    step = luigi.Parameter(default='download')
    max_age = luigi.IntParameter(default=24 * 30)

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='building-inspector')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        yield Download()

class Import(histograph.Import):
    dataset = luigi.Parameter(default='building-inspector')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        yield Transform()
