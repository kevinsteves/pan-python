#!/usr/bin/env python

# ./setup.py sdist bdist_wheel

from setuptools import setup
import sys
sys.path[:0] = ['lib']
from pan.xapi import __version__

with open('README.rst') as f:
    long_description = f.read()

setup(
    name='pan-python',
    version=__version__,
    author='Kevin Steves',
    author_email='kevin.steves@pobox.com',
    description='Multi-tool set for Palo Alto Networks' +
    ' PAN-OS, Panorama, WildFire and AutoFocus',
    long_description=long_description,
    long_description_content_type='text/x-rst',
    url='https://github.com/kevinsteves/pan-python',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'Intended Audience :: End Users/Desktop',
        'License :: OSI Approved :: ISC License (ISCL)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    package_dir={'': 'lib'},
    packages=[
        'pan',
        'pan/afapi',
        'pan/licapi'
    ],
    scripts=[
        'bin/panxapi.py',
        'bin/panconf.py',
        'bin/panwfapi.py',
        'bin/panafapi.py',
        'bin/panlicapi.py',
    ],
)
