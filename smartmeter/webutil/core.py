import datetime
import logging
import hashlib

from smartmeter import analyze


log = logging.getLogger(__name__)


class TmpStorage(object):

    def __init__(self):
        self.storage = {}

    def add(self, csv_file):
        # generate key:
        key = hashlib.sha1(csv_file.read()).hexdigest()
        if key not in self.storage:
            # generate stats:
            csv_file.seek(0)
            data = analyze.read_csv_file(csv_file)
            csv_file.close()
            stats = analyze.Stats(data)
            stats._load_dts = datetime.datetime.now()
            stats.calc_stats()
            # store:
            self.storage[key] = stats
        return key

    def get(self, key):
        return self.storage[key]

    def remove(self, key):
        del self.storage[key]
        log.info('Deleted: {}'.format(key))

    def cleanup(self, minutes=15):
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(minutes=minutes)
        for key in self.storage:
            if self.get(key)._load_dts < threshold:
                self.remove(key)
