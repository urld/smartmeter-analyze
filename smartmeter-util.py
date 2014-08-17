#!/usr/bin/python
"""Smartmeter Util.

Usage:
    {basename} summary [options] [-p <pattern>] <filename>...
    {basename} weekly [options] [-p <pattern>] <filename>...
    {basename} import [options] [-p <pattern>] <filename>...
    {basename} -h | --help
    {basename} --version

Options:
    -h --help       Show help.
    --debug         Print debugging messages.
    -p <pattern>    Pattern to filter csv files if one or more directories are
                    specified in the file list. [default: tageswerte*.csv]
"""

from __future__ import print_function
import sys

from docopt import docopt
from smartmeter import analyze

if __name__ == "__main__":
    args = docopt(__doc__.format(basename=__file__), version='0.1.0')
    if args['--debug']:
        print(args)
    try:
        data = analyze.read_consumption_csv(args['<filename>'], args['-p'])
    except analyze.InputError as e:
        print(e)
        sys.exit(1)
    if args['weekly']:
        analyze.print_stats_week(data)
    else:
        analyze.print_summary(data)
