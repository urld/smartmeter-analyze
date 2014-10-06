import logging

from flask import request, redirect, url_for, render_template
from docutils.core import publish_string

import smartmeter.analyze
from smartmeter.webutil import app, TMP_STORAGE


log = logging.getLogger(__name__)


@app.route('/about')
def about():
    """This only works in development environment."""
    with open('README.rst') as file:
        readme = file.read()
    return publish_string(readme, writer_name='html')


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/analyze', methods=['GET', 'POST'])
def analyze():
    if request.method == 'POST':
        file = request.files['file']
        if file and file.filename.rsplit('.', 1)[1] in ['csv']:
            key = TMP_STORAGE.add(file)
            return redirect(url_for('report', key=key))
        else:
            return redirect(url_for('analyze'))
    else:
        return render_template('analyze.html')


@app.route('/analyze/<key>')
def report(key):
    stats = TMP_STORAGE.get(key)
    if stats:
        rst = smartmeter.analyze.rst_summary(stats)
        return publish_string(rst, writer_name='html')
    else:
        return "404: Stats not found!", 404


@app.route('/clear/<key>')
def delete(key):
    TMP_STORAGE.remove(key)
    return redirect(url_for('analyze'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404
