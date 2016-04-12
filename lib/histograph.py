import luigi

from datetime import datetime, timedelta
import dateutil.parser
import pytz
from subprocess import call
import json
import urllib2
import time

class Data(luigi.Task):
    dataset = luigi.Parameter()
    step = luigi.Parameter()
    max_age = luigi.IntParameter(default=24)

    def run(self):
        node = 'node'
        script = '/Users/bertspaan/code/nypl-spacetime/spacetime-etl/index.js'
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
        except IOError, err:
            return False

    def input(self):
        path = '/Users/bertspaan/data/histograph/data'
        filename = '{}/{}/{}/{}'.format(path, self.step, self.dataset, '.status.json')
        return luigi.LocalTarget(filename)

class Import(luigi.Task):
    dataset = luigi.Parameter()
    max_age = luigi.IntParameter(default=24)
    types = luigi.Parameter(default='both', significant=False)

    def check_types(self, types):
        if not types in ['pits', 'relations', 'both']:
            raise ValueError('types should be `pits`, `relations`, or `both`')

    def too_old(self, date):
        if date is None:
            return True

        now = datetime.now(pytz.utc)
        date = dateutil.parser.parse(date)

        if (now - date).total_seconds() / 60 / 60 > self.max_age:
            return True
        else:
            return False

    def fill_none(self, date_updated):
        if date_updated is None:
            return {
                'pits': None,
                'relations': None
            }
        else:
            return date_updated

    def date_updated(self):
        try:
            api = 'http://localhost:3001'
            data = json.load(urllib2.urlopen('{}/{}/{}'.format(api, 'datasets', self.dataset)))

            if 'dateUpdated' in data:
                return data['dateUpdated']
            else:
                return None
        except urllib2.HTTPError, err:
            if err.code == 404:
                return None
            else:
                raise

    def run(self):
        self.check_types(self.types)

        node = 'node'
        script = '/Users/bertspaan/code/nypl-spacetime/histograph-import/index.js'

        first_date_updated = self.fill_none(self.date_updated())

        code = call([node, script, self.dataset])

        if code == 1:
            raise Exception('Neeeeetjes')

        same_dates = True
        while same_dates:
            time.sleep(5)
            date_updated = self.fill_none(self.date_updated())

            if self.types == 'pits':
                same_dates = first_date_updated['pits'] == date_updated['pits']
            elif self.types == 'relations':
                same_dates = first_date_updated['relations'] == date_updated['relations']
            elif self.types == 'both':
                same_dates = ((first_date_updated['pits'] == date_updated['pits']) or
                    (first_date_updated['relations'] == date_updated['relations']))

    def complete(self):
        self.check_types(self.types)

        try:
            date_updated = self.date_updated()
        except urllib2.URLError, err:
            raise ValueError('Could not connect to Space/Time API')

        if date_updated is None:
            return False

        if self.types == 'pits':
            return not self.too_old(date_updated['pits'])
        elif self.types == 'relations':
            return not self.too_old(date_updated['relations'])
        elif self.types == 'both':
            return not (self.too_old(date_updated['pits']) and
                self.too_old(date_updated['relations']))

        return False
