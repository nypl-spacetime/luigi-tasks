# my_module.py, available in your sys.path
import luigi
from datetime import datetime, timedelta
import dateutil.parser
import pytz
from subprocess import call
import json

class Data(luigi.Task):
    dataset = luigi.Parameter()
    step = luigi.Parameter()
    max_age = luigi.IntParameter(default=24)

    def run(self):
        node = 'node'
        script = '/Users/bertspaan/code/nypl-spacetime/histograph-data/index.js'
        code = call([node, script, '--steps', self.step, self.dataset])

        if code == 1:
            raise Exception("Neeeeetjes")

    def complete(self):
        try:
            with self.input().open('r') as status_file:
                status = json.load(status_file)
                if status['success']:
                    now = datetime.now(pytz.utc)
                    date = dateutil.parser.parse(status['date'])
                    if (now - date).total_seconds() / 60 / 60 > self.max_age:
                        return False
                    else:
                        return True
                else:
                    return False
        except IOError as inst:
            return False

    def input(self):
        path = '/Users/bertspaan/data/histograph/data'
        filename = '{}/{}/{}/{}'.format(path, self.step, self.dataset, '.status.json')
        return luigi.LocalTarget(filename)

class Import(luigi.Task):
    dataset = luigi.Parameter()
    max_age = luigi.IntParameter(default=24)

    def run(self):
        node = 'node'
        script = '/Users/bertspaan/code/nypl-spacetime/histograph-import/index.js'

        code = call([node, script, self.dataset])

        # wacht hier tot dinges op redis staat!

        # print 'VISSEN'
        # print self.input()

        if code == 1:
            raise Exception('Neeeeetjes')

    #
    def complete(self):
        return True
    # #     # roep API aan, kijk wanneer last_imported
    #     return False
