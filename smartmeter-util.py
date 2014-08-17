#!/usr/bin/python

from __future__ import print_function

from smartmeter import analyze


def print_usage():
    print("Usage: {basename} filename".format(basename=__file__))

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print_usage()
        sys.exit(2)

    filename = sys.argv[1]
    data = analyze.read_consumption_csv(filename)
    analyze.print_summary(data)
    print("\n")
    analyze.print_stats_week(data)
