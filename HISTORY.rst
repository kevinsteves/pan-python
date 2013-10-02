Release History
===============

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
