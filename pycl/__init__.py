# -*- coding: utf-8 -*-

# Define self package variable
__version__ = '1.0.2'
__all__ = ["pycl"]
__doc__='python3 library containing general utilities to manipulate files, strings and folders'
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
__package_data__ =  ['test_pycl.ipynb', 'data/*']
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
    
# Collect info in a dictionnary for setup.py
from collections import OrderedDict
setup_dict = OrderedDict()

setup_dict["name"]=__name__
setup_dict["version"]=__version__
setup_dict["description"]=__doc__
setup_dict["url"]=__url__
setup_dict["author"]= __author__
setup_dict["author_email"]=__email__
setup_dict["license"]=__licence__
setup_dict["classifiers"]= __classifiers__
setup_dict["extras_require"]= __extras_require__
setup_dict["packages"]=[__name__]
setup_dict["package_dir"]={__name__: __name__}
setup_dict["package_data"]={__name__: __package_data__}
