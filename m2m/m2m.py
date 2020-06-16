import csv
import time
import os
import sys
import json
from argparse import ArgumentParser

from pyuntl.untl_structure import PYUNTL_DISPATCH
from pyuntl.untldoc import untlpydict2xmlstring, untlpy2dict


fieldTypes = {
    'title': 'basic',
    'creator': 'agent',
    'contributor': 'agent',
    'publisher': 'agent',
    'date': 'basic',
    'language': 'basic',
    'description': 'basic',
    'subject': 'basic',
    'coverage': 'basic',
    'source': 'basic',
    'relation': 'basic',
    'collection': 'basic',
    'institution': 'basic',
    'rights': 'basic',
    'resourceType': 'basic',
    'format': 'basic',
    'identifier': 'basic',
    'note': 'basic',
    'degree': 'basic',
    'meta': 'basic',
    'primarySource': 'basic',
    'citation': 'basic',
    }


def CSVToDict(csvFileName):
    readerDict = csv.DictReader(open(csvFileName))
    return list(readerDict)


class MetadataConverterException(Exception):
    """Base class for exceptions in this package"""
    pass


class MetadataRecord(object):

    def __init__(self, metadataCreator, addDate=False):
        # create our initial tree
        self.root_element = PYUNTL_DISPATCH['metadata']()
        self.mapping('basic', 'meta', metadataCreator, qualifier='metadataCreator')
        if addDate is True:
            self.mapping('basic', 'meta', '%s' % time.strftime(
                     '%Y-%m-%d, %H:%M:%S'), qualifier='metadataCreationDate')

    def __bytes__(self):
        return untlpydict2xmlstring(untlpy2dict(self.root_element))

    def __str__(self):
        return self.__bytes__().decode()

    def setBaseDirectory(self, BaseDirectory):
        self.baseDirectory = BaseDirectory

    def setFolderName(self, FolderName):
        self.foldername = FolderName

    def mapping(self, elementType, elementName, elementValue, qualifier=None,
                required=True, info='', location='', agent_type='', split='',
                function=None):
        """
        Mapping Function
        """

        if elementType not in ('basic', 'agent'):
            raise MetadataConverterException(
                'Unsupported mapping function type, %s' % elementType)

        # strip whitespace
        if elementValue is None:
            return None

        strippedValue = elementValue.strip()

        # test if the value is present if required
        if required is True:
            if strippedValue == '':
                raise MetadataConverterException(
                    'Value required for element named "%s"' % elementName)

        # if there isn't value don't continue
        if strippedValue == '':
            return None

        if elementName not in fieldTypes:
            raise MetadataConverterException(
                'Element named "%s" not in fieldTypes' % elementName)

        if fieldTypes[elementName] != elementType:
            raise MetadataConverterException(
                    'Element "%s" should be of %s type, but you are attempting'
                    ' to add it as "%s" type.'
                    % (elementName, fieldTypes[elementName], elementType))

        if location.strip() != '' and elementName != 'publisher':
            raise MetadataConverterException('location can only be used on publisher element')
        # If split is set then split on the split pattern,
        # creating an element for each

        if split.strip() != '':
            valueList = [elem.strip() for elem in strippedValue.split(split)]
        else:
            valueList = [strippedValue]

        if elementType == 'basic':
            for value in valueList:
                if function:
                    value = function(value)
                sub = PYUNTL_DISPATCH[elementName]()
                if qualifier and qualifier.strip() != '':
                    sub.set_qualifier(qualifier)
                sub.set_content(value)
                self.root_element.add_child(sub)
        elif elementType == 'agent':
            for value in valueList:
                if function:
                    value = function(value)
                agent = PYUNTL_DISPATCH[elementName]()
                if qualifier and qualifier.strip() != '':
                    agent.set_qualifier(qualifier)
                agent.add_child(
                    PYUNTL_DISPATCH['name'](content=value))
                if info.strip() != '':
                    agent.add_child(
                        PYUNTL_DISPATCH['info'](content=info.strip()))
                if location.strip() != '':
                    agent.add_child(
                        PYUNTL_DISPATCH['location'](content=location.strip()))
                if agent_type.strip() != '':
                    agent.add_child(
                        PYUNTL_DISPATCH['type'](content=agent_type.strip()))
                self.root_element.add_child(agent)

    def writeTemplateFiles(self, baseDirectory, foldername):
        writeDirectory = os.path.join(baseDirectory, foldername)
        try:
            os.makedirs(writeDirectory)
        except OSError:
            if os.path.exists(writeDirectory):
                pass  # no big deal if they exist
            else:
                raise MetadataConverterException(
                    'Unable to create the output directory %s. ' +
                    'Perhaps you should check permissions?' %
                    writeDirectory)
        with open(os.path.join(writeDirectory, 'metadata.xml'), 'wb') as templateFile:
            templateFile.write(self.__bytes__())
        return '%s finished' % foldername

    def writeJSONFile(self, baseDirectory, foldername, data):
        writeDirectory = os.path.join(baseDirectory, foldername)
        try:
            os.makedirs(writeDirectory)
        except OSError:
            if os.path.exists(writeDirectory):
                pass  # no big deal if they exist
            else:
                raise MetadataConverterException(
                    'Unable to create the output directory %s. '
                    'Perhaps you should check permissions?' % writeDirectory)
        with open(os.path.join(writeDirectory, 'metadata.json'), 'w') as jsonFilename:
            jsonFilename.write(json.dumps(data,
                               sort_keys=True,
                               indent=4,
                               separators=(',', ': ')))

        return '%s finished JSON' % foldername


if __name__ == '__main__':

    parser = ArgumentParser()

    parser.add_argument('mapping',
                        help='Specify the mapping file to use for this CSV')

    parser.add_argument('file',
                        help='Specify a CSV file to process.')

    parser.add_argument('-n', '--row', type=int,
                        dest='row',
                        help='Specify a single row number to process')

    parser.add_argument('-w', '--write', action='store_true',
                        dest='write',
                        help='Write records to files')

    parser.add_argument('-j', '--json', action='store_true',
                        dest='json',
                        help='Write json version of metadata')
    args = parser.parse_args()

    print('Processing CSV file %s with mapping %s' % (args.file, args.mapping))
    mappingPath = os.path.abspath(args.mapping)
    CSVPath = os.path.abspath(args.file)
    CSVRows = CSVToDict(CSVPath)
    localDict = {}

    exec(compile(open(mappingPath).read(), mappingPath, 'exec'), {}, localDict)

    mappingFunction = localDict['processRecord']

    if args.row:
        try:
            CSVRows = [CSVRows[args.row - 1]]
        except IndexError:
            print('Sorry, %s is not a valid row number.' % args.row)
            sys.exit(1)

    for x in range(len(CSVRows)):
        row = CSVRows[x]
        if args.write:
            print('Writing record for row %s' % x)
            record = mappingFunction(MetadataRecord, row)
            record.writeTemplateFiles(record.baseDirectory, record.foldername)
        if args.json:
            print('Writing json record for row %s' % x)
            record = mappingFunction(MetadataRecord, row)
            record.writeJSONFile(record.baseDirectory, record.foldername, row)
        else:
            print('Processing row %s' % x)
            record = mappingFunction(MetadataRecord, row)
            print(record)
