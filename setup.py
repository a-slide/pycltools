#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""       
  ___         _ 
 | _ \_  _ __| |
 |  _/ || / _| |
 |_|  \_, \__|_|
      |__/        
                                __   __      __  
 /\  _| _. _ _   |   _ _  _ _    _) /  \ /| /__  
/--\(_|| |(-| )  |__(-(_)(-|    /__ \__/  | \__) 
                      _/                         
"""

from setuptools import setup, find_packages

setup(
    name='pycl',
    version='1.0.dev1',
    description='pycl contains a generic collection of functions and classes for basic file manipulation in python 3',
    long_description=open('README.md', 'r').read(),
    url='https://github.com/a-slide/pycl',
    author='Adrien Leger',
    author_email='aleg@ebi.ac.uk',
    license='GPLv3',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6', ],

    packages=["pycl"],
    package_dir={'pycl': 'pycl'},
    package_data={'pycl': ['data/*', "test_pycl.ipynb"]},
)
