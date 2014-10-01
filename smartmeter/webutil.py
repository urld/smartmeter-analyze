import datetime
import logging
import hashlib

from flask import Flask, request, redirect, url_for
from docutils.core import publish_string

from smartmeter import analyze


app = Flask(__name__)
# maximal file size for uploaded files: (8MB)
app.config['MAX_CONTENT_LENGTH'] = 8 * 1024 * 1024
log = logging.getLogger(__name__)
TMP_STORAGE = None


@app.route('/analyze', methods=['GET', 'POST'])
def api_upload_csv():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.rsplit('.', 1)[1] in ['csv']:
            key = TMP_STORAGE.add(file)
            return redirect(url_for('api_analyze', key=key))
        else:
            return redirect(url_for('api_upload_csv'))
    else:
        return '''
        <!doctype html>
        <title>Upload new File</title>
        <h1>Upload new File</h1>
        <form action="" method=post enctype=multipart/form-data>
            <p><input type=file name=file></p>
            <p><input type=submit value=Analyze!></p>
        </form>
        '''


@app.route('/analyze/<key>')
def api_analyze(key):
    stats = TMP_STORAGE.get(key)
    if stats:
        rst = analyze.rst_summary(stats)
        return publish_string(rst, writer_name='html')
    else:
        return "404: Stats not found!", 404


@app.route('/clear/<key>')
def api_clear(key):
    TMP_STORAGE.remove(key)
    return redirect(url_for('api_upload_csv'))


class TmpStorage(object):

    def __init__(self):
        self.storage = {}

    def add(self, csv_file):
        # generate key:
        key = hashlib.sha1(csv_file.read()).hexdigest()
        if key not in self.storage:
            # generate stats:
            csv_file.seek(0)
            data = analyze.read_csv_file(csv_file)
            csv_file.close()
            stats = analyze.Stats(data)
            stats._load_dts = datetime.datetime.now()
            stats.calc_stats()
            # store:
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
            if self.get(key)._load_dts < threshold:
                self.remove(key)


def run_server(debug=False):
    global TMP_STORAGE
    TMP_STORAGE = TmpStorage()
    app.run(debug=debug, ssl_context='adhoc')
