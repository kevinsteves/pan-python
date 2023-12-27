Release History
===============

0.24.0 (2023-12-26)
-------------------

- tests/test_wfapi_cld_web_artifacts.py: Update URL, 0.0.0.0 now has
  404 status.

- tests/test_wfapi_cld_submit_url.py: Wait up to 300 seconds for
  report to be available.

- tests/test_wfapi_cld_appl_verdict.py: Fix test_04 to work until bug
  fixed.

- tests/wfapi_mixin.py: commit missing test file.

- Add support for type=import API request.

0.23.0 (2023-11-19)
-------------------

- Rename test filename, log() method does not support Panorama to
  device redirection.

- Use 11.1 documentation links.

- pan.xapi, pan.xapi.rst, panxapi.rst: Modified version of
  https://github.com/kevinsteves/pan-python/pull/54
  from Matthew Kazmar.

  type=export request supports target argument.

- tests/test_xapi_fw_tgt_multi_config.py: PAN-196392 is fixed.

- tests/test_xapi_fw_tgt_multi_config.py: Error message changed.

- pan.config: Support 11.1.0 config for set format.

0.22.0 (2023-03-07)
-------------------

- pan.config: Support 11.0.0 config for set format.

0.21.0 (2023-01-13)
-------------------

- pan.wfapi: Add C2 verdict.

- pan.wfapi, pan.rc: Add agent argument to constructor.  Agent is used
  to specify the API key type for Prisma API keys.  Can be specified
  in .panrc; no command line argument at this time.

- pan.wfapi: Remove handling for no ssl.CertificateError.

- pan.wfapi: Remove handling of Python 2.7 HTTP reason.

- pan.wfapi: Remove checks for Python version around ssl module.

- pan.wfapi, panwfapi.py: Add support for url parameter to report()
  and verdict().

- pan.wfapi: Remove old check for ssl.SSLContext().

- Fix some pycodestyle issues.

- pan.wfapi, panwfapi.py: Add support for the get URL web artifacts
  API request.

- Add unit tests for the WildFire API.

- Use 11.0 documentation links.

- pan.xapi: Modified version of
  https://github.com/kevinsteves/pan-python/pull/47
  from Justin Bradfield.

  1. Use urlopen() as a context manager
  2. Immediately read() response
  3. Set object 'pan_body' attribute to read() result

- panxapi.py: IOError merged into OSError as of Python 3.3.

0.20.0 (2022-08-31)
-------------------

- pan.xapi: Panorama to device redirection (target=) is allowed for
  type=report.

- Add support for type=config&action=multi-config XML API request
  which provides a mechanism to perform multiple configuration API
  requests with transactional support.

- pan.xapi: Remove PAN-OS 8.0 TLS warning from 2017.

- Add tests for PAN-OS XML API.

0.19.0 (2022-04-21)
-------------------

- NOTE: Python 3 only release; Python 2 support is removed.  In
  general will plan to support the supported Python releases (with bug
  and security updates); currently >= 3.7.

- Switch to pyproject.toml based build system.

0.18.0 (2022-04-13)
-------------------

- pan.afapi, pan.afapi.rst: Workaround for autofocus API bug. Use
  af_in_progress to determine search completion. At some point,
  af_message was changed from "complete" to "success" to indicate
  search completion.

0.17.0 (2022-03-19)
-------------------

- pan.config: Support 10.0.0 and 10.1.0 config for set format.

- Use 10.1 documentation links.

- pan.config: Support 10.2.0 config for set format.

- Use 10.2 documentation links.

0.16.0 (2020-01-11)
-------------------

- pan.config: Support 9.1.0 config for set format.

- pan.licapi: 'version' field in request header should use version
  attribute and not int().  This was not noticed because version:256
  would previously use the current API version of 1.  Bug found by
  Stacey Sheldon.

- pan.licapi.rst: Document pan.licapi._ApiVersion int() layout
  correctly.

- Use 9.1 documentation links.

- panwfapi.py: Fix 'SyntaxWarning: "is" with a literal. Did you mean
  "=="?' warning from Python 3.8.

- setup.py: Add Python 3.8.

0.15.0 (2019-07-18)
-------------------

- pan.afapi: Automatic int conversions have been deprecated in
  Python3.  See: https://bugs.python.org/issue27672

- Use 9.0 documentation links.

- pan.wfapi, panwfapi.py, pan.wfapi.rst, panwfapi.rst: Add support for
  retrieving additional malware test file types.

- pycodestyle fixes.

