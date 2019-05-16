"""
Функции записи данных
"""

import csv
import re
from functools import singledispatch
from typing import List

from lightdataparser.datatype import CsvObject, DataNode


def sort_sets(sets: List[set]) -> list:
    """
Сортировка с парсиногом чисел из строки
    :param sets: Входное множество
    :return: Выходной сортированный список
    """

    def natural_keys(text):
        return [int(c) if c.isdigit() else c for c in re.findall(r'(\d+)', str(text))]

    return [sorted(s, key=natural_keys) for s in sets]


def packing_data(output_data: List[List[DataNode]], sort_func, use_union=False, **kwargs) -> list:
    """
Упаковка списка списков узлов каждого файла в целое с указанными условиями (лямбда) сортировки
    :param output_data: Выходные данные по каждому файлу в виде списка узлов
    :param sort_func: Функция для выбора сортируемых данных
    :param use_union: Использовать объединение данных (По умолчанию - пересечение)
    :param kwargs: Пока единственный дополнительный параметр :key sum_equal_value, коотрый говорит о том,
     что нужно суммировать все значения с повторяющимся индексом, кроме указанного в value столбца
    :return: Готовый для экспорта список с первой строкой - заголовоком, и остальными - значениями
    """

    def set_operator(sets, index, list_data):
        """
Выбор оператора объединения данных в зависимости от состояния ключа
        :param sets: Список с заголовками файлов
        :param index: Номер файла
        :param list_data: Список с данными по номеру файла
        """
        try:
            if use_union:
                sets[index] = sets[index].union(list_data)
            else:
                sets[index] = sets[index].intersection(list_data)
        except IndexError:
            sets.append(set(list_data))

    def decompose_header(data, data_func):
        """
Сборка и объединение заголовков для каждого файла
        :param data: Исходные данных
        :param data_func: Функция для получения заголовка
        :return: Список списков из множеств заголовков
        """
        sets = []
        for file_data in data:
            for it, node_data in enumerate(file_data):
                node_data.sort()
                set_operator(sets, it, data_func(node_data))
        return sets

    # Сортированный список с заголовками
    header_sets = decompose_header(output_data, lambda n: n.getheader())
    # Список с выходными именами
    name_sets = []
    # Список с выходными строками данных
    data = []
    for file_data in output_data:
        out_rows = []
        for idx, node in enumerate(file_data):
            name = node.name
            # Смотрим на доп параметр и номер стоблца
            if "sum_equal_value" in kwargs and kwargs["sum_equal_value"] != idx:
                # если есть, дописываем каждому имени доп букву 'S'
                name = node.name + "S"
            name_list = [name + str(el) for el in sorted(header_sets[idx])]
            # Собираем и сортируем все имена вместе
            set_operator(name_sets, idx, name_list)
            for i, el in enumerate(node):
                try:
                    # пробуем объеденить с выходными строками построчно
                    out_rows[i].extend(el[:len(header_sets[idx])])
                except IndexError:
                    # Если у нас нет такой строки, добавляем в конец
                    out_rows.append(el[:len(header_sets[idx])])
        # Объединяем с существующими данными
        data.extend(out_rows)

    # Если указан доп параметр, складываем повторяющиеся столбцы
    if "sum_equal_value" in kwargs:
        offset = 0
        # Ищем границы, по которым НЕ нужно суммировать
        not_include = (0, 0)
        for i, el in enumerate(header_sets):
            if kwargs["sum_equal_value"] == i:
                not_include = (offset, offset + len(el))
                break
            offset += len(el)

        # Сортируем исключаемые данные функцией сортировки
        sort_val = [sort_func(el) for el in data]
        # Формируем список кортежей с повтороными индексами
        duplicates = [(sort_val.index(el), i) for i, el in enumerate(sort_val) if i != sort_val.index(el)]
        # сортируем в обратном порядке по второму элементу кортежа (для корректного удаления)
        duplicates.sort(reverse=True, key=lambda l: l[1])
        # Складываем и удаляем столбцы с повторяющимися значениями в индексах
        for a, b in duplicates:
            l, r = not_include
            for idx, (i, j) in enumerate(zip(data[a], data[b])):
                if idx not in range(l, r):
                    i = int(i)
                    data[a][idx] = i
                    data[a][idx] += int(j)
            data.pop(b)
        # На выходе имеем строки с уникальными именами и индексами
    # Сортируем строки по заданной функции
    data.sort(key=sort_func)
    header = sum(sort_sets(name_sets), [])
    # Вставляем первой строкой сортированный список заголовочных имен
    data.insert(0, header)
    return data


@singledispatch
def dump(file, data):
    """
Общая управляемая функция для сохранения данных
    :param file: Объект с типом файла
    :param data: Строки с данными
    """
    print("Can't save.\nUnsupported file type: {}".format(file))
    return False


@dump.register(CsvObject)
def _dump_csv(file, data):
    with open(file.path, 'w') as f:
        writer = csv.writer(f, delimiter=file.delimeter, quotechar=file.quotechar, quoting=csv.QUOTE_NONE)
        for row in data:
            writer.writerow(row)
    return True
