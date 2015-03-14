import datetime
import logging
import hashlib

from smartmeter import analyze


log = logging.getLogger(__name__)


class TmpStorage(object):

    def __init__(self, ttl_minutes=1):
        self.storage = {}
        self.ttl = datetime.timedelta(minutes=ttl_minutes)

    def add(self, csv_file):
        # generate key:
        key = hashlib.sha1(csv_file.read()).hexdigest()
        load_dts = datetime.datetime.now()
        if not self.has_item(key):
            # generate stats:
            csv_file.seek(0)
            data = analyze.read_csv_file(csv_file)
            csv_file.close()
            stats = analyze.Stats(data)
            stats.calc_stats()
            # store:
            self.storage[key] = (stats, load_dts)
        else:
            # update/reset load_dts:
            self.storage[key] = (self.storage[key][0], load_dts)
        return key

    def get(self, key):
        if self._is_valid(key):
            return self.storage[key][0]
        else:
            self.remove(key)
            return self.get(key)

    def get_load_dts(self, key):
        return self.storage[key][1]

    def get_all(self, key):
        """Returns a tuple of (stats, load_dts)"""
        if self._is_valid(key):
            return self.storage[key]
        else:
            self.remove(key)

    def remove(self, key):
        del self.storage[key]
        log.info('Deleted: {}'.format(key))

    def cleanup(self, minutes=15):
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(minutes=minutes)
        for key in self.storage:
            if self.get(key)._load_dts < threshold:
                self.remove(key)

    def _is_valid(self, key):
        now = datetime.datetime.now()
        threshold = now - self.ttl
        if self.get_load_dts(key) < threshold:
            return False
        else:
            return True

    def has_item(self, key):
        if key in self.storage:
            if self._is_valid(key):
                return True
            else:
                self.remove(key)
                return False
        else:
            return False

    def get_ttl(self):
        return self.ttl
