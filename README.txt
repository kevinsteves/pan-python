pan-python is a Python package for Palo Alto Networks' Next-Generation
Firewalls, and provides a Python and command line interface to the
PAN-OS and Panorama XML API.

Python versions 2.7 and 3.2 are supported with a single code base
(3.3 is expected to work but is untested at this time).  There
are no external modules required to use pan-python.

The pan package contains the following modules:

    pan.xapi:   pan.xapi.PanXapi class
    pan.commit: pan.commit.PanCommit class (internal)
    pan.rc:     pan.rc.PanRc class (internal)

bin/panxapi.py is a command line program for accessing the XML
API and is built using the pan.xapi and pan.commit modules.

Documentation:

  doc/panxapi.html
  doc/pan.xapi.html

Install:

  You can install the package or just run the programs from within
  the package source directory:

    $ tar xzf pan-python-1.0.0.tar.gz
    $ cd pan-python-1.0.0

    $ cd bin
    $ ./panxapi.py

  or:

    $ sudo ./setup.py install
    $ panxapi.py

Author:

  Kevin Steves <kevin.steves@pobox.com>

$Id: README.txt,v 1.3 2013/03/06 23:42:04 stevesk Exp $
