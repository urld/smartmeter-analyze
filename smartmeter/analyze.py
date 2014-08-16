#!/usr/bin/python

import csv

FILE = '../test/tageswerte-20140816-174538.csv'


def _read_csv(filename, delimiter=';'):
    with open(filename, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=delimiter)
        for row in reader:
            yield row


def read_consumption_csv(filename):
    # TODO: error handling
    consumption_csv = _read_csv(filename, delimiter=';')
    # header = consumption_csv.next()
    consumption_csv.next()  # skip header
    consumptions = [{'date': day[0],
                    'consumption': float(day[1].replace(',', '.'))}
                    for day in consumption_csv]
    return consumptions


def print_summary(consumptions):
    # TODO: use pandas dataframe for nicer output
    values = map(lambda c: c['consumption'], consumptions)
    count = len(consumptions)
    total = sum(values)
    average = total / count
    print "Days:\t{}".format(count)
    print "Sum:\t{} kWh".format(total)
    print "Avg:\t{} kWh".format(round(average, 3))
    print "Max:\t{} kWh".format(max(values))
    print "Min:\t{} kWh".format(min(values))


if __name__ == "__main__":
    consumptions = read_consumption_csv(FILE)
    print_summary(consumptions)
