import luigi
from lib import histograph
from datetime import timedelta

MAX_AGE = timedelta(days=1)

class Transform(histograph.Data):
    dataset = luigi.Parameter(default='wards')
    step = luigi.Parameter(default='transform')
    max_age = luigi.IntParameter(default=24 * 30)

class Import(histograph.Import):
    dataset = luigi.Parameter(default='wards')
    max_age = luigi.IntParameter(default=24 * 30)
    types = luigi.Parameter(default='pits')

    def requires(self):
        return Transform()
