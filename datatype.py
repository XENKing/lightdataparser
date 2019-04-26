"""
Contain base data structures
"""
from collections.abc import MutableSequence
from functools import total_ordering, singledispatch, update_wrapper
from typing import List, overload


def method_dispatch(func):
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[-1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


class CsvMeta(type): pass


class XmlMeta(type): pass


class JsonMeta(type): pass


class CsvObject(metaclass=CsvMeta):
    delimeter = ','
    quotechar = '"'
    def __init__(self, path):
        self.path = path


class TsvObject(CsvObject):
    delimeter = '\t'
    quotechar = '"'

class JsonObject(metaclass=JsonMeta):
    def __init__(self, path):
        self.path = path


class XmlObject(metaclass=XmlMeta):
    def __init__(self, path):
        self.path = path


class DataNode(MutableSequence):
    """A container for manipulating lists of indexes"""

    def __init__(self, name, header: list = None):
        """Initialize the class
        :type header: list
        """
        super(DataNode, self).__init__()
        self.name = name

        if header is not None:
            self._header = list(header)
            self._list = list(range(max(header) + 1))
            for index in self._header:
                self._list[index] = list()
        else:
            self._header = list()
            self._list = list()

    def __repr__(self):
        return "<{0} [name={1}, header={2}, data={3}]>".format(self.__class__.__name__,
                                                               self.name, self._header, self._list)

    def __len__(self):
        return len(self._header)

    def __getitem__(self, index):
        return list(self._list[i][index] for i in self._header)

    def __delitem__(self, index):
        for i in self._header:
            del self._list[i][index]

    def __setitem__(self, index, value: list):
        for i, el in zip(self._header, value):
            self._list[i][index] = el

    def __str__(self):
        return str(list(map(lambda el: list(map(str, el)), self._list)))

    @method_dispatch
    def insert(self, index, value=None):
        if index < max(self._header):
            self._list[index] = list()
            return
        tmp_list = list(range(index + 1))
        for i in self._header:
            tmp_list[i] = self._list[i]
        if value:
            tmp_list[index] = value
        else:
            tmp_list[index] = list()
        self._list = tmp_list

    @insert.register(list)
    def _insert_list(self, index, value):
        for i, el in zip(self._header, value):
            self._list[i].insert(index, el)

    @method_dispatch
    def append(self, value):
        if value in self._header:
            raise IndexError("Specified index already in header")
        self.insert(value)
        self._header.append(value)

    @append.register(list)
    def _append_list(self, value):
        self.insert(len(self._list), value)

    def sort(self, reverse=False):
        self._header.sort(reverse=reverse)

    def getheader(self):
        return self._header
