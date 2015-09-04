import unittest

from lxml import etree
from lxml import objectify

from m2m import m2m


def xml_to_pretty_string(xml):
    objectify.deannotate(xml, xsi_nil=True)
    etree.cleanup_namespaces(xml)

    s = etree.tostring(xml, pretty_print=True)
    return '<?xml version="1.0" encoding="UTF-8"?>\n' + s


class MetadataRecordTests(unittest.TestCase):

    def setUp(self):
        xml = """<?xml version="1.0" encoding="UTF-8"?>
            <metadata>
                <title />
                <meta qualifier='metadataCreator'></meta>
            </metadata>
        """
        self.tree = objectify.fromstring(xml)

        agent_xml = """<?xml version="1.0" encoding="UTF-8"?>
            <metadata>
                <creator>
                    <info />
                    <type />
                    <name />
                </creator>
                <meta />
            </metadata>
        """
        self.agent_tree = objectify.fromstring(agent_xml)

        pub_xml = """<?xml version="1.0" encoding="UTF-8"?>
            <metadata>
                <publisher>
                    <name />
                    <location />
                </publisher>
                <meta />
            </metadata>
        """
        self.pub_tree = objectify.fromstring(pub_xml)

    def test_metadata_record_setup(self):
        # test that the creation of a record creates a MetadataRecord object.

        record = m2m.MetadataRecord('mphillips')
        self.assertIsInstance(record, m2m.MetadataRecord)

    def test_metadata_record_setup_with_date(self):

        record = m2m.MetadataRecord('mphillips', addDate=True)
        self.assertIsInstance(record, m2m.MetadataRecord)

    def test_none_element_value_equals_none(self):
        # if element value is None then it should return None.

        record = m2m.MetadataRecord('mphillips')
        self.assertEquals(record.map('basic', 'title', None), None)

    def test_empty_element_value_equals_none(self):
        # if element value is empty for non-required elements
        # then map should return None.

        record = m2m.MetadataRecord('mphillips')
        self.assertEquals(record.map('basic', 'title', '', required=False),
                          None)

    def test_set_base_directory(self):

        record = m2m.MetadataRecord('mphillips')
        record.setBaseDirectory('out')
        self.assertEquals(record.baseDirectory, 'out')

    def test_set_folder_name(self):

        record = m2m.MetadataRecord('mphillips')
        record.setFolderName('folder')
        self.assertEquals(record.foldername, 'folder')

    def test_element_not_in_field_type(self):

        record = m2m.MetadataRecord('mphillips')

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            record.map('basic', 'author', 'text')

        expected_error = 'Element named "author" not in fieldTypes'
        self.assertEqual(str(cm.exception), expected_error)

    def test_unsupported_mapping_function_type(self):

        record = m2m.MetadataRecord('mphillips')

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            record.map('simple', 'title', 'text')

        expected_error = 'Unsupported mapping function type, simple'
        self.assertEqual(str(cm.exception), expected_error)

    def test_missing_required_metadata_value(self):

        record = m2m.MetadataRecord('mphillips')

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            record.map('basic', 'title', '')

        expected_error = 'Value required for element named "title"'
        self.assertEqual(str(cm.exception), expected_error)

    def test_incorrect_element_type_for_valid_element(self):

        record = m2m.MetadataRecord('mphillips')

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            record.map('agent', 'title', 'test')

        expected_error = 'Element "title" should be of basic type, but you' \
                         ' are attempting to add it as "agent" type.'
        self.assertEqual(str(cm.exception), expected_error)

    def test_split_function_of_map(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'm|f', split='|')

        self.tree.title = ['m', 'f']
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_empty_split_function_of_map(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'm|f', split='')

        self.tree.title = 'm|f'
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_map_unqualified_basic_no_options(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'test_title')

        self.tree.title = 'test_title'
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_map_qualified_basic_no_options(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'test_title', qualifier='officialtitle')

        self.tree.title = 'test_title'
        self.tree.title.set('qualifier', 'officialtitle')
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_map_empty_qualified_basic_no_options(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'test_title', qualifier='')

        self.tree.title = 'test_title'
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_map_qualified_basic_with_function(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('basic', 'title', 'test_title',
                   qualifier='officialtitle',
                   function=(lambda x: x.upper())
                   )

        self.tree.title = 'TEST_TITLE'
        self.tree.title.set('qualifier', 'officialtitle')
        self.tree.meta = 'mphillips'
        self.tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.tree))

    def test_map_unqualified_agent_no_options(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('agent', 'creator', 'Phillips, Mark')

        self.agent_tree.creator.name = 'Phillips, Mark'
        del self.agent_tree.creator.info
        del self.agent_tree.creator.type
        self.agent_tree.meta = 'mphillips'
        self.agent_tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.agent_tree))

    def test_map_qualified_agent_no_options(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('agent', 'creator', 'Phillips, Mark', qualifier='aut')

        self.agent_tree.creator.name = 'Phillips, Mark'
        del self.agent_tree.creator.info
        del self.agent_tree.creator.type
        self.agent_tree.creator.set('qualifier', 'aut')
        self.agent_tree.meta = 'mphillips'
        self.agent_tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.agent_tree))

    def test_map_qualified_agent_info_only(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('agent', 'creator', 'Phillips, Mark',
                   qualifier='aut', info='First Publication')

        self.agent_tree.creator.info = 'First Publication'
        self.agent_tree.creator.name = 'Phillips, Mark'
        del self.agent_tree.creator.type
        self.agent_tree.creator.set('qualifier', 'aut')
        self.agent_tree.meta = 'mphillips'
        self.agent_tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.agent_tree))

    def test_map_qualified_agent_info_and_agent_type(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('agent', 'creator', 'Phillips, Mark',
                   qualifier='aut',
                   info='First Publication',
                   agent_type='per')

        self.agent_tree.creator.info = 'First Publication'
        self.agent_tree.creator.name = 'Phillips, Mark'
        self.agent_tree.creator.type = 'per'
        self.agent_tree.creator.set('qualifier', 'aut')
        self.agent_tree.meta = 'mphillips'
        self.agent_tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.agent_tree))

    def test_map_qualified_agent_with_location(self):
        record = m2m.MetadataRecord('mphillips')
        record.map('agent', 'publisher', 'UNT Libraries',
                   location='Denton, Texas')

        self.pub_tree.publisher.name = 'UNT Libraries'
        self.pub_tree.publisher.location = 'Denton, Texas'
        self.pub_tree.meta = 'mphillips'
        self.pub_tree.meta.set('qualifier', 'metadataCreator')

        self.assertEqual(str(record), xml_to_pretty_string(self.pub_tree))

    def test_incorrect_use_of_location_in_agent_that_is_not_publisher(self):

        record = m2m.MetadataRecord('mphillips')

        with self.assertRaises(m2m.MetadataConverterException) as cm:
            record.map('agent', 'creator', 'Phillips, Mark',
                       location='aut')

        expected_error = 'location can only be used on publisher element'
        self.assertEqual(str(cm.exception), expected_error)


def suite():
    test_suite = unittest.makeSuite(MetadataRecordTests, 'test')
    return test_suite

if __name__ == '__main__':
    unittest.main()
