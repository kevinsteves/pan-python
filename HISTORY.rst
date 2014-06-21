Release History
===============

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
