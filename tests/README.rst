pan-python Tests
================

``pan-python`` tests use the Python `unit testing framework
<https://docs.python.org/3/library/unittest.html>`_.

Test Naming
-----------

Tests can be created for any of the components in ``pan-python`` using
the following naming convention:

  ====================  ==================
  pan-python Component  Test Script Prefix
  ====================  ==================
  PAN-OS XML API        *test_xapi_*
  PAN-OS Licensing API  *test_licapi_*
  WildFire API          *test_wfapi_*
  AutoFocus API         *test_afapi_*
  ====================  ==================

Tests are currently available for the following components:

- PAN-OS XML API

PAN-OS XML API Tests
--------------------

A lab PAN-OS firewall or Panorama are required to run tests.

PAN-OS XML API tests can be performed on the following targets:

  ==================================================  ===========
  Test Target                                         Target Name
  ==================================================  ===========
  PAN-OS firewall                                     **fw**
  Panorama                                            **pano**
  PAN-OS firewall via Panorama to device redirection  **tgt**
  ==================================================  ===========

Test scripts use the following naming convention to define the valid
test targets:

  ===============  ========================  ============
  Target Names     Test Script Prefix        Test Targets
  ===============  ========================  ============
  **fw**           *test_xapi_fw_*           PAN-OS firewall only
  **pano**         *test_xapi_pano_*         Panorama only
  **fw_pano**      *test_xapi_fw_pano_*      PAN-OS firewall or Panorama
  **fw_tgt**       *test_xapi_fw_tgt_*       PAN-OS firewall or firewall via Panorama to device redirection
  **fw_tgt_pano**  *test_xapi_fw_tgt_pano_*  PAN-OS firewall, Panorama or firewall via Panorama to device redirection
  ===============  ========================  ============

Specifying Test Target
~~~~~~~~~~~~~~~~~~~~~~

A `.panrc file
<https://github.com/kevinsteves/pan-python/blob/master/doc/panrc.rst>`_
is used to reference the test target by a *tagname*.

Export the ``XAPI_TAG`` environment variable with the *tagname* to
use from a .panrc file:
::

  $ export XAPI_TAG=vm-50-3

Panorama to Device Redirection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Panorama to device redirection can be used to perform XML API
requests to connected devices via Panorama using the ``target=serial``
API request argument.  To execute tests using Panorama to device
redirection the ``.panrc`` *hostname* specifies the Panorama and
the *serial* specifies the connected device:
::

  $ grep vm-50-3-panorama .panrc
  # vm-50-3-panorama
  hostname%vm-50-3-panorama=172.25.2.100
  api_username%vm-50-3-panorama=admin
  api_password%vm-50-3-panorama=password
  serial%vm-50-3-panorama=015351000046877

Run Tests
~~~~~~~~~

To run tests from the top-level directory:
::

  $ python3 -m unittest discover -v -s tests -t . -p TARGET-PATTERN

To run tests from the ``tests/`` directory:
::

  $ python3 -m unittest discover -v -t .. -p TARGET-PATTERN

Examples
~~~~~~~~

From the ``tests/`` directory run tests to a Panorama target:
::

  $ XAPI_TAG=panorama-2 python3 -m unittest discover -v -t .. -p 'test_xapi_*pano*'
  test_01 (tests.test_xapi_fw_tgt_pano_export.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_log.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_log.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_op.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_op.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_report.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_user_id.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_user_id.PanXapiTest) ... ok

  ----------------------------------------------------------------------
  Ran 8 tests in 6.184s

  OK

From the ``tests/`` directory run tests to a firewall target:
::

  $ XAPI_TAG=vm-50-3 python3 -m unittest discover -v -t .. -p 'test_xapi_*fw*'
  test_01 (tests.test_xapi_fw_tgt_config.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_multi_config.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_multi_config.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_export.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_log.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_log.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_op.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_op.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_report.PanXapiTest) ... ok
  test_01 (tests.test_xapi_fw_tgt_pano_user_id.PanXapiTest) ... ok
  test_02 (tests.test_xapi_fw_tgt_pano_user_id.PanXapiTest) ... ok

  ----------------------------------------------------------------------
  Ran 11 tests in 19.983s

  OK
