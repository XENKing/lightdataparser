import unittest
from unittest.mock import patch, mock_open

from lightdataparser.datatype import DataNode, CsvObject

from lightdataparser import dumping


class TestDumpingProcess(unittest.TestCase):

    def test_sort_sets(self):
        sets = [{'A2', 'D3', 'C4', 'B1'}, {'G4', 'E2', 'F0'}]
        sort_sets = dumping.sort_sets(sets)
        self.assertEqual(sort_sets, [['B1', 'A2', 'D3', 'C4'], ['F0', 'E2', 'G4']])

    def test_packing_data(self):
        output_data = [[DataNode('A', [0]), DataNode('B', [0]),
                        DataNode('C', [0]), DataNode('D', [0])],
                       [DataNode('A', [0]), DataNode('B', [0]), DataNode('K', [0])]]
        data = [[[4, 1], [5, 3], [0, 2], [3, 7]], [[3, 1], [4, 4], [0, 9]]]
        results = [[[1, 3, 2, 7], [1, 4, 9], [3, 4, 0], [4, 5, 0, 3]],
                   [[1, 3, 2, 7], [3, 4, 0], [1, 4, 9], [4, 5, 0, 3]],
                   [[7, 5, 0, 3], [1, 3, 2, 7], [1, 4, 9]]]

        for i, j in zip(output_data, data):
            for k, l in zip(i, j):
                k._list[0].extend(l)

        for i in range(3):
            packed_data = dumping.packing_data(output_data, lambda l, n=i: l[n],
                                               use_union=True if i == 1 else False) if i != 2 else dumping.packing_data(
                output_data, lambda l, n=i: l[n], use_union=True if i == 1 else False, sum_equal_value=1)
            packed_data.pop(0)  # Т.к. в множествах порядок не сохраняется, столбцы могут быть различны
            self.assertEqual(packed_data, results[i])

    def test_dump(self):
        data = [['A0', 'B0', 'D0'], [1, 3, 2, 7], [1, 4, 9], [3, 4, 0], [4, 5, 0, 3]]

        dumping.dump(object(), data)

        with patch('lightdataparser.dumping.open', new=mock_open()):
            dumping.dump(CsvObject('out.csv'), data)
