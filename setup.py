#!/usr/bin/env python

from distutils.core import setup
from smartmeter import __version__

# readme = open('README.rst').read()

setup(
    name='smartmeter',
    version=__version__,
    description='tools to analyze and manage consumption data from smartmeters',
    # long_description=readme + '\n\n' + history,
    author='David Url',
    author_email='david@x00.at',
    url='https://x00.at',
    packages=[
        'smartmeter',
    ],
    package_data={'smartmeter': ['logging.conf']},
    py_modules=[
        'docopt',
    ],
    scripts=[
        'smutil',
    ],
    package_dir={'smartmeter': 'smartmeter'},
    license="BSD",
    keywords='smartmeter, data analysis',
    classifiers=[
        'Development Status :: 1 - Planning',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: GNU Affero General Public License v3 or later (AGPLv3+)',
        'Natural Language :: English',
        'Operating System :: OS Independent',   # is it?
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
        '',
    ],
)
