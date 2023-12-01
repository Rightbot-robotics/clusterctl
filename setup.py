#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
try:
    from setuptools import setup, find_packages
except ImportError:
    print ("clusterctl needs setuptools in order to build. ")
    print("Please install it using your package manager (usually python-setuptools) or via pip (pip install setuptools).")
    sys.exit(1)

requirements = []

test_requirements = []

here = os.path.abspath(os.path.dirname(__file__))
try:
    README = open(os.path.join(here, 'README.rst')).read()
    CHANGES = open(os.path.join(here, 'CHANGES.txt')).read().replace('.. :changelog:', '')
except:
    README = ''
    CHANGES = ''

data_files = []

setup(
    name='clusterctl',
    version= '0.0.1',
    description= "control",
    long_description=README + '\n\n' +  CHANGES,
    author='author',
    keywords = 'supervisor ansible',
    author_email='rbrtwnklr@gmail.com',
    url='https://github.com/RobWin/supervisorclusterctl.git',
    packages=find_packages(exclude=["docs", "test"]),
    install_requires=requirements,
    tests_require=test_requirements,
    test_suite="test",
    data_files=data_files,
    license='GPLv3',
    entry_points={
     'console_scripts': [
         'clusterctl = clusterctl.clusterctl:main'
        ],
    }
)