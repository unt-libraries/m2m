# m2m
m2m is a python package and command line tool to assist in converting csv documents into UNTL metadata records. m2m stands for "metadata to metadata".

```python
>>> from m2m import m2m
>>> record = m2m.MetadataRecord("mphillips")
>>> record.mapping("basic", "title", "Pawn of Prophecy", qualifier="officialtitle")
>>> record.mapping("agent", "creator", "Eddings, David", qualifier="aut", agent_type="per")
>>> record.mapping("basic", "date", "1982", qualifier="creation")
>>> print(record)
<?xml version="1.0" encoding="UTF-8"?>
<metadata>
  <title qualifier="officialtitle">Pawn of Prophecy</title>
  <creator qualifier="aut">
    <type>per</type>
    <name>Eddings, David</name>
  </creator>
  <date qualifier="creation">1982</date>
  <meta qualifier="metadataCreator">mphillips</meta>
</metadata>
```

Requirements
------------

* Python 3.6 - 3.8

Installation
--------------

This application can be installed by following the steps below:

    $ git clone https://github.com/unt-libraries/m2m.git

    $ cd m2m

    $ pip install .

This application can be run using following command with example files.

    $ python m2m/m2m.py -m tests/data/test_2_untl.py tests/data/test.csv

Testing
-------

Install tox on your system:

    $ pip install tox

To run the development tests, use the following command:

    $ tox

License
-------

See LICENSE.txt

Acknowledgements
----------------

_m2m_ was developed at the UNT Libraries.

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
