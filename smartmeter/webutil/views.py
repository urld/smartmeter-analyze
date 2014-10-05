import logging

from flask import request, redirect, url_for
from docutils.core import publish_string

from smartmeter import analyze
from smartmeter.webutil import app, TMP_STORAGE


log = logging.getLogger(__name__)


@app.route('/')
def api_about():
    """This only works in development environment."""
    with open('README.rst') as file:
        readme = file.read()
    return publish_string(readme, writer_name='html')


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
