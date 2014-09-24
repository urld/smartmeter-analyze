import datetime
from fnmatch import fnmatch
import logging
import os

import numpy as np
import pandas as pd

SEP_LINE = '='*33

pd.set_option('display.precision', 4)

log = logging.getLogger(__name__)


class InputError(Exception):

    """Raised if there was a problem with input files."""

    def __init__(self, msg, input=None):
        self.msg = msg
        self.input = input

    def __str__(self):
        if self.input:
            return "{msg}: {input}".format(msg=self.msg, input=self.input)
        else:
            return str(self.msg)


class FileDataSource(object):

    """A collection of csv files which are used as data source."""

    def __init__(self, sources=[], pattern='*.csv'):
        self.sources = []
        self.raw_sources = {}
        self.cached_data = None
        for source in sources:
            self.add_source_directory(source, pattern)

    def add_source_file(self, file):
        if not os.path.isfile(file):
            raise InputError('CSV file not found', input=file)
        self.raw_sources[file] = None
        self.sources += [file]
        return file

    def add_source_directory(self, directory, pattern):
        if os.path.isdir(directory):
            self.raw_sources[directory] = pattern
            sources = self._find_files(directory, pattern)
            self.sources += sources
            return sources
        else:
            return self.add_source_file(directory)

    def _find_files(self, directory, pattern):
        filelist = []
        for root, dirs, files in os.walk(directory, followlinks=True):
            filelist += [os.path.join(root, f)
                         for f in files if fnmatch(f, pattern)]
        return filelist

    def refresh_sources(self):
        sources = []
        for dir, pattern in self.raw_sources:
            if pattern:
                sources += self._find_files(dir, pattern)
            else:
                sources += [dir]
        log.info("{} files found. (previously: {})".format(len(sources),
                                                           len(self.sources)))
        self.sources = sources
        self.cached_data = None

    def _read_data(self):
        log.debug('Reading files: ' + repr(self.sources))
        data = []
        for filename in self.sources:
            data += [pd.read_csv(filename,
                                 delimiter=';',
                                 header=0,  # ignore header
                                 usecols=[0, 1],  # third column is empty
                                 names=['date', 'usage'],
                                 index_col='date',  # use date as index
                                 decimal=',',
                                 parse_dates=True,
                                 infer_datetime_format=True,
                                 dayfirst=True,  # csv dateformat: DD.MM.YYYY
                                 )]
        if data:
            union = pd.concat(data)
            union.sort_index(inplace=True)
            unique = union.groupby(union.index).first()
            log.info('read_data: IN={} OUT={}'.format(len(union), len(unique)))
            return unique
        else:
            raise InputError('No data read.')

    def get_data(self):
        if self.cached_data is None:
            self.cached_data = self._read_data()
        return self.cached_data


class Stats(object):

    def __init__(self, data):
        self.data = data
        self._extend_dataframe()
        self.start_date = None
        self.end_date = None
        self.day_count = None
        self.averages = {}
        self.max = None
        self.max_date = None
        self.min = None
        self.min_date = None

    def _extend_dataframe(self):
        self.data['year'] = self.data.index.year
        self.data['month'] = self.data.index.month
        self.data['weekday'] = self.data.index.weekday
        monthly = self.data.groupby('month')
        self.data['monthly_cumsum'] = monthly['usage'].cumsum()
        yearly = self.data.groupby('year')
        self.data['yearly_cumsum'] = yearly['usage'].cumsum()

    def calc_date_range(self):
        if not self.start_date:
            self.start_date = self.data.index.min().date()
        if not self.end_date:
            self.end_date = self.data.index.max().date()
        if not self.day_count:
            self.day_count = self.data.usage.count()
        return self.start_date, self.end_date

    def calc_averages(self):
        weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                    'Saturday', 'Sunday']
        if 'daily' not in self.averages:
            self.averages['daily'] = self.data.usage.mean()
        if 'monthly' not in self.averages:
            monthly = self.data.groupby('month')
            monthly_avg = monthly[['usage']].sum()[:-1].usage.mean()
            self.averages['monthly'] = monthly_avg
        if 'weekly' not in self.averages:
            weekday_group = self.data.groupby('weekday')
            weekday_avg = weekday_group.aggregate(np.mean)
            weekday_avg.index = weekdays
            for weekday in weekdays:
                self.averages[weekday] = weekday_avg.loc[weekday, 'usage']
            self.averages['weekly'] = weekday_avg.sum()['usage']
        return self.averages

    def calc_extrema(self):
        if not self.min:
            self.min_date = self.data.usage.idxmin().date()
            self.min = self.data.usage.min()
        if not self.max:
            self.max_date = self.data.usage.idxmax().date()
            self.max = self.data.usage.max()
        return self.min, self.max

    def calc_stats(self):
        self.calc_date_range()
        self.calc_extrema()
        self.calc_averages()

    def get_monthly_cumsum(self, due_date=None):
        if not due_date:
            due_date = self.end_date
        return self.data.loc[due_date, 'monthly_cumsum']

    def get_yearly_cumsum(self, due_date=None):
        if not due_date:
            due_date = self.end_date
        return self.data.loc[due_date, 'yearly_cumsum']


def print_summary(stats):
    print_coverage(stats)
    print_extrema(stats)
    print_averages(stats)


def print_coverage(stats):
    print "============="
    print "DATA COVERAGE"
    print "=============\n"
    print "     {} days".format(stats.day_count)
    print "from {}".format(stats.start_date)
    print "to   {}".format(stats.end_date)
    print ""


def print_extrema(stats):
    print "======="
    print "EXTREMA"
    print "=======\n"
    print " min usage {:>8} kWh  ({})".format(stats.min, stats.min_date)
    print " max usage {:>8} kWh  ({})".format(stats.max, stats.max_date)
    print ""


def print_averages(stats):
    print "========"
    print "AVERAGES"
    print "========\n"
    for key in ['monthly', 'weekly', 'daily']:
        print "{:>10}{:>9.3f} kWh".format(key, round(stats.averages[key], 3))
    print ""
    weekdays = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday',
                'Saturday', 'Sunday']
    for key in weekdays:
        print "{:>10}{:>9.3f} kWh".format(key, round(stats.averages[key], 3))
    print ""


def print_comparisons(stats, due_date=None):
    if not due_date:
        due_date = stats.end_date
    cum_usage = stats.get_monthly_cumsum(due_date)
    prev_due_date = _previous_month(due_date)
    prev_cum_usage = stats.get_monthly_cumsum(prev_due_date)
    prev_end_date = _previous_month_end(due_date)
    prev_total_usage = stats.get_monthly_cumsum(prev_end_date)
    delta = cum_usage - prev_cum_usage
    print "==================="
    print "MONTHLY COMPARISONS"
    print "===================\n"
    print "last month total {:>9.3f} kWh  ({})".format(prev_total_usage,
                                                       prev_end_date)
    print "last month       {:>9.3f} kWh  ({})".format(prev_cum_usage,
                                                       prev_due_date)
    print "current month    {:>9.3f} kWh  ({})".format(cum_usage, due_date)
    print "difference       {:>+9.3f} kWh  ({})".format(delta, prev_due_date)
    print ""


def _previous_month(date):
    prev_month = date
    while prev_month.month == date.month or date.day < prev_month.day:
        prev_month -= datetime.timedelta(days=1)
    return prev_month


def _previous_month_end(date):
    return date.replace(day=1) - datetime.timedelta(days=1)
