..
 NOTE: derived from documentation in PAN-perl

 Copyright (c) 2011 Palo Alto Networks, Inc. <info@paloaltonetworks.com>
 Copyright (c) 2013 Kevin Steves <kevin.steves@pobox.com>

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

==========
panxapi.py
==========

-----------------------------------------------------
command line program for accessing the PAN-OS XML API
-----------------------------------------------------

NAME
====

 panxapi.py - command line program for accessing the PAN-OS XML API

SYNOPSIS
========
::

 panxapi.py [options] [xpath]
    -d                    delete object at xpath
    -e element            edit XML element at xpath
    -g                    get candidate config at xpath
    -k                    generate API key
    -s                    show active config at xpath
    -S element            set XML element at xpath
    -U cmd                execute dynamic update command
    -C cmd                commit candidate configuration
    --force               force commit when conflict
    --partial part        commit specified part
    -A cmd                commit-all (Panorama)
    --ad-hoc query        perform ad hoc request
    --modify              insert known fields in ad hoc query
    -o cmd                execute operational command
    --export category     export PCAP files
    --log log-type        retrieve log files
    --src src             clone source node xpath
                          export source file/path/directory
    --dst dst             move/clone destination node name
                          rename new name
                          export destination file/path/directory
    --move where          move after, before, bottom or top
    --rename              rename object at xpath to dst
    --clone               clone object at xpath, src xpath
    --vsys vsys           VSYS for dynamic update/partial commit/
                          operational command
    -l api_username:api_password
    -h hostname
    -P port               URL port number
    --serial number       serial number for Panorama redirection/
                          commit-all
    --group name          device group for commit-all
    --merge               merge with candidate for commit-all
    --nlogs num           retrieve num logs
    --skip num            skip num logs
    --filter filter       log selection filter
    -K api_key
    -x                    print XML response to stdout
    -p                    print XML response in Python to stdout
    -j                    print XML response in JSON to stdout
    -r                    print result content when printing response
    -X                    convert text command to XML
    --ls                  print formatted pcap-listing to stdout
    --recursive           recursive export
    -H                    use http URL scheme (default https)
    -G                    use HTTP GET method (default POST)
    -D                    enable debug (multiple up to -DDD)
    -t tag                .panrc tagname
    -T seconds            urlopen() timeout
    --cafile path         file containing CA certificates
    --capath path         directory of hashed certificate files
    --version             display version
    --help                display usage

