..
 Copyright (c) 2014-2017 Kevin Steves <kevin.steves@pobox.com>

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
 submit link                      /publicapi/submit/link
 submit links                     /publicapi/submit/links
 submit verdict change request    /publicapi/submit/change-request
 get previously uploaded sample   /publicapi/get/sample
 get sample PCAP                  /publicapi/get/pcap
 get sample analysis report       /publicapi/get/report
 get sample verdict               /publicapi/get/verdict
 get sample verdicts              /publicapi/get/verdicts
 get verdicts changed             /publicapi/get/verdicts/changed
 get URL web artifacts            /publicapi/get/webartifacts
 get sample malware test file     /publicapi/test/**file_type**
 ==============================   ========

pan.wfapi Constants
-------------------

 **__version__**
  pan package version string.

 **DEBUG1**, **DEBUG2**, **DEBUG3**
  Python ``logging`` module debug levels (see **Debugging and
  Logging** below).

 **BENIGN**, **MALWARE**, **GRAYWARE**, **PHISHING**, **C2**, **PENDING**, **ERROR**, **UNKNOWN**, **INVALID**
  Constants for the integer verdict values.

 **VERDICTS**
  A dictionary which maps the integer verdict values to a tuple
  of (name, description).


pan.wfapi Constructor and Exception Class
-----------------------------------------

class pan.wfapi.PanWFapi()
~~~~~~~~~~~~~~~~~~~~~~~~~~
 ::

  class pan.wfapi.PanWFapi(tag=None,
                           hostname=None,
                           api_key=None,
                           timeout=None,
                           http=False,
                           ssl_context=None,
                           agent=None)

 **tag**
  .panrc tagname.

 **hostname**
  URI hostname used in API requests.    This can also be
  specified in a .panrc file using the ``hostname`` *varname*.

  This is used to specify an alternate cloud (e.g.,
  ``beta.wildfire.paloaltonetworks.com``) or a WildFire appliance.

  The default is ``wildfire.paloaltonetworks.com``.

 **api_key**
  ``api_key`` argument used in API requests.  This can also be
  specified in a .panrc file using the ``api_key`` *varname*.

 **timeout**
  The ``timeout`` value for urlopen() in seconds.

 **http**
  Use *http* URL scheme for API requests.  This can be used with the
  ``testfile()`` method to get a malware test file over HTTP.

 **ssl_context**
  An ssl.SSLContext() to use for HTTPS requests.  An SSL context holds
  data such as SSL configuration options and certificates.

  This can be used to specify the ``cafile``, ``capath`` and other SSL
  configuration options.

  When ``ssl_context`` is *None*, if the **certifi** package is
  installed its Certificate Authority (CA) bundle is used for SSL
  server certificate verification, otherwise no changes are made to
  the default **ssl** module settings.

  The default is *None*.

 **agent**
  Specify the API key type for Prisma API keys:

   **pcc** - Prisma Cloud Compute-based WildFire public API key

   **prismaaccessapi** - Prisma Access-based WildFire public API key

exception pan.wfapi.PanWFapiError
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 Exception raised by the PanWFapi class when an error occurs.  The
 string representation of an instance of this exception will contain a
 user-friendly error message.

pan.wfapi.PanWFapi Methods
--------------------------

submit(file=None, url=None, links=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``submit()`` method submits a file, URL or web page links to
 WildFire for analysis.

 **file**
  Path to a file to submit for analysis.

 **url**
  URL to a file to submit for analysis.

 **links**
  List of links (URLs to web pages) to submit for analysis.
  A maximum of 1,000 links can be submitted in a request.

 You must submit one of **file**, **url** or **links**.

change_request(hash=None, verdict=None, email=None, comment=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``change_request()`` method is used to request a manual review
 of a sample's verdict by the Threat Research Team.

 **hash**
  The SHA256 hash for the sample.

 **verdict**
  The suggested integer verdict.

 **email**
  Notification e-mail address.

 **comment**
  Explanation for the change request.  Can be up to 2048 bytes.

sample(hash=None)
~~~~~~~~~~~~~~~~~

 The ``sample()`` method gets a previously uploaded sample file.  The
 sample can be specified by its MD5 or SHA256 hash.

report(hash=None, format=None, url=url)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``report()`` method gets an analysis report for a previously uploaded
 sample.

 **hash**
  An MD5 or SHA256 hash of the sample.  This cannot be a link hash.

 **format**
  WildFire report output format string:

   **xml** - XML document (default when the **hash** parameter is used)

   **pdf** - PDF document

   **maec** - `Malware Attribute Enumeration and Characterization <https://maecproject.github.io/about-maec/>`_ JSON document

   **json** - JSON document.  This can only be specified for URL
   analysis verdicts, and is the default when the **url** parameter
   is used.

 **url**
  A web page URL.  The **url** parameter is used to retrieve verdicts that
  have been processed using
  `URL analysis <https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-whats-new/latest-wildfire-cloud-features/url-analysis>`_.

verdict(hash=None, url=url)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``verdict()`` method gets a single verdict for a previously
 analyzed sample or link (URL).

 **hash**
  An MD5 or SHA256 hash.  For links, this is a hash of the URL, and is
  used to retrieve verdicts that have been processed using the legacy URL
  analyzer.

 **url**
  A web page URL.  The **url** parameter is used to retrieve verdicts that
  have been processed using
  `URL analysis <https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-whats-new/latest-wildfire-cloud-features/url-analysis>`_.

 Palo Alto Networks recommends using the **url** parameter when
 retrieving web page verdicts for the most accurate and up to date
 information.

 The result is an XML document with verdict represented as an integer:

 =====  ========  ===========
 Value  Verdict   Description
 =====  ========  ===========
 0      benign
 1      malware
 2      grayware
 4      phishing
 5      C2        command-and-control
 -100   pending   sample exists and verdict not known
 -101   error     sample is in error state
 -102   unknown   sample does not exist
 -103   invalid   hash is invalid
 =====  ========  ===========

verdicts(hashes=None)
~~~~~~~~~~~~~~~~~~~~~

 The ``verdicts()`` method gets verdicts for previously analyzed
 samples and links (URLs).

 **hashes**
  A list of up to 500 MD5 or SHA256 hashes.  For links, this is a hash
  of the URL.

 The result is an XML document with verdict represented as an integer.

verdicts_changed(date=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``verdicts_changed()`` method gets the hashes of samples whose
 verdicts have changed within the last 30 days starting at the date
 specified.  The format for the **date** argument is *YYYY-MM-DD*.

pcap(hash=None, platform=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``pcap()`` method gets a PCAP (packet capture) file of network
 activity for a previously uploaded sample.  The sample can be
 specified by its MD5 or SHA256 hash.  The sandbox environment for the
 PCAP can optionally be specified using the platform ID.  If no
 platform is specified a PCAP from an environment that resulted in a
 *Malware* verdict is returned.

 Platform IDs are documented in the
 `Get a Packet Capture <https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-api/get-wildfire-information-through-the-wildfire-api/get-a-packet-capture-wildfire-api.html>`_
 section of the *WildFire API Reference*.

web_artifacts(\*, url=None, types=None)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

 The ``web_artifacts`` method gets web artifacts discovered during
 analysis of the specified web page URL.  Artifacts can include a JPEG
 screen shot of the page and files downloaded during analysis.
 Artifacts are provided in a compressed tar archive (.tgz) file, and
 the file is placed in the ``attachment`` data attribute.

 **url**
  A web page URL.  The **url** parameter is used to retrieve artifacts
  discovered using
  `URL analysis <https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-whats-new/latest-wildfire-cloud-features/url-analysis>`_.

 **types**
  A comma separated string of artifact types:

  ===============   ===========
  Artifact Type     Description
  ===============   ===========
  screenshot        JPEG screen shot
  download_files    files downloaded during analysis
  ===============   ===========

  The default is to include both a screen shot and files downloaded in
  the tar archive (``screenshot,download_files``).

testfile(file_type=None)
~~~~~~~~~~~~~~~~~~~~~~~~

 The ``testfile()`` method gets a sample malware test file.  Each
 request returns a similar file named
 ``wildfire-test-``\ *file_type*\ ``-file`` with a different hash
 and with verdict *Malware*.

 **file_type** is one of the following file types:

 ==========  ===========  ===========
 File Type   File Suffix  Description
 ==========  ===========  ===========
 pe          .exe         Portable Executable format
 apk         .apk         Android Package
 macos       none         MacOSX
 elf         none         Executable and Linkable Format
 ==========  ===========  ===========

 The default is ``pe``.

 This requires an ``api_key`` even though it is not
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

 Status codes that can be returned include:

 ===============================  ===========
 HTTP status-code, reason-phrase  Description
 ===============================  ===========
 401 Unauthorized                 API key invalid
 403 Forbidden                    Permission denied
 404 Not Found                    Report/sample/pcap not found
 405 Method Not Allowed           Must use method POST
 413 Request Entity Too Large     Sample size exceeds maximum
 418                              Invalid file type
 419 Quota Exceeded               Maximum daily uploads exceeded
 419 Quota Exceeded               Maximum daily queries exceeded
 420 Insufficient Arguments       Missing required request parameter
 421 Invalid Argument             Invalid request parameter
 422 URL Download Error           URL download error
 456                              Invalid request
 513                              File upload failed
 ===============================  ===========

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

 The ``response_type`` data attribute is set to the type of the
 response:

  **xml** - the message body is an XML document (*application/xml*)

  **txt** - the message body is text (*text/plain*)

  **html** - the message body is an HTML document (*text/html*)

  **json** - the message body is a JSON document (*application/json*)

Debugging and Logging
---------------------

 The Python standard library ``logging`` module is used to log debug
 output; by default no debug output is logged.

 In order to obtain debug output the ``logging`` module must be
 configured: the logging level must be set to one of **DEBUG1**,
 **DEBUG2**, or **DEBUG3** and a handler must be configured.
 **DEBUG1** enables basic debugging output and **DEBUG2** and
 **DEBUG3** specify increasing levels of debug output.

 For example, to configure debug output to **stderr**:
 ::

  import logging

  if options['debug']:
      logger = logging.getLogger()
      if options['debug'] == 3:
          logger.setLevel(pan.wfapi.DEBUG3)
      elif options['debug'] == 2:
          logger.setLevel(pan.wfapi.DEBUG2)
      elif options['debug'] == 1:
          logger.setLevel(pan.wfapi.DEBUG1)

      handler = logging.StreamHandler()
      logger.addHandler(handler)

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

 Advanced Wildfire Administration
  https://docs.paloaltonetworks.com/advanced-wildfire

 WildFire API Reference
  https://docs.paloaltonetworks.com/wildfire/u-v/wildfire-api.html

AUTHORS
=======

 Kevin Steves <kevin.steves@pobox.com>
