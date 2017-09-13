..
 Copyright (c) 2017 Palo Alto Networks, Inc. <techbizdev@paloaltonetworks.com>

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

===========
panafapi.py
===========

-------------------------------------------
command line interface to the AutoFocus API
-------------------------------------------

NAME
====

 panafapi.py - command line interface to the AutoFocus API

SYNOPSIS
========
::

 panafapi.py [options]
    --sessions            search AutoFocus sessions
    -A                    get aggregate of sessions
    -H                    get histogram of sessions
    --session id          get AutoFocus session
    --samples             search AutoFocus samples
    --sample-analysis     get AutoFocus sample analysis report
    --top-tags            search AutoFocus top tags
    --tags                search AutoFocus tags
    --tag name            get AutoFocus tag
    --export              export AutoFocus list
    -r json               JSON API request (multiple -r's allowed)
    -n num                request num results
    --scope scope         search scope
    --hash hash           sample hash
    --terminal            get only final search result
    -t tag                .panrc tagname
    -K api_key            AutoFocus API key
    -V api_version        AutoFocus API version (default v1.0)
    -h hostname           AutoFocus hostname
    -p                    print response in Python to stdout
    -j                    print response in JSON to stdout
    -D                    enable debug (multiple up to -DDD)
    --ssl opt             SSL verify option: verify|noverify
    -T seconds            HTTP connect timeout
    --version             display version
    --help                display usage

DESCRIPTION
===========

 **panafapi.py** is used to perform AutoFocus API requests.
 It uses the PanAFapi class from the **pan.afapi** module to
 execute API requests.

 The options are:

 ``--sessions``
  Search AutoFocus sessions using the ``/sessions/search/``
  and ``/sessions/results/`` API requests.

 ``-A``
  Search AutoFocus sessions using the ``/sessions/aggregate/search/``
  and ``/sessions/aggregate/results/`` API requests.

 ``-H``
  Search AutoFocus sessions using the ``/sessions/histogram/search/``
  and ``/sessions/histogram/search/`` API requests.

 ``--session`` *id*
  Get details for AutoFocus session using the ``/session/`` API
  request.

 ``--samples``
  Search AutoFocus (WildFire) samples using the ``/samples/search/``
  and ``/samples/results/`` API requests.

 ``--sample-analysis``
  Get details for a sample's WildFire analysis using the
  ``/sample/{id}/analysis`` API request.

 ``--top-tags``
  Search AutoFocus top tags data using the ``/top-tags/search/``
  and ``/top-tags/results/`` API requests.  This data corresponds to
  the *Top Tags* data in the AutoFocus portal dashboard and search
  statistics.

 ``--tags``
  Search AutoFocus tags using the ``/tags/`` API request.

 ``--tag`` *name*
  Get details for an AutoFocus tag using the ``/tag/``
  API request.

 ``--export``
  Export a list of saved AutoFocus artifacts using the
  ``/export/`` API request.

 ``-r`` *json*
  JSON object to use in the body of the API request.

  Multiple ``-r`` options are allowed.

  *json* can be a JSON string, a path to a file containing JSON,
  or the value **-** to specify that JSON is on *stdin*.

 ``-n`` *num*
  Specify number of results for the request.

  This is a convenience option and sets the ``pageSize`` string for
  ``--tags`` and the ``size`` string for the search options to *num*
  in the JSON body of the request.

 ``--scope`` *scope*
  Specify the scope for the request.

  This is a convenience option and sets the ``scope`` string for
  ``--tags`` and the search options to *scope* in the JSON body of the
  request.

 ``--hash`` *hash*
  Specify the hash for the request.

  This sets the ``sampleid`` argument for the ``--sample-analysis``
  (PanAFapi ``sample_analysis()`` method) request.  The ``sampleid``
  is the SHA256 hash of the sample.

 ``--terminal``
  Set the ``terminal`` argument for the ``*_search_results()`` PanAFapi
  methods to ``True``.

  This specifies that only the terminal (complete) search result
  should be returned.

  By default intermediate (incomplete) search results are returned
  (the ``terminal`` argument is set to ``False``).

 ``-t`` *tag*
  Specify tagname for .panrc file.

 ``-K`` *api_key*
  Specify the API key for the request.

 ``-V`` *api_version*
  Specify the API version for the request.

  API version is a string in the form v\ **major**.\ **minor** or
  **major**.\ **minor** (e.g., *v1.0*).  The API version is used to determine
  the PanAFapi class implementation to use.

  The default API version can be determined by running ``panafapi.py -D``.

 ``-h`` *hostname*
  URI hostname used in API requests.    This can also be
  specified in a .panrc file using the ``hostname`` *varname*.

  The default is ``autofocus.paloaltonetworks.com``.

 ``-p``
  Print JSON response in Python to *stdout*.

 ``-j``
  Print JSON response to *stdout*.

 ``-D``
  Enable debugging.  May be specified multiple times up to 3
  to increase debugging output.

 ``--ssl`` *opt*
  Specify the type of SSL server certificate verification to be
  performed.

  ``verify``
   Perform SSL server certificate verification.  This is the default.

  ``noverify``
   Disable SSL server certificate verification.

 ``-T`` *seconds*
  The HTTP connect ``timeout`` in seconds.

 ``--version``
  Display version.

 ``--help``
  Display command options.

 The following describes the options used to perform each AutoFocus
 API request:

 ===================   ===================================  =================
 Options               PanAFapi Method                      API Resource URIs
 ===================   ===================================  =================
 --sessions            sessions_search_results()            | /sessions/search/
                                                            | /sessions/results/
 --sessions -A         sessions_aggregate_search_results()  | /sessions/aggregate/search/
                                                            | /sessions/aggregate/results/
 --sessions -H         sessions_histogram_search_results()  | /sessions/histogram/search/
                                                            | /sessions/histogram/results/
 --session id          session()                            | /session/
 --samples             samples_search_results()             | /samples/search/
                                                            | /samples/results/
 --sample-analysis     sample_analysis()                    | /sample/{id}/analysis
 --top-tags            top_tags_search_results()            | /top-tags/search/
                                                            | /top-tags/results/
 --tags                tags()                               | /tags/
 --tag name            tag()                                | /tag/
 --export              export()                             | /export/
 ===================   ===================================  =================

FILES
=====

 ``.panrc``
  .panrc file.

EXIT STATUS
===========

 **panafapi.py** exits with 0 on success and 1 if an error occurs.

EXAMPLES
========

 .. Note:: Examples may use the **jp.py** program from
	   `JMESPath <http://jmespath.org/>`_.

 Add AutoFocus API key with tagname *autofocus* to .panrc file.

 First `Get Your API Key
 <https://www.paloaltonetworks.com/documentation/autofocus/autofocus/autofocus_api/get-started-with-the-autofocus-api/get-your-api-key>`_.
 ::

  $ KEY=e3222942-2080-11e7-b1c7-03f23b1b6cb4
  $ echo "api_key%autofocus=$KEY" >>.panrc

 Verify API key.
 ::

  $ panafapi.py -t autofocus --tags
  tags: 200 OK tags=50 total_count=1394

 Get 10 tags using ``-n 10``.
 ::

  $ panafapi.py -t autofocus --tags -j -n 10 | jp.py 'tags[].public_tag_name'
  tags: 200 OK tags=10 total_count=1394
  [
      "Commodity.180Solutions", 
      "Commodity.1stBrowser", 
      "Commodity.360Root", 
      "Unit42.4H", 
      "Unit42.777Ransomware", 
      "Commodity.7ev3n", 
      "Unit42.7ev3nHONEST", 
      "Unit42.7h9rRansomware", 
      "Unit42.9002", 
      "Unit42.AbaddonPOS"
  ]

 Get tag details.
 ::

  $ panafapi.py -t autofocus --tag Unit42.777Ransomware -j | jp.py tag
  tag: 200 OK
  {
      "count": 9, 
      "lasthit": "2016-05-28 05:50:27", 
      "tag_class": "malware_family", 
      "description": "777 ransomware appears to have been around since September 2015,but several new samples were discovered during mid-2016. This ransomware will encrypt files and append the .777 extension to them. There is a public decryptor that will automatically decrypt any files that end with the .777 extension.", 
      "tag_definition_status_id": 1, 
      "up_votes": 1, 
      "created_at": "2017-02-14 10:59:23", 
      "tag_class_id": 3, 
      "tag_definition_scope_id": 4, 
      "tag_definition_scope": "unit42", 
      "comments": [], 
      "updated_at": "2017-02-14 10:59:23", 
      "tag_definition_status": "enabled", 
      "source": "Unit 42", 
      "tag_name": "777Ransomware", 
      "public_tag_name": "Unit42.777Ransomware", 
      "refs": "[{\"source\":\"BleepingComputer\",\"title\":\"Emsisoft Releases Decryptors for the Xorist and 777 Ransomware\",\"url\":\"https://www.bleepingcomputer.com/news/security/emsisoft-releases-decryptors-for-the-xorist-and-777-ransomware/\",\"created\":\"2017-01-30T12:50:49\"}]", 
      "customer_name": "Palo Alto Networks Unit42"
  }

 Search private samples for malware and save results.
 ::

  $ cat q-malware.json
  {
      "query": {
          "children": [
              {
                  "field": "sample.malware",
                  "operator": "is",
                  "value": 1
              }
          ],
          "operator": "all"
      }
  }

  $ panafapi.py -t autofocus --samples -r q-malware.json --scope private -n 100 -j > malware-private.json
  samples_search: 200 OK 339 0%
  samples_results: 200 OK 556 0% hits=0 total=0 time=0:00:00.591
  samples_results: 200 OK 10% hits=8 total=8 time=0:00:03.636
  samples_results: 200 OK 18% hits=9 total=9 time=0:00:04.658
  samples_results: 200 OK 35% hits=29 total=29 time=0:00:07.145
  samples_results: 200 OK 41% hits=74 total=74 time=0:00:07.966
  samples_results: 200 OK 73% hits=89 total=89 time=0:00:10.715
  samples_results: 200 OK 93% hits=91 total=91 time=0:00:11.592
  samples_results: 200 OK 100% hits=94 total=94 time=0:00:12.566 "complete"

 Display some results.
 ::

  $ jp.py -f malware-private.json 'hits[0:2]._source.[create_date,filetype,tag]'
  [
      [
          "2017-03-30T13:14:29", 
          "PE", 
          [
              "Commodity.WildFireTest"
          ]
      ], 
      [
          "2017-03-30T12:24:30", 
          "PE", 
          [
              "Commodity.WildFireTest"
          ]
      ]
  ]

 Get sample analaysis details.
 ::

  $ jp.py -f malware-private.json 'hits[0]._source.[sha256]'
  [
      "3886f96be7f889f38b88e93b12188eed6974ace9223334e7c0aa366a3cb61200"
  ]

  $ HASH=3886f96be7f889f38b88e93b12188eed6974ace9223334e7c0aa366a3cb61200

  $ panafapi.py -t autofocus --sample-analysis --hash $HASH -j > $HASH.json
  sample-analysis: 200 OK

 Display report connection section.
 ::

  $ jp.py -f $HASH.json 'connection'
  {
      "win7": [
          {
              "line": "unknown , udp , 23.96.94.144:123 , US", 
              "b": 32901349, 
              "m": 6590112, 
              "g": 359377
          }, 
          {
              "line": "unknown , udp , 224.0.0.252:5355 , -", 
              "b": 20249526, 
              "m": 7999437, 
              "g": 371806
          }
      ], 
      "winxp": [
          {
              "line": "unknown , udp , 23.96.94.144:123 , US", 
              "b": 32901349, 
              "m": 6590112, 
              "g": 359377
          }
      ]
  }

SEE ALSO
========

 pan.afapi

 AutoFocus API Reference Guide
  https://www.paloaltonetworks.com/documentation/autofocus/autofocus/autofocus_api

 View API Request for a Search as **panafapi.py** command line
  https://www.paloaltonetworks.com/documentation/autofocus/autofocus/new-feature-guide/new-features-march-2016/api-request-for-a-search

 AutoFocus Administrator's Guide
  https://www.paloaltonetworks.com/documentation/autofocus/autofocus/autofocus_admin_guide

AUTHORS
=======

 Palo Alto Networks, Inc. <techbizdev@paloaltonetworks.com>