DESCRIPTION
===========

 **panxapi.py** is used to perform XML API requests on a PAN-OS
 firewall and Panorama.  It uses the PanXapi class from the
 **pan.xapi** module to execute API requests.

 The options are:

 ``-d``
  Perform the ``action=delete`` device configuration API request
  with the **xpath** argument.  ``delete`` is used to remove an existing
  object at the node specified by **xpath**.

 ``-e`` *element*
  Perform the ``action=edit`` device configuration API request with
  the **element** and **xpath** arguments.  ``edit`` is used to replace
  an existing object at the node specified by **xpath**.

  **element** can be an XML string, a path to a file containing XML,
  or the value **-** to specify the XML is on *stdin*.

 ``-g``
  Perform the ``action=get`` device configuration API request with the
  optional **xpath** argument.  ``get`` is used to retrieve the
  *candidate* configuration on the firewall.

 ``-k``
  Perform the ``type=keygen`` key generation API request with the
  **api_username** and **api_password** arguments.  This is
  used to generate an API key for the **-K** argument or a
  .panrc file.

 ``-s``
  Perform the ``action=show`` device configuration API request with
  the optional **xpath** argument.  ``show`` is used to retrieve the
  *active* configuration on the firewall.

 ``-S`` *element*
  Perform the ``action=set`` device configuration API request with the
  **element** and **xpath** arguments.  ``set`` is used to create a new
  object at the node specified by **xpath**.

  **element** can be an XML string, a path to a file containing XML,
  or the value **-** to specify the XML is on *stdin*.

 ``-U`` *cmd*
  Perform the ``type=user-id`` dynamic object update API request with the
  **cmd** argument and optional **--vsys** argument.  This is used to
  update dynamic objects including ip-user mappings and address objects.

  **cmd** can be an XML string, a path to a file containing XML,
  or the value **-** to specify the XML is on *stdin*.

 ``-C`` *cmd*
  Perform the ``type=commit`` commit configuration API request with
  the **cmd** argument.  This schedules a job to execute a
  configuration mode **commit** command to commit the candidate
  configuration.

  **cmd** can be an XML string, a path to a file containing XML,
  or the value **-** to specify the XML is on *stdin*.

  When *cmd* is the empty string the XML string will be created
  according to the **--force**, **--partial** and **--vsys** options
  specified.  If no commit options are specified it defaults to
  '<commit></commit>'.

 ``--force``
  Force the commit command in the event of conflict.

 ``--partial`` *part*
  Commit or exclude the specified *part* of the configuration.

  *part* can be:

  - device-and-network-excluded
  - policy-and-objects-excluded
  - shared-object-excluded
  - no-vsys
  - vsys

  **device-and-network-excluded** applies when the device is in
  single-vsys mode and **shared-object-excluded** applies when the device
  is in multi-vsys mode.

  Multiple parts can be specified by using multiple **--partial**
  options or separating each part with comma (,).  Virtual systems for
  the **vsys** part can be specified with **--vsys**.

 ``-A`` *cmd*
  Perform the ``type=commit`` commit configuration API request with
  the **cmd** argument and specify ``action=all``.  This
  is used to push shared policy from Panorama to managed firewalls.

  **cmd** can be an XML string, a path to a file containing XML,
  or the value **-** to specify the XML is on *stdin*.

  When *cmd* is the empty string the XML string will be created
  according to the **--serial**, **--group**, **--merge** and
  **--vsys** options specified.

 ``--ad-hoc`` *query*
  Perform an ad hoc (custom) API request using the query string specified.
  Query string must be field=value pairs separated by ampersand (**&**).
  The string will be URL-encoded before performing the API request.

  **--ad-hoc** can be used to construct API requests that are not
  directly supported by PanXapi.

 ``--modify``
  Modify an ad hoc query by inserting known fields.  By default
  the query is not modified.

  The known fields that can be inserted are:

  - xpath
  - key (api_key)
  - user (api_username)
  - password (api_password)
  - target (--serial)

 ``-o`` *cmd*
  Perform the ``type=op`` operational command API request with the
  **cmd** argument.

  **cmd** can be a text string (see **-X**), an XML string, a path to
  a file containing XML, or the value **-** to specify the XML is on
  *stdin*.

 ``--export`` *category*
  Perform the ``action=export`` export packet capture (PCAP) API request.

  *category* specifies the type of PCAP to export or list:

  - application-pcap
  - threat-pcap
  - filter-pcap

 ``--log`` *log-type*
  Perform the ``type=log`` retrieve log API request with the **log-type**
  argument.

  *log-type* specifies the type of log to retrieve and can be:

  - config
  - hipmatch
  - system
  - threat
  - traffic
  - url
  - wildfire

  Also see the **--nlogs**, **--skip** and **--filter** options.

 ``--src`` *src*
  Specify the source file, path or directory for **--export** and
  the source XPath for **--clone**.

  The **src** argument is used to specify:

  - date directory for application-pcap and threat-pcap PCAP file listing
  - PCAP file path for exporting application-pcap and threat-pcap
  - file name for exporting filter-pcap

 ``--dst`` *dst*
  The **--dst** argument is used with **--export** to specify:

  - a destination directory for exported file (retains original file name)
  - a file or path for exported file (file saved with new file name)

  The **--dst** argument is used with **--move**, **--rename** and
  **--clone** to specify destination node name (e.g., rule10).

 ``--move`` *where*
  Perform the ``action=move`` device configuration API request with the
  **xpath**, **where** and **dst** arguments.

  This moves the location of an existing node in the configuration
  specified by **xpath**.  *where* is used to specify the location of
  the node and can be *after*, *before*, *bottom* or *top*.
  **--dst** is used to specify the relative destination node name when
  *where* is *after* or *before*.

  **--move** is most frequently used to reorder rules (security,
  nat, qos, etc.) within the rulebase, however can be used to
  move other nodes in the configuration.

 ``--rename``
  Perform the ``action=rename`` device configuration API request with the
  **xpath** and **newname** arguments.

  This renames an existing node in the configuration specified by
  **xpath**.  **--dst** is used to specify the new name for the node.

 ``--clone``
  Perform the ``action=clone`` device configuration API request with the
  **xpath**, **from** and **newname** arguments.

  This clones (copies) an existing node in the configuration specified by
  **xpath**.  **--src** is used to specify the source XPath and **--dst**
  is used to specify the new name for the cloned node.

 ``--vsys`` *vsys*
  Specify optional **vsys** for dynamic update (**-U**), partial vsys
  commit (**--partial** vsys), commit-all (**-A**) and operational
  commands (**-o**).

  *vsys* can be specified using name (**vsys2**) or number (**2**).

  Multiple virtual systems can be specified by using multiple
  **--vsys** options or separating each *vsys* with comma (,).

 ``-l`` *api_username:api_password*
  Specify the **api_username** and **api_password** which are used
  to generate the **api_key** used in API requests.

 ``-h`` *hostname*
  Specify the **hostname** which is used to generate the URI
  for API requests.

 ``-P`` *port*
  Specify the **port** number used in the URL.  This can be used to
  perform port forwarding using for example ssh(1).

 ``--serial`` *number*
  Specify the serial number used for Panorama to device redirection.
  This sets the **target** argument to the serial number specified in
  device configuration, commit configuration, key generation, dynamic
  object update and operational command API requests.

  When an API request is made on Panorama and the serial number is
  specified, Panorama will redirect the request to the managed device
  with the serial number.

 ``--group`` *name*
  Specify the device group name used for Panorama commit-all (**-A**).

 ``--merge``
  Specify the **merge-with-candidate-cfg** option for Panorama commit-all
  (**-A**).

 ``--nlogs`` *num*
  Specify the number of logs to retrieve for the **--log** option.

  The default is 20 and the maximum is 5000.

  **pan.xapi** currently loads the entire XML document into memory
  using the **ElementTree** module.  A large number of log entries can
  cause a memory exception which may not be possible to catch.  If you
  see exceptions when using a large **--nlog** value try reducing it.

 ``--skip`` *num*
  Specify the number of logs to skip for the **--log** option.  This
  can be used to retieve log entries in batches by skipping previously
  retrieved logs.

  The default is 0.

 ``--filter`` *filter*
  Specify the log query selection filter for the **--log** option.
  This is a set of log filter expressions as can be specified in the
  Monitor tab in the Web UI.

 ``-K`` *api_key*
  Specify the **api_key** used in API requests.  This is not required to
  perform API requests if the **api_username** and **api_password** are
  provided using the **-l** argument or a .panrc file.

 ``-x``
  Print XML response to *stdout*.

 ``-p``
  Print XML response in Python to *stdout*.

 ``-j``
  Print XML response in JSON to *stdout*.

 ``-r``
  Print result content when printing the response (removes outer
  <response><result> elements).  If a <result> element is not present
  this prints the entire response.  This option applies to **-x**,
  **-p** and **-j** response output.

 ``-X``
  Convert a CLI-style *cmd* argument to XML.  This works by converting all
  unquoted arguments in *cmd* to start and end elements and treating
  double quoted arguments as text after removing the quotes.  For
  example:

  - show system info

    * <show><system><info></info></system></show>

  - show interface "ethernet1/1"

    * <show><interface>ethernet1/1</interface></show>

 ``--ls``
  Print formatted PCAP listing to *stdout*.  For use with **--export**.

 ``--recursive``
  Export recursively.  This copies the PCAP files to the YYYYMMDD
  directory in their path, and creates the directory if needed.

 ``-H``
  Use the *http* URL scheme for API requests.  The default is to use
  the *https* URL scheme.

 ``-G``
  Use the HTTP *GET* method for API requests.  The default is to use
  the HTTP *POST* method with Content-Type
  application/x-www-form-urlencoded.

 ``-D``
  Enable debugging.  May be specified multiple times up to 3
  to increase debugging output.

 ``-t`` *tag*
  Specify tagname for .panrc.

 ``-T`` *seconds*
  Specify the ``timeout`` value for urlopen().

 ``--cafile`` *path*
  Specify the ``cafile`` value for urlopen().  ``cafile`` is a file
  containing CA certificates to be used for SSL server certificate
  verification. By default the SSL server certificate is not verified.
  ``--cafile`` is only supported in Python version 3.2 and greater.

 ``--capath`` *path*
  Specify the ``capath`` value for urlopen().  ``capath`` is a
  directory of hashed certificate files to be used for SSL server
  certificate verification. By default the SSL server certificate is
  not verified.
  ``--capath`` is only supported in Python version 3.2 and greater.

 ``--version``
  Display version.

 ``--help``
  Display command options.

 ``xpath``
  XPath for request.  **xpath** can be a string, a path to a file
  containing the XPath, or the value **-** to specify the XPath
  is on *stdin*.

