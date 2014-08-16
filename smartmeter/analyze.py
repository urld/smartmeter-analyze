import pandas as pd
# import numpy as np

FILE = '../test/tageswerte-20140816-174538.csv'
# SEP_LINE = "=================================="
SEP_LINE = '='*33


def read_consumption_csv(filename):
    consumptions = pd.read_csv(filename,
                               delimiter=';',
                               header=0,  # ignore header
                               usecols=[0, 1],  # third column is empty
                               names=['date', 'consumption'],
                               index_col='date',  # use date as index
                               decimal=',',
                               parse_dates=True,
                               infer_datetime_format=True,
                               dayfirst=True,  # csv dateformat: DD.MM.YYYY
                               )
    return consumptions


def print_summary(data):
    aggregates = [[data.consumption.sum()],
                  [data.consumption.mean()],
                  ]
    extrema = [[data.consumption.idxmin(), data.consumption.min()],
               [data.consumption.idxmax(), data.consumption.max()],
               ]
    print "CONSUMPTION SUMMARIES"
    print SEP_LINE
    print "from {}".format(data.index.min().date())
    print "to   {}".format(data.index.max().date())
    print "({} days)".format(data.consumption.count())
    print SEP_LINE
    print pd.DataFrame(aggregates,
                       columns=['consumption [kWh]'],
                       index=['sum', 'average'])
    print SEP_LINE
    print pd.DataFrame(extrema,
                       columns=['date', 'consumption [kWh]'],
                       index=['min', 'max'])
