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


@app.route('/analyze/<key>', methods=['GET'])
def report(key):
    try:
        stats = TMP_STORAGE.get(key)
    except KeyError as e:
        return resource_not_found(e)
    return render_template('report.html', stats=stats)
#    rst = smartmeter.analyze.rst_summary(stats)
#    return publish_string(rst, writer_name='html')


@app.route('/analyze/<key>', methods=['DELETE', 'POST'])
def delete(key):
    try:
        TMP_STORAGE.remove(key)
    except KeyError as e:
        return resource_not_found(e)
    return redirect(url_for('index'))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.site.html', page=request.path), 404


def resource_not_found(e):
    return render_template('404.resource.html',
                           method=request.method,
                           resource=request.path), 404