- pan.licapi, pan.afapi: Remove verbose argument from namedtuple() for
  Python 3.7.  From Michael Richardson.

0.14.0 (2018-12-22)
-------------------

- setup.py: Cleanup and switch to setuptools.  Will now also publish
  wheels to PyPI.  Classify as Production/Stable.

- Rename README.txt to README.rst and shrink.

- pan.config: Support 9.0.0 config for set format.

0.13.0 (2018-04-29)
-------------------

- Documentation fixes.

- pan.config: Support 8.1.0 config for set format.

- Use 8.1 documentation links.

0.12.0 (2017-05-28)
-------------------

- Add documentation for panafapi.py.

- Documentation fixes.

- panxapi.py: For json.dumps() use separators=(',', ': ') so -j output
  is the same with py2 and py3 (this is the default when indent is not
  None starting in 3.4).

- panxapi.py: Allow -t '' which is the same as no tag but can also be
  used to create tag-less entries for a .panrc.

- pan.config: Quote set argument with single quotes if it contains a
  double quote.

0.11.0 (2017-03-31)
-------------------

- pan.wfapi.rst, panwfapi.rst: Reference "WildFire API Reference" for
  platform ID documentation.

- Use 8.0 documentation links.

- pan.config: Add XPaths for 8.0.

- Add a Python and command line interface to the PAN-OS licensing API.

- panwfapi.py, pan.wfapi: Add phishing verdict.

- pan.xapi: When URLError try to deduce if it's a SSL handshake error
  and if OpenSSL may not support TLS 1.1, and log warning at DEBUG1
  that PAN-OS 8.0 does not allow TLS 1.0 connections by default.

- pan.xapi, pan.afapi, pan.wfapi: log ssl.OPENSSL_VERSION at DEBUG3.

- pan.xapi.rst: Fix cut-paste error in xml_result().

- Remove Python 3.[23] and add 3.5 to supported list.  3.[23] should
  continue to work however I'm not testing with them.

- pan.wfapi, pan.xapi: Handle ssl.CertificateError exception.

- pan.wfapi: Fix raise of PanXapiError vs. PanWFapiError.

- pan.config: Add XPaths used for XML to set translation in 7.0 and 7.1.

- pan.xapi: Add undocumented feature to use pre PAN-OS 4.1 API request
  URI and commit request.  From Darlene Wong.

0.10.0 (2016-07-23)
-------------------

- pan.http: Use email.message_from_string() for the headers attribute,
  which is now an email.message.Message object:

    https://docs.python.org/2/library/email.message.html

  encoding attribute now set with Message get_content_charset()
  method.

  Add content_type attribute using Message get_content_type() method.

  NOTE: this *may* introduce an incompatibility depending on how you
  were using pan.afapi.PanAFapiRequest http_headers.

- pan.http: If using urllib and no content-type header urlencode data
  so application/x-www-form-urlencoded request works.

- panxapi.rst: Add link to "PAN-OS XML API Labs with pan-python".

- Updated documentation links to PAN-OS 7.1.

- pan.xapi, pan.wfapi: Sanitize secrets in debug output.

