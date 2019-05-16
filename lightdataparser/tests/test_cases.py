import unittest
import sys
from unittest.mock import patch, DEFAULT

from lightdataparser import main


class TestMainCases(unittest.TestCase):

    def test_file_simple(self):
        with patch.multiple('lightdataparser.main', get_out_path=DEFAULT, get_format=DEFAULT, get_paths=DEFAULT,
                            extract_data=DEFAULT, packing_data=DEFAULT, dump=DEFAULT):
            test_args = [['path', '-h'], ['path', '-v'], ['path', 'test.csv'], ['path', 'test.csv', 'test.json'],
                         ['path', 'folder'], ['path', '-r', 'folder'], ['path', '-o', 'out.tsv', 'test.csv'],
                         ['path', '-a', 'test.csv'], ['path', '-u', 'test.csv']]

            for i, args in enumerate(test_args):
                with patch('lightdataparser.tests.test_cases.sys.argv', new=args):
                    if i < 2:
                        with self.assertRaises(SystemExit):
                            main.main()
                    else:
                        main.main()
            gui_args = {'recursive_option': False, 'union_option': False, 'advanced_option': False, 'output_file': '',
                        'input_path': ''}

            main.main(True, gui_args)
