import unittest
from m2m import m2m

class MetadataRecordTests(unittest.TestCase):

    def testMetadataRecordSetup(self):
        # test that the creation of a record creates a MetadataRecord object.

        self.record = m2m.MetadataRecord("mphillips")
        self.assertIsInstance(self.record, m2m.MetadataRecord)

    def testNoneElementValueEqualsNone(self):
        # if element value is None then it should return None.

        self.record = m2m.MetadataRecord("mphillips")
        self.assertEquals(self.record.map("basic", "title", None), None)

    def testEmptyElementValueEqualsNone(self):
        # if element value is empty for non-required elements 
        # then map should return None.

        self.record = m2m.MetadataRecord("mphillips")
        self.assertEquals(self.record.map("basic", "title", "", required=False), None)

    def testSetBaseDirectory(self):

        self.record = m2m.MetadataRecord("mphillips")
        self.record.setBaseDirectory("out")
        self.assertEquals(self.record.baseDirectory, "out")

    def testSetFolderName(self):

        self.record = m2m.MetadataRecord("mphillips")
        self.record.setFolderName("folder")
        self.assertEquals(self.record.foldername, "folder")

    def testElementNotInFieldType(self):

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            self.record = m2m.MetadataRecord("mphillips")
            self.record.map("basic", "author", "text")

        the_exception = cm.exception
        self.assertEqual(the_exception.value, 'Element named "author" not in fieldTypes')

    def testUnsupportedMappingFunctionType(self):

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            self.record = m2m.MetadataRecord("mphillips")
            self.record.map("simple", "title", "text")

        the_exception = cm.exception
        self.assertEqual(the_exception.value, 'Unsupported mapping function type, simple')

    def testMissingRequiredMetadataValue(self):

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            self.record = m2m.MetadataRecord("mphillips")
            self.record.map("basic", "title", "")

        the_exception = cm.exception
        self.assertEqual(the_exception.value, 'Value required for element named "title"')

    def testIncorrectElementTypeForValidElement(self):

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            self.record = m2m.MetadataRecord("mphillips")
            self.record.map("agent", "title", "test")

        the_exception = cm.exception
        self.assertEqual(the_exception.value, "Element 'title' should be of basic type, but you are attempting to add it as 'agent' type.")

    def testSplitFunctionOfMap(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "m|f", split="|")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title>m</title>\n  <title>f</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testEmptySplitFunctionOfMap(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "m|f", split="")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title>m|f</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapUnqualifiedBasicNoOptions(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "test_title")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title>test_title</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualifiedBasicNoOptions(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "test_title", qualifier="officialtitle")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title qualifier="officialtitle">test_title</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapEmptyQualifiedBasicNoOptions(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "test_title", qualifier="")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title>test_title</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualiiedBasicWithFunction(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("basic", "title", "test_title", qualifier="officialtitle", function=(lambda x: x.upper()))

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <title qualifier="officialtitle">TEST_TITLE</title>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapUnqualifiedAgentNoOptions(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("agent", "creator", "Phillips, Mark")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <creator>\n    <name>Phillips, Mark</name>\n  </creator>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualifiedAgentNoOptions(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("agent", "creator", "Phillips, Mark", qualifier="aut")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <creator qualifier="aut">\n    <name>Phillips, Mark</name>\n  </creator>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualifiedAgentInfoOnly(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("agent", "creator", "Phillips, Mark", 
                        qualifier="aut", info="First Publication")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <creator qualifier="aut">\n    <info>First Publication</info>\n    <name>Phillips, Mark</name>\n  </creator>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualifiedAgentInfoAndAgentType(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("agent", "creator", "Phillips, Mark", 
                        qualifier="aut",
                        info="First Publication",
                        agent_type="per")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <creator qualifier="aut">\n    <info>First Publication</info>\n    <type>per</type>\n    <name>Phillips, Mark</name>\n  </creator>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testMapQualifiedAgentWithLocation(self):
        self.record = m2m.MetadataRecord("mphillips")
        self.record.map("agent", "publisher", "UNT Libraries", 
                        location="Denton, Texas")

        self.assertEquals(self.record.__str__(), '<?xml version="1.0" encoding="UTF-8"?>\n<metadata>\n  <publisher>\n    <name>UNT Libraries</name>\n    <location>Denton, Texas</location>\n  </publisher>\n  <meta qualifier="metadataCreator">mphillips</meta>\n</metadata>\n')

    def testIncorrectUseOfLocationInAgentThatIsNotPublisher(self):

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            self.record = m2m.MetadataRecord("mphillips")
            self.record.map("agent", "creator", "Phillips, Mark", 
                        location="aut")

        the_exception = cm.exception
        self.assertEqual(the_exception.value, "location can only be used on publisher element")

def suite():
    test_suite = unittest.makeSuite(MetadataRecordTests, 'test')
    return test_suite

if __name__ == "__main__":
    unittest.main()