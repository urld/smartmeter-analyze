#!/usr/bin/python
"""Smartmeter Util.

Usage:
    {basename} summary [options] <filename>...
    {basename} weekly [options] <filename>...
    {basename} import [options] <filename>...
    {basename} -h | --help
    {basename} --version

Options:
    -h --help   Show help.
    --debug     Print debugging messages.
"""

from __future__ import print_function

from docopt import docopt
from smartmeter import analyze

if __name__ == "__main__":
    arguments = docopt(__doc__.format(basename=__file__), version='0.1.0')
    data = analyze.read_consumption_csv(arguments['<filename>'])
    if arguments['--debug']:
        print(arguments)
    if arguments['weekly']:
        analyze.print_stats_week(data)
    else:
        analyze.print_summary(data)
