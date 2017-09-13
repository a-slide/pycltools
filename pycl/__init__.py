# -*- coding: utf-8 -*-

# Define self package variable
__version__ = '1.0.4'
__all__ = ["pycl"]
__author__= 'Adrien Leger'
__email__ = 'aleg@ebi.ac.uk'
__url__ = "https://github.com/a-slide/pycoQC"
__licence__ = 'GPLv3'
__classifiers__ = [
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Science/Research',
    'Topic :: Scientific/Engineering :: Bio-Informatics',
    'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.3',
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',]

__extras_require__ = {
    'toogle_code':  ["notebook"],
    'larger_display':  ["notebook"],
    'jprint':  ["notebook"],
    'jhelp':  ["notebook"],
    'count_uniq':  ["pandas"],
    'bash_update':  ["notebook"],
    'reformat_table':  ["pandas"],
    'url_exist':  ["httplib2"],
    'scp':  ["paramiko"],
    }

__package_data__ =  ['test_pycl.ipynb', 'data/*']
__python_requires__='>=3'
__description__= "pycl is a package written in python3 containing a collection of generic functions and classes for file parsing, manipulation..."

__long_description__="""
pycl contains many functions organized in several categories:

* jupyter notebook specific tools
* file predicates
* path manipulation
* string formatting
* file manipulation
* file information/parsing
* directory manipulation
* shell manipulation
* dictionnary formatting
* table formatting
* web tools
* functions tools
* ssh tools

Many of the function replicate bash commands in pure python.

Please be aware that pycl is an experimental package that is still under development. It was tested under Linux Ubuntu 16.04 and in an HPC 
environment running under Red Hat Enterprise 7.1. You are welcome to raise issues, contribute to the development and submit patches or
updates.
"""

# Collect info in a dictionnary for setup.py
setup_dict = {
    "name":__name__,
    "version":__version__,
    "description": __description__,
    "long_description": __long_description__,
    "url":__url__,
    "author": __author__,
    "author_email":__email__,
    "license":__licence__,
    "classifiers": __classifiers__,
    "extras_require": __extras_require__,
    "packages":[__name__],
    "package_dir":{__name__: __name__},
    "package_data":{__name__: __package_data__},
    "python_requires": __python_requires__,
    }
