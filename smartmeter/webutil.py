import datetime
import logging

from flask import Flask, request, redirect
from docutils.core import publish_string

from smartmeter import analyze


app = Flask(__name__)
# maximal file size for uploaded files: (8MB)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
log = logging.getLogger(__name__)
TMP_STORAGE = None


@app.route("/dir/<dir_url>")
def summary(dir_url):
    dir = dir_url.replace('_', '/')
    log.debug(dir)
    input = analyze.FileDataSource([dir], 'tageswerte*.csv')
    stats = analyze.Stats(input.get_data())
    stats.calc_stats()
    rst = analyze.rst_summary(stats)
    return publish_string(rst, writer_name='html')


@app.route('/analyze', methods=['GET', 'POST'])
def upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.rsplit('.', 1)[1] in ['csv']:
            key = TMP_STORAGE.add(file)
            return redirect('analyze/{}'.format(key))
        else:
            return redirect('analyze/{}'.format(key))
    else:
        return "Use HTTP-POST to upload your csv file!"


@app.route('/analyze/<key>')
def url_analyze(key):
    stats = TMP_STORAGE.get(key)
    if stats:
        rst = analyze.rst_summary(stats)
        return publish_string(rst, writer_name='html')
    else:
        return "404: Stats not found!"


@app.route('/clear/<key>')
def clear(key):
    TMP_STORAGE.remove(key)


class TmpStorage(object):

    def __init__(self):
        self.storage = {}

    def add(self, csv):
        data = analyze.read_csv_file(csv)
        stats = analyze.Stats(data)
        stats.calc_stats()
        key = str(hash(csv))
        self.storage[key] = stats
        return key

    def get(self, key):
        return self.storage[key]

    def remove(self, key):
        del self.storage[key]

    def cleanup(self, minutes=15):
        now = datetime.datetime.now()
        threshold = now - datetime.timedelta(minutes=minutes)
        for key in self.storage:
            if self.get(key)._date_created < threshold:
                self.remove(key)


def run_server(debug=False):
    global TMP_STORAGE
    TMP_STORAGE = TmpStorage()
    app.run(debug=debug)
