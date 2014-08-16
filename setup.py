#!/usr/bin/env python

from distutils.core import setup

# readme = open('README.rst').read()

setup(
    name='smartmeter',
    version='0.1.0',
    description='tools to analyze and manage consumption data from smartmeters',
    # long_description=readme + '\n\n' + history,
    author='David Url',
    author_email='david@x00.at',
    url='https://x00.at',
    packages=[
        'smartmeter',
    ],
    scripts=[
        'smartmeter-util',
    ],
    package_dir={'smartmeter': 'smartmeter'},
    license="BSD",
    keywords='smartmeter, data analysis',
    classifiers=[
        'Natural Language :: English',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
    ],
)
