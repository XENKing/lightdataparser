import unittest
from unittest.mock import patch

from lightdataparser import extracting


class TestExtractProcess(unittest.TestCase):

    def setUp(self):
        with open("filepaths.txt", 'r') as f:
            self.bad_files = f.read().splitlines()
        self.test_files = "../../input_files"

    def tearDown(self):
        pass

    def test_get_path(self):
        paths = extracting.get_paths(self.bad_files)
        self.assertEqual(paths, [])

    @patch('lightdataparser.extracting.Path.touch', return_value=None)
    def test_get_out_path(self, mock_touch):
        empty_path = extracting.get_out_path('')
        paths = [extracting.get_out_path(file) for file in self.bad_files]
        folder_path = extracting.get_out_path(self.test_files)

    @patch('lightdataparser.extracting.parse', return_value=({'A': 1, 'B': 0, 'C': 3, 'D': 2}, [3, 2, 1, 4]))
    @patch('lightdataparser.extracting.split_nodes', return_value=([], [(0, 3)]))
    @patch('lightdataparser.extracting.parse_nodes')
    def test_extract_data(self, mock_parse_nodes, mock_split_nodes, mock_parse):
        paths = extracting.get_paths([self.test_files])
        data = extracting.extract_data(paths)
        for node in data:
            self.assertEqual(node, [])
