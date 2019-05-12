"""
Используемые структуры
"""
from collections.abc import MutableSequence
from functools import singledispatch, update_wrapper


def method_dispatch(func):
    """
Переопределение единой диспетчеризации для методов класса
https://stackoverflow.com/questions/24601722/how-can-i-use-functools-singledispatch-with-instance-methods
    """
    dispatcher = singledispatch(func)

    def wrapper(*args, **kw):
        # Используем последний аргумент в качестве выбора типа для диспетчеризации
        return dispatcher.dispatch(args[-1].__class__)(*args, **kw)

    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)
    return wrapper


# Метаклассы, на которые будет опираться функция диспетчеризации
class CsvMeta(type):
    pass


class XmlMeta(type):
    pass


class JsonMeta(type):
    pass


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
    """
Последовательный контейнер для организации хранения узлов(групп) данных
    """

    def __init__(self, name, header: list = None):
        super(DataNode, self).__init__()
        # Имеет своё имя, для удобного взаимодействия
        self.name = name

        if header is not None:
            # Если Загловок узла не пустой, копируем его, создаем списков по максимальному числу в заголовке
            self._header = list(header)
            self._list = list(range(max(header) + 1))
            for index in self._header:
                self._list[index] = list()
        else:
            # Иначе - проосто инициализируем
            self._header = list()
            self._list = list()

    def __repr__(self):
        """
Красивый вывод для класса
        """
        return "<{0} [name={1}, header={2}, data={3}]>".format(self.__class__.__name__,
                                                               self.name, self._header, self._list)

    def __len__(self):
        return len(self._header)

    def __getitem__(self, index):
        """
        :param index: Номер строки в списке списков
        :return: Новый список из каждого списка с указанным индексом
        """
        return list(self._list[i][index] for i in self._header)

    def __delitem__(self, index):
        for i in self._header:
            del self._list[i][index]

    def __setitem__(self, index, value: list):
        for i, el in zip(self._header, value):
            self._list[i][index] = el

    def __str__(self):
        """
Собираем все списки в строку
        """
        return str([[str(el) for el in r] for i, r in enumerate(self._list) if i in self._header])

    @method_dispatch
    def insert(self, index, value=None):
        """
Вставить значение как индекс в заголовке и выделяем для индекса новый список
        :param index: Куда вставлять
        :param value: Что добавлять
        """
        if index < max(self._header):
            if value:
                self._list[index] = value
            else:
                self._list[index] = list()
            return
        # Cоздаем новый массив ссылок нужной длины
        tmp_list = list(range(index + 1))
        # Переприсваиваем и создаем новые ссылки во временном списке
        for i in self._header:
            tmp_list[i] = self._list[i]
        if value:
            tmp_list[index] = value
        else:
            tmp_list[index] = list()
        # Меняем ссылку на новый массив ссылок
        self._list = tmp_list

    @insert.register(list)
    def _insert_list(self, index, value):
        """
Вставить значения из списка, длина которого строго равна длине заголовочного списка
        :param index: Куда вставлять
        :param value: Список-строка с данными
        """
        for i, el in zip(self._header, value):
            self._list[i].insert(index, el)

    @method_dispatch
    def append(self, value):
        """
Добавить новый индекс в заголовочный список
        :param value: индекс
        """
        if value in self._header:
            raise IndexError("Specified index already in header")
        # Выделяем новое место
        self.insert(value)
        # Потом добавляем в заголовок
        self._header.append(value)

    @append.register(list)
    def _append_list(self, value):
        """
Добавить новые значения в конец списка узла
        :param value:
        """
        self.insert(len(self._list), value)

    def sort(self, reverse=False):
        """
Сортировка обеспечивается только применением сортировки к заголовку
        """
        self._header.sort(reverse=reverse)

    def getheader(self):
        """
        :return: Заголовочный список
        """
        return self._header
