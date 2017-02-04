#!/usr/bin/env python
#

import commands
import os
import re
import sys

from distutils.core import setup
from distutils.command.install import install as install_org
from distutils.command.install_data import install_data as install_data_org


import pyconfidence
release_version = pyconfidence.__version__ 

# ===========================================================
#                D A T A     F I L E S 
# ===========================================================

rpm_data_files=[ ]

# -----------------------------------------------------------

def choose_data_files():
    rpminstall = True
    userinstall = False
     
    if 'bdist_rpm' in sys.argv:
        rpminstall = True

    elif 'install' in sys.argv:
        for a in sys.argv:
            if a.lower().startswith('--home'):
                rpminstall = False
                userinstall = True
                
    return rpm_data_files
       
# ===========================================================

# setup for distutils
setup(
    name="pyconfidence",
    version=release_version,
    description='pyconfidence package',
    long_description='''This package contains pyconfidence''',
    license='GPL',
    author='Jose Caballero',
    author_email='jcaballero@bnl.gov',
    maintainer='Jose Caballero',
    maintainer_email='jcaballero@bnl.gov',
    url='https://matrix.net',
    # we include the test/ subdirectory
    packages=['pyconfidence', 
              'pyconfidence.test', 
              'pyconfidence.test.unit', 
              ],

    scripts = [],
    
    data_files = choose_data_files()
)
