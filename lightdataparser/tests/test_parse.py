import unittest
from unittest.mock import patch, mock_open

from lightdataparser import parsing
from lightdataparser.datatype import CsvObject, JsonObject, XmlObject, TsvObject, DataNode


class TestParseProcess(unittest.TestCase):

    def test_parse_unsupported(self):
        data = parsing.parse(object())
        self.assertEqual(data, ({}, []))

    def test_parse(self):
        files = [CsvObject('test.csv'), TsvObject('test.tsv'), JsonObject('test.json')]
        datas = ['A2,B1,C4,D3\n3,2,1,0', 'A2\tB1\tC4\tD3\n3\t2\t1\t0',
                 '{"fields": [{"A2":3,"B1":2,"C4":1,"D3":0}]}']
        for file, read_data in zip(files, datas):
            with patch('lightdataparser.parsing.open', new=mock_open(read_data=read_data)):
                header, data = parsing.parse(file)
                self.assertEqual(header, {'A': [2], 'B': [1], 'C': [4], 'D': [3]})
                self.assertEqual(data, [['3', '2', '1', '0']])

    def test_parse_json_exception(self):
        datas = ['#$!@', '{1:2}', '{"1":[{"2":3}}]']
        for read_data in datas:
            with patch('lightdataparser.parsing.open', new=mock_open(read_data=read_data)):
                parsing.parse(JsonObject('test.json'))
                from json import JSONDecodeError
                self.assertRaises(JSONDecodeError)

    def test_parse_xml(self):
        file = XmlObject('test.xml')
        read_data = '''<?xml version="1.0" encoding="UTF-8" ?>\n
            <root>\n
                <objects>\n
                    <object name="A2">\n
                        <value>3</value>\n
                    </object>\n
                    <object name="B1">\n
                        <value>2</value>\n
                    </object>\n
                    <object name="C4">\n
                        <value>1</value>\n
                    </object>\n
                    <object name="D3">\n
                        <value>0</value>\n
                    </object>\n
                </objects>\n
            </root>\n'''
        with patch('lightdataparser.parsing.ElementTree.open', new=mock_open(read_data=read_data)):
            header, data = parsing.parse(file)
            self.assertEqual(header, {'A': [2], 'B': [1], 'C': [4], 'D': [3]})
            self.assertEqual(data, [['3', '2', '1', '0']])

    @patch('lightdataparser.parsing.DataNode', return_value='')
    def test_split_nodes(self, mock_node):
        header = {'A': [2], 'B': [1], 'C': [4], 'D': [3]}
        nodes, bounds = parsing.split_nodes(header)
        self.assertEqual(nodes, ['', '', '', ''])
        self.assertEqual(bounds, [(0, 1), (1, 2), (2, 3), (3, 4)])

    def test_parse_nodes(self):
        nodes = [DataNode('A', [2]), DataNode('B', [1]), DataNode('C', [4]), DataNode('D', [3])]
        bounds = [(0, 1), (1, 2), (2, 3), (3, 4)]
        data = [['3', '2', '1', '0']]
        parsing.parse_nodes(nodes, bounds, data)
        for node, el in zip(nodes, data[0]):
            self.assertEqual(node[0], list(str(el)))
