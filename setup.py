#!/usr/bin/env python

# $ ./setup.py sdist

from distutils.core import setup

version = 'snapshot'
version = None

if version is None:
    import sys
    sys.path[:0] = ['lib']
    from pan.xapi import __version__
    version = __version__
elif version == 'snapshot':
    import time
    version = 'snapshot-' + time.strftime('%Y%m%d')

setup(name='pan-python',
      version=version,
      description='Python package for PAN-OS',
      long_description='Python interface to the PAN-OS XML API',
      author='Kevin Steves',
      author_email='kevin.steves@pobox.com',
      url='https://github.com/kevinsteves/pan-python',
      license='ISC',
#
      package_dir = {'': 'lib'},
      packages=['pan'],
      scripts=['bin/panxapi.py']
     )
