Python SPDX Parser Library.
===========================

Official repository: http://git.spdx.org/?p=spdx-tools-python.git

GitHub mirror: https://github.com/ah450/sdpx-tools-python

This library provides an implementation of a tag/value and RDF SPDX parser in python.

Expected Features:
==================
* API for creating and manipulating SPDX documents.
* Parse Tag/Value format SPDX files
* Parse RDF format SPDX files
* Create Tag/Value files.
* Create RDF files.

Current Status:
===============
* RDF Parser unimplemented.
* Tag/Value Parser missing License parsing rules.
* Writers unimplemented.


How to use:
===========
Sample Tag/Value parsing Usage:
```Python
    from spdx.parsers.tagvalue import Parser
    from spdx.parsers.tagvaluebuilders import Builder
    from spdx.parsers.loggers import StandardLogger
    p = Parser(Builder(), StandardLogger())
    p.build()
    # data is a string containing the SPDX file.
    document, error = p.parse(data)

```

The file `parse_tv_ex.py` has a working example
try running `python parse_tv_ex.py 'Examples/SPDXSimpleTag.tag' `

Installation:
=============
Clone the repository and run `python setup.py install`
on windows the command should be `setup.py install`

How to run tests:
=================
From the project root directory.

run: `nosetests`

Dependencies:
=============
nose : https://pypi.python.org/pypi/nose/1.3.3

PLY : https://pypi.python.org/pypi/ply/3.4
