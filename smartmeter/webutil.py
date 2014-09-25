from smartmeter import analyze
from flask import Flask
import logging
from docutils.core import publish_string

app = Flask(__name__)
log = logging.getLogger(__name__)


@app.route("/<dir_url>")
def summary(dir_url):
    dir = dir_url.replace('_', '/')
    log.debug(dir)
    input = analyze.FileDataSource([dir], 'tageswerte*.csv')
    stats = analyze.Stats(input.get_data())
    stats.calc_stats()
    rst = analyze.rst_summary(stats)
    return publish_string(rst, writer_name='html')


def run_server(debug=False):
    print debug
    app.run(debug=debug)
