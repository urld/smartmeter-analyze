#!/usr/bin/env python

import os
from distutils.core import setup
from distutils.command.install import install
from smartmeter import __version__

# readme = open('README.rst').read()


def _merge_dicts(d1, d2):
    d = d1
    for k2 in d2:
        if k2 in d1:
            d[k2] = d1[k2] + d2[k2]
        else:
            d[k2] = d2[k2]
    return d

# BEWARE!! Changing this might have unexpected effects binary distributions:
EXTERNAL_PACKAGE_DATA = {'smartmeter': ['LICENSE', 'README.rst', 'AUTHORS.rst']}
PACKAGE_DATA = {'smartmeter': ['logging.conf']}
ALL_PACKAGE_DATA = _merge_dicts(PACKAGE_DATA, EXTERNAL_PACKAGE_DATA)


class install_complete(install):
    """Kind of dirty hack to include files containing authors, license and
    and readme with binary distributions.
    """
    def run(self):
        # create symbolic links to trigger copying:
        links = []
        for package in EXTERNAL_PACKAGE_DATA:
            for path in EXTERNAL_PACKAGE_DATA[package]:
                link = os.path.join(self.build_lib, package, path)
                links.append(link)
                os.symlink(os.path.join(os.getcwd(), path), link)
        # call original install (targets of symbolic links will be copied):
        install.run(self)
        # cleanup temporary links:
        for link in links:
            os.unlink(link)


setup(
    cmdclass={'install': install_complete},
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
    package_dir={'smartmeter': 'smartmeter'},
    package_data=PACKAGE_DATA,
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
    ],
)
