#!/usr/bin/env python

from distutils.core import setup
from smartmeter import __version__

with open('README.rst') as readme:
    readme = readme.read()  # reading the readme (haha)

setup(
    name='smartmeter-analyze',
    version=__version__,
    description='tools to analyze and manage consumption data from smartmeters',
    long_description=readme,
    author='David Url',
    author_email='david@x00.at',
    url='https://github.com/durl/smartmeter-analyze',
    packages=[
        'smartmeter',
        'webutil',
    ],
    package_data={'smartmeter': ['logging.conf'],
                  'webutil': ['templates/*/*', 'templates/*',
                              'static/*/*', 'static/*']},
    py_modules=[
        'docopt',
    ],
    scripts=[
        'smutil',
    ],
    requires=[
        'pandas (>=0.14.1)',
    ],
    license='GNU Affero General Public License v3 or later (AGPLv3+)',
    keywords='smartmeter, data analysis, wiener netze',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'Natural Language :: English',
        'Programming Language :: Python :: 2.7',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Utilities',
    ],
)
