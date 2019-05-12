import unittest
from unittest.mock import patch

from lightdataparser import datatype


class TestDataTypes(unittest.TestCase):

    def test_datanode(self):
        emptyNode = datatype.DataNode('Name')
        print(emptyNode, len(emptyNode))
        del emptyNode

        node = datatype.DataNode('Name', [2, 3])
        with self.assertRaises(IndexError):
            node.append(2)
        node.append(4)
        with self.assertRaises(IndexError):
            node[0] = [4]
        with self.assertRaises(IndexError):
            del node[0]
        with self.assertRaises(IndexError):
            print(node[0])
        node.insert(0)
        node.insert(1, 1)
        node.insert(5, 1)
        node.append([2, 3, 4])
        print(repr(node))
