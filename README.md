# m2m
m2m is a python package and command line tool to assist in converting csv documents into UNTL metadata records. m2m stands for "metadata to metadata".

```python
>>> from m2m import m2m
>>> record = m2m.MetadataRecord("mphillips")
>>> record.map("basic", "title", "Pawn of Prophecy", qualifier="officialtitle")
>>> record.map("agent", "creator", "Eddings, David", qualifier="aut", agent_type="per")
>>> record.map("basic", "date", "1982", qualifier="creation")
>>> print record
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

# License

See LICENSE.txt.

Acknowledgements
----------------

_m2m_ was developed at the UNT Libraries.

If you have questions about the project feel free to contact Mark Phillips at mark.phillips@unt.edu.