FILES
=====

 ``.panrc``
  .panrc file.  See PanXapi documentation for .panrc format.

EXIT STATUS
===========

 **panxapi.py** exits with 0 on success and 1 if an error occurs.

EXAMPLES
========

 Generate an API key.
 ::

  $ panxapi.py -l admin:admin -h 172.29.9.253 -k
  keygen: success
  API key:  "C2M1P2h1tDEz8zF3SwhF2dWC1gzzhnE1qU39EmHtGZM="

 Create a .panrc file with the API key.
 ::

  $ echo 'hostname=172.29.9.253' >.panrc
  $ echo 'api_key=C2M1P2h1tDEz8zF3SwhF2dWC1gzzhnE1qU39EmHtGZM=' >>.panrc

 Retrieve the *active* configuration and write it to a file.
 ::

  $ panxapi.py -sxr >active.xml
  show: success

 Retrieve and display a security rule from the *active* configuration.
 ::

  $ xpath="/config/devices/entry/vsys/entry/rulebase/security/rules/entry[@name='rule7']"
  $ panxapi.py -sxr $xpath | head
  show: success
  <entry name="rule7">
    <option>
      <disable-server-response-inspection>no</disable-server-response-inspection>
    </option>
    <from>
      <member>trust</member>
    </from>
    <to>
      <member>dmz</member>
    </to>

 Edit the *application* of a security rule.
 ::

  $ echo '<application><member>rsync</member></application>' >app.xml
  $ panxapi.py -e app.xml $xpath/application
  edit: success [code="20"]: command succeeded

 Retrieve and display modified *application* from the *candidate* configuration.
 ::

  $ panxapi.py -gxr $xpath/application
  get: success [code="19"]
  <application admin="admin" time="2013/03/02 15:17:31"><member admin="admin" time="2013/03/02 15:17:31">rsync</member></application>

 Commit candidate configuration.
 ::

  $ panxapi.py -C ''
  commit: success [code="19"]: Commit job enqueued with jobid 912

 Show job id.
 ::

  $ panxapi.py -Xjro 'show jobs id "912"'
  op: success
  {
    "job": {
      "details": null, 
      "id": "912", 
      "progress": "99", 
      "result": "PEND", 
      "status": "ACT", 
      "stoppable": "yes", 
      "tenq": "2013/03/02 15:21:26", 
      "tfin": "Still Active", 
      "type": "Commit", 
      "warnings": null
    }
  }

 Save security rule.
 ::

  $ panxapi.py -sxr $xpath >rule.xml
  show: success

 Delete security rule.
 ::

  $ panxapi.py -d $xpath
  delete: success [code="20"]: command succeeded

 Commit Policy and Object configuration.
 ::

  $ panxapi.py --partial device-and-network-excluded
  commit: success [code="19"]: Commit job enqueued with jobid 914

 Add security rule.
 ::

  $ xpath2="/config/devices/entry/vsys/entry/rulebase/security/rules"
  $ panxapi.py -S rule.xml $xpath2
  set: success [code="20"]: command succeeded

 Move security rule.
 ::

  $ panxapi.py --move top $xpath
  move: success [code="20"]: command succeeded

 Rename security rule.
 ::

  $ panxapi.py --rename --dst rule7-b $xpath
  rename: success [code="20"]: command succeeded

 Retrieve WildFire logs matching filter.
 ::

  $ panxapi.py --log wildfire -xr --filter '(misc eq wajam_install.exe)'
  log: success [code="19"]
  <job>
      <tenq>11:29:24</tenq>
      <tdeq>11:29:25</tdeq>
      <tlast>11:29:26</tlast>
      <status>FIN</status>
      <id>89</id>
    </job>
    <log>
      <logs count="1" progress="100">
        <entry logid="5910273572261068816">
  [...]

 Retrieve report using the **--ad-hoc** option.
 ::

  $ panxapi.py -x --modify --ad-hoc 'type=report&reporttype=dynamic&reportname=acc-summary'
  ad_hoc: success
  <response status="success"><report logtype="appstat" reportname="acc-summary">
      <result end="2013/09/13 23:59:59" end-epoch="1379141999" generated-at="2013/09/14 10:34:31" generated-at-epoch="1379180071" logtype="appstat" name="acc summary" range="Friday, September 13, 2013" start="2013/09/13 00:00:00" start-epoch="1379055600">
        <entry>
          <name>paloalto-wildfire-cloud</name>
          <risk-of-name>1</risk-of-name>
          <nbytes>9005951</nbytes>
          <nthreats>0</nthreats>
          <nsess>723</nsess>
          <npkts>20924</npkts>
        </entry>
  [...]


SEE ALSO
========

 pan.xapi, panconf.py

AUTHORS
=======

 Kevin Steves <kevin.steves@pobox.com>
