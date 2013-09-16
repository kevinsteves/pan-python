#!/usr/bin/env python

# $Id: setup.py,v 1.5 2013/08/18 18:49:45 stevesk Exp $

# $ ./setup.py sdist

from distutils.core import setup

version='20130818'

setup(name='pan-python',
      version=version,
      description='Python package for PAN-OS',
      long_description='Python interface to the PAN-OS XML API',
      author='Kevin Steves',
      author_email='kevin.steves@pobox.com',
      url='http://pobox.com/~kevin.steves/',
      license='ISC',
#
      package_dir = {'': 'lib'},
      packages=['pan'],
      scripts=['bin/panxapi.py']
     )
