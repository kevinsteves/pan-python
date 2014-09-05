..
 Copyright (c) 2014 Kevin Steves <kevin.steves@pobox.com>

 Permission to use, copy, modify, and distribute this software for any
 purpose with or without fee is hereby granted, provided that the above
 copyright notice and this permission notice appear in all copies.

 THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
 WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
 MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
 ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
 WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
 ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
 OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

=========
pan.wfapi
=========

------------------------------------
Python interface to the WildFire API
------------------------------------

NAME
====

 pan.wfapi - Python interface to the WildFire API

SYNOPSIS
========
::

 import pan.wfapi

 try:
     wfapi = pan.wfapi.PanWFapi(tag='wildfire')

 except pan.wfapi.PanWFapiError as msg:
     print('pan.wfapi.PanWFapi:', msg, file=sys.stderr)
     sys.exit(1)

 sample = '/var/wildfire/samples/sample1.exe'

 try:
     wfapi.submit(file=sample)

 except pan.wfapi.PanWFapiError as msg:
     print('submit:', msg, file=sys.stderr)
     sys.exit(1)

 print('sample %s submitted' % sample)
 print(wfapi.response_body)

DESCRIPTION
===========

 The pan.wfapi module defines the PanWFapi class, which provides an
 interface to the WildFire API.

 PanWFapi provides an interface to all WildFire API requests:

 ==============================   ========
 Request                          URI path
 ==============================   ========
 submit file                      /publicapi/submit/file
 submit URL                       /publicapi/submit/url
 get previously uploaded sample   /publicapi/get/sample
 get sample PCAP                  /publicapi/get/pcap
 get sample analysis report       /publicapi/get/report
 get sample malware test file     /publicapi/test/pe
 ==============================   ========

pan.wfapi Attributes
--------------------

 **__version__**
  pan package version string.

pan.wfapi Constructor and Exception Class
-----------------------------------------

class pan.wfapi.PanWFapi()
~~~~~~~~~~~~~~~~~~~~~~~~~~
 ::

  class pan.wfapi.PanWFapi(debug=0,
                           tag=None,
                           hostname=None,
                           api_key=None,
                           timeout=None,
                           http=False,
                           cacloud=True,
                           cafile=None,
                           capath=None)

 **debug**
  Debug level.  Can be 0-3; 0 specifies no debugging output and 1-3
  specifies increasing debugging output written to *stderr*.

 **tag**
  .panrc tagname.

 **hostname**
  URI hostname used in API requests.    This can also be
  specified in a .panrc file using the ``hostname`` *varname*.

  This is used to test alternate clouds (e.g.,
  ``beta.wildfire.paloaltonetworks.com``).

  The default is ``wildfire.paloaltonetworks.com``.

 **api_key**
  ``api_key`` argument used in API requests.  This can also be
  specified in a .panrc file using the ``api_key`` *varname*.

 **timeout**
  The ``timeout`` value for urlopen() in seconds.

 **http**
  Use *http* URL scheme for API requests.  This can be used with the
  ``testfile()`` method to get a malware test file over HTTP.

 **cacloud**
  By default SSL server certificate verification is performed using
  the Go Daddy Class 2 Certification Authority Root Certificate which
  is used by the WildFire cloud and is stored in the PanWFapi class.
  ``cacloud=False`` can be used to disable verification for test clouds
  or if the cloud CA changes.

  urlopen() only supports SSL server certificate verification in
  Python version 3.2 and greater.  

 **cafile**
  The ``cafile`` value for urlopen().  ``cafile`` is a file containing
  CA certificates to be used for SSL server certificate
  verification. By default the SSL server certificate is not verified.
  ``cafile`` is only supported in Python version 3.2 and greater.

 **capath**
  The ``capath`` value for urlopen().  ``capath`` is a directory of
  hashed certificate files to be used for SSL server certificate
  verification. By default the SSL server certificate is not verified.
  ``capath`` is only supported in Python version 3.2 and greater.

exception pan.wfapi.PanWFapiError
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Exception raised by the PanWFapi class when an error occurs.  The
 string representation of an instance of this exception will contain a
 user-friendly error message.

pan.wfapi.PanWFapi Methods
--------------------------

submit(file=None, url=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``submit()`` method submits a file or URL to WildFire for analysis.

sample(hash=None)
~~~~~~~~~~~~~~~~~

 The ``sample()`` method gets a previously uploaded sample file.  The
 sample can be specified by its MD5 or SHA256 hash.

report(hash=None, format=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``report()`` method gets an analysis report for a previously uploaded
 sample.  The sample can be specified by its MD5 or SHA256 hash.
 The report format can be ``xml`` or ``pdf``.  The default is ``xml``.

pcap(hash=None, platform=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``pcap()`` method gets a PCAP (packet capture) file of network
 activity for a previously uploaded sample.  The sample can be
 specified by its MD5 or SHA256 hash.  The sandbox environment for the
 PCAP can optionally be specified using the platform ID.  If no
 platform is specified a PCAP from an environment that resulted in a
 *Malware* verdict is returned.

 Valid platform IDs are:

 ===========  ===================
 Platform ID  Sandbox Environment
 ===========  ===================
 1            Windows XP, Adobe Reader 9.3.3, Office 2003
 2            Windows XP, Adobe Reader 9.4.0, Flash 10, Office 2007
 3            Windows XP, Adobe Reader 11, Flash 11, Office 2010
 4            Windows 7, Adobe Reader 11, Flash 11, Office 2010
 201          Android 2.3, API 10, avd2.3.1
 ===========  ===================

testfile()
~~~~~~~~~~

 The ``testfile()`` method gets a sample malware test file.  Each request
 returns a similar PE (Portable Executable) file named
 ``wildfire-test-pe-file.exe`` with a different hash and with verdict
 *Malware*.

 This currently requires an ``api_key`` even though it is not
 needed for the API request.

attachment
~~~~~~~~~~

 The ``attachment`` data attribute is a dictionary used to access a
 downloaded file's filename and content; it will contain two keys:

 ========  =====
 Key       Value
 ========  =====
 filename  filename field in content-disposition header
 content   file content from HTTP message body
 ========  =====

http_code
~~~~~~~~~

 The ``http_code`` data attribute contains the HTTP response status
 code.

http_reason
~~~~~~~~~~~

 The ``http_reason`` data attribute contains the HTTP response reason
 phrase.

response_body
~~~~~~~~~~~~~

 The ``response_body`` data attribute contains the HTTP response
 message body.

response_type
~~~~~~~~~~~~~

 The ``response_type`` data attribute is set to ``xml`` when the message
 body is an XML document.

FILES
=====

 ``.panrc``
  .panrc file

EXAMPLES
========

 The **panwfapi.py** command line program calls each available
 PanWFapi method and can be reviewed for sample usage.

SEE ALSO
========

 panwfapi.py

AUTHORS
=======

 Kevin Steves <kevin.steves@pobox.com>
