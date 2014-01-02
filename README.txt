pan-python is a Python package for Palo Alto Networks' Next-Generation
Firewalls.  It provides:

  - a Python and command line interface to the PAN-OS and Panorama XML API
  - a command line program for managing PAN-OS XML configurations

Python versions 2.7, 3.2 and 3.3 are supported with a single code
base.  There are no external modules required to use pan-python.

The pan package contains the following modules:

    pan.xapi:   pan.xapi.PanXapi class
    pan.commit: pan.commit.PanCommit class (internal)
    pan.rc:     pan.rc.PanRc class (internal)
    pan.config: pan.config.PanConfig class (internal)

bin/panxapi.py is a command line program for accessing the XML API and
uses the pan.xapi and pan.commit modules.

bin/panconf.py is a command line program program for managing PAN-OS
XML configurations and uses the pan.config module.

Documentation:

  Rendered reStructuredText from GitHub:

    https://github.com/kevinsteves/pan-python/blob/master/doc/panxapi.rst
    https://github.com/kevinsteves/pan-python/blob/master/doc/panconf.rst
    https://github.com/kevinsteves/pan-python/blob/master/doc/pan.xapi.rst

  HTML from source distribution:

    doc/panxapi.html
    doc/panconf.html
    doc/pan.xapi.html

Install:

  You can install the package or just run the programs from within the
  package source directory:

    $ tar xzf pan-python-1.0.0.tar.gz
    $ cd pan-python-1.0.0

    $ cd bin
    $ ./panxapi.py

  or:

    $ sudo ./setup.py install
    $ panxapi.py

Remote Git Repository:

  https://github.com/kevinsteves/pan-python

Author:

  Kevin Steves <kevin.steves@pobox.com>
