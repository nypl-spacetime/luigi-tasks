import luigi
from lib import histograph
from datasets import building_inspector
from datasets import centerlines
from datasets import directory_1854
from datasets import geonames
from datasets import mapwarper
from datasets import oldnyc
from datasets import streets_addresses
from datasets import tgn_geonames
from datasets import tgn
from datasets import wards

class Import(luigi.WrapperTask):
    def requires(self):
        yield building_inspector.Import()
        yield wards.Import()
        yield centerlines.Import()
        yield directory_1854.Import()
        yield geonames.Import()
        yield mapwarper.Import()
        yield oldnyc.Import()
        yield streets_addresses.Import()
        yield tgn_geonames.Import()
        yield tgn.Import()

class Stats(histograph.Data):
    dataset = luigi.Parameter(default='stats-test')
    step = luigi.Parameter(default='stats')
    max_age = luigi.IntParameter(default=24 * 30)

    def requires(self):
        return Import()
