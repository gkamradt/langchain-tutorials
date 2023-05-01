#!/usr/bin/env python

# Copyright (c) 2014 SeatGeek

# This file is part of thefuzz.

from thefuzz import __version__
import os

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


def open_file(fname):
    return open(os.path.join(os.path.dirname(__file__), fname))


setup(
    name='thefuzz',
    version=__version__,
    author='Adam Cohen',
    author_email='adam@seatgeek.com',
    packages=['thefuzz'],
    extras_require={'speedup': ['python-levenshtein>=0.12']},
    url='https://github.com/seatgeek/thefuzz',
    license="GPLv2",
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
        'Programming Language :: Python :: 3 :: Only',
    ],
    description='Fuzzy string matching in python',
    long_description=open_file('README.rst').read(),
    zip_safe=True,
)