- pan.wfapi, bin/panwfapi.py: Deprecate the use of
  pan.wfapi.cloud_ssl_context() for SSL server certificate
  verification.

  NOTE: Changes are backwards compatible however use of
  cloud_ssl_context() is not recommended.

  If your operating system certificate store is insufficient you can
  install certifi (https://pypi.python.org/pypi/certifi) and its CA
  bundle will now be used for SSL server certificate verification when
  ssl_context is None.

- pan.xapi: Allow Python 2.6 as a one-off while still using
  sys.version_info.major named attribute.

- pan.xapi, panxapi.py: Support for type=report API request.  Joint
  effort with Andrew Stanton.

0.9.1 (2016-03-09)
------------------

- panrc.rst: AutoFocus API uses .panrc also.

- pan.rc: Sanitize secrets in debug output.

- pan.http: Handle ssl.CertificateError exception.

- panxapi.py: api_password now optional for -l; when not specified the
  user is prompted for the password (using getpass.getpass()).

0.9.0 (2016-01-27)
------------------

- AutoFocus API support.

- panwfapi.py: Add hash length to hash invalid length message.

- pan.wfapi: Use email package for HTTP header retrieval and parsing;
  also fixes potential issue with not handling a quoted filename in
  content-disposition header.

      content-disposition: attachment; filename="sample"

0.8.0 (2015-10-17)
------------------

- Don't override default Exception class __init__() and __str__()
  methods since we don't change anything.

- pan.wfapi: Restore behaviour of allowing non-2XX response codes to
  fall through urlopen() that was erroneously removed in previous SSL
  handling/PEP 476 changes.

- pan.xapi: For commit sync=True, sleep at the top of the loop so we
  don't poll immediately after commit.

- pan.wfapi: Mention WildFire appliance in the module docstring.

- pan.wfapi, panwfapi.py: Rework SSL handling to use SSL context and
  recognize PEP 476 changes in Python 2.7.9 and 3.4.3.  Greatly
  simplifies SSL certificate verification.

  NOTE INCOMPATIBLE CHANGES:

  pan.wfapi.PanWFapi(): cacloud, cafile, capath removed.
  ssl_context added.

  panwfapi.py: --cacloud removed.  --ssl added.

- panxapi.py: If a .panrc tagname is specified with -k the output will
  be hostname and api_key varname values for use in a .panrc file.

- panwfapi.rst: hostname can also specify a WildFire appliance.

- panwfapi.py: Allow --date to be specified as -days or 0 for today.

- Use 7.0 links to documentation.

- reStructuredText blank line cleanup.

- pan.wfapi, panwfapi.py: Add support for /publicapi/submit/link(s)
  requests.

- pan.wfapi, panwfapi.py: Add support for WildFire API
  /publicapi/submit/change-request request.

0.7.0 (2015-05-25)
------------------

- pan.xapi: Allow xml_result() to match result in report output.

- pan.config: Fix typo causing Panorama 6.1 xpaths to not be used.

- panrc.rst:  Add section on .panrc file permissions.

- panxapi.py: Use lstrip('\r\n').rstrip() on response XML and message
  before printing.

- Fix a bug where we only processed the first node for -pjr when there
  was more than one node.

- Move .panrc documentation to a separate document.

- Documentation: /publicapi/get/verdicts allows up to 500 hashes.

0.6.0 (2015-03-20)
------------------

- Don't name the internal log function log as this steps on the log()
  method in pan.xapi; change in all modules for consistency.

- panwfapi.rst: Typo in WildFire .panrc example.

- pan.xapi: type=report&reporttype=predefined response does not return
  charset in content-type. Fix to be more liberal in what we accept.

- pan.wfapi.rst: Fix wrong variable in Debugging and Logging example.

- pan.xapi: Document element_root data attribute.

- panxapi.py: Missed a use of pan.xapi.xml_python() when it was
  removed.

- panxapi.py: Fix --ls (formatted PCAP listing), which has been broken
  since 5.0 due to XML response format changes.

- pan.xapi: Workaround bug in 5.0 and 6.0: export PCAP response
  incorrectly uses content-type text/plain instead of
  application/octet-stream.

- panxapi.py, pan.xapi: Add support for the extended packet capture
  feature added in PAN-OS 6.0 which is used for threat PCAPs.

- panxapi.py: Files besides PCAP can be exported that are returned as
  attachments (e.g., device-state), so rename save_pcap() to
  save_attachment().

- pan.xapi: Add text_document data attribute which contains the
  message body from the previous API request when the response
  content-type is text/plain.

- panxapi.py: Add --text option to print text to stdout.

- panxapi.py, pan.xapi: Allow --ad-hoc to be used to modify (replace)
  and augment (add to) the standard parameters in the request.

- Add reference to PAN-OS and WildFire documentation to SEE ALSO
  sections of the documentation.

- panxapi.py: Can export more than PCAP files; update documentation
  and usage.

- Add Python 3.4 to supported list.

- pan.xapi: When an XML response does not contain a status attribute
  (e.g., export configuration), set to 'success'.

- pan.xapi: If ElementTree has text use for start of xml_result()
  string.

- pan.xapi.op(): Handle multiple double quoted arguments for
  cmd_xml=True.

- panxapi.py: When -r is specified without any of -xjp, -x is now
  implied.

- pan.config: Add PAN-OS 6.1 for set CLI.

- pan.wfapi: Don't override self._msg in __set_response() if already
  set.  Handle case on non 2XX HTTP code and no content-type in
  response.

- panxapi.py: Print warning if extra arguments after xpath.

- pan.xapi: Address changes to Python 2.7.9 and 3.4.3 which now
  perform SSL server certificate verification by default (see PEP
  476).  Maintains past behaviour of no verification by default.

  NOTE: this removes the cafile and capath arguments from PanXapi()
  and adds ssl_context.

- pan.wfapi, panwfapi.py: Add support for:
    get sample verdict               /publicapi/get/verdict
    get sample verdicts              /publicapi/get/verdicts
    get verdicts changed             /publicapi/get/verdicts/changed

- pan.wfapi.rst: Add table with HTTP status codes that can be
  returned.

- pan.wfapi: Add constants for verdict integer values.

- pan.wfapi: Remove HTTP status code reason phrases that are returned
  by default now.

- Set SIGPIPE to SIG_DFL in panxapi.py for consistency with panconf.py
  and panwfapi.py.  This is needed on some systems when piping to
  programs like head so we don't see BrokenPipeError.  Also handle
  AttributeError for Windows which doesn't have SIGPIPE.

0.5.0 (2014-10-22)
------------------

- Change debug messages in modules from print to stderr to log using
  the logging module.  See the section 'Debugging and Logging' in
  pan.wfapi.rst and pan.xapi.rst for an example of configuring the
  logging module to enable debug output.

  IMPORTANT NOTE: the debug argument has been removed from the
  constructors, so programs using them must be modified.

- Add platform ID for Windows 7 64-bit sandbox to WildFire
  documentaton.

- Fix bug in panconf.py: positional arguments not initialized to none
  in conf_set()

- Remove undocumented xml_python() method from pan.xapi and pan.wfapi.
  Use pan.config if you need this.

- Add 'serial' varname to .panrc.  Allows you to have tags which
  reference a Panorama managed device via redirection.  Suggested by
  Jonathan Kaplan.

- Add example to panxapi.rst: Print operational command variable using
  shell pipeline.

- Document --sync, --interval, --timeout for panxapi.py

- Add --validate to panxapy.py which runs commit with a cmd argument
  of <commit><validate></validate></commit> to validate the
  configuration.  This is a new feature in PAN-OS 6.0.

- Fix keygen() to return api_key as documented.

- Add support for type=config&action=override.  From btorres-gil

0.4.0 (2014-09-14)
------------------

- WildFire API support.

0.3.0 (2014-06-21)
------------------

- PEP8 cleanup.

- fix unintended _valid_part to valid_part variable name change in
  pan.config.

- handle type=user-id register and unregister response messages.
  suggested and initial diff by btorresgil.

- fix serial number (target API argument) not set in type=commit;
  from btorresgil.

- fix debug print to stdout vs. stderr in pan.xapi.

- changes for PyPI upload in setup.py.

0.2.0 (2014-03-22)
------------------

- various PEP8 cleanup.

- use HISTORY.rst for changes/release history vs. CHANGES.txt.

- add panconf.py, a command line program for managing PAN-OS XML
  configurations.

- add Panorama 5.1 (same as 5.0) for set CLI.

- add PAN-OS 6.0 XPaths for set CLI.

- pan.xapi: use pan.config for XML to Python conversion and remove
  duplicated code.

- I am developing with Python 3.3 by default now so add as supported.

- Rewrite XML response message parser to use xml.etree.ElementTree
  path/xpath to match each known format.  This will make it easier to
  support additional message formats.

  Multi-line messages (multiple line elements) are now newline
  delimited.

- operational command 'show jobs id nn' can have response with path
  './result/job/details/line'; if so set status_detail to text (can be
  multi-line).

- pan.xapi: if an XML response message is an empty string set it to
  None vs. ''.

- panxapi: print status line the same for exception/non-exception. We
  now quote message in non-exception case.

- handle ./newjob/newmsg within ./result/job/details/line of 'show
  jobs xxx' response.  the response message parser makes this easy
  now, but I'm still unsure if we really want to try to handle these
  things because the response formats are not documented.

- panxapi: add path value to --capath and --cafile argument usage.

- panxapi: don't print exception message if it's a null string.

- add --timeout and --interval options for use with --log to panxapi.

- rename pan.xapi log() sleep argument to interval and rework query
  interval processing slightly.

- add synchronous commit capability.

  TODO: more complete show job message parsing, especially for commit-all.

0.1.0 (2013-09-21)
------------------

- missing newline in debug.

- handle response with <msg><line><line>xxx</line></line>...

- in print_status() give priority to exception message over
  status_detail.

- use both code and reason from URLError exception for error message.

- Add support for log retrieval (type=log) to pan.xapi (see the log()
  method) and panxapi.py (see the --log option).

- reStructuredText cleanup.

- add example to retrieve report using the --ad-hoc option.

- Change name of distribution from PAN-python to pan-python.

- Add __version__ attribute and --version option.

- Add GitHub references to README and setup.py.

(2013-03-06)
------------

- initial release (on DevCenter)
