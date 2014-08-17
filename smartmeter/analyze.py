import pandas as pd
import numpy as np

SEP_LINE = '='*33

pd.set_option('display.precision', 4)


def read_consumption_csv(filename):
    usages = pd.read_csv(filename,
                         delimiter=';',
                         header=0,  # ignore header
                         usecols=[0, 1],  # third column is empty
                         names=['date', 'usage'],
                         index_col='date',  # use date as index
                         decimal=',',
                         parse_dates=True,
                         infer_datetime_format=True,
                         dayfirst=True,  # csv dateformat: DD.MM.YYYY
                         )
    return usages


def print_summary(data):
    data['month'] = data.index.month
    month_group = data.groupby('month')
    aggregates = [[data.usage.sum()],
                  [month_group[['usage']].sum()[:-1].usage.mean()],
                  [data.usage.mean()],
                  ]
    extrema = [[data.usage.idxmin(), data.usage.min()],
               [data.usage.idxmax(), data.usage.max()],
               ]
    print "CONSUMPTION SUMMARIES"
    print SEP_LINE
    print "from {}".format(data.index.min().date())
    print "to   {}".format(data.index.max().date())
    print "({} days)".format(data.usage.count())
    print SEP_LINE
    print pd.DataFrame(aggregates,
                       columns=['usage [kWh]'],
                       index=['sum', 'monthly average', 'daily average'])
    print SEP_LINE
    print pd.DataFrame(extrema,
                       columns=['date', 'usage [kWh]'],
                       index=['min', 'max'])


def print_stats_week(data):
    weekdays = ['Monday',
                'Tuesday',
                'Wednesday',
                'Thursday',
                'Friday',
                'Saturday',
                'Sunday']
    data['weekday'] = data.index.weekday
    weekday_group = data.groupby('weekday')
    weekday_avg = weekday_group.aggregate(np.mean)
    weekday_avg.index = weekdays
    weekday_avg.index.name = 'Weekday'
    weekly_avg = weekday_avg.sum()

    print "WEEK STATS:"
    print SEP_LINE
    print weekday_avg[['usage']]
    print "\nweekly average {} kWh".format(round(weekly_avg, 3))
