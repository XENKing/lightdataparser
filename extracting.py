"""
Функции извлечения данных
"""

from pathlib import Path
from typing import List

from datatype import DataNode, TsvObject, CsvObject, JsonObject, XmlObject
from parsing import parse, split_nodes, parse_nodes


def get_path(file: str, create_if_not_exist: bool = False) -> Path:
    """
Проверяет существование указанного пути к файлу
    :param file: строковое местоположение файла/пути
    :param create_if_not_exist: Создать файл по указанному пути если его не существует
    :return: объект типа Path
    """
    path = None
    try:
        path = Path(file).resolve(strict=True)
    except FileNotFoundError as e:
        print("Failed to read: %s" % e)
        if create_if_not_exist:
            f = open(file, 'w')
            f.close()
            path = Path(file).resolve(strict=True)
    return path


def get_format(file: Path) -> object:
    """
Распознает формат и возвращает объект, ассоциированный с расширением файла
    :param file: Существующий путь к файлу
    :return: Ассоциированный объект класса
    """
    if file.suffix == ".tsv":
        return TsvObject(file)
    elif file.suffix == ".csv":
        return CsvObject(file)
    elif file.suffix == ".json":
        return JsonObject(file)
    elif file.suffix == ".xml":
        return XmlObject(file)


def extract_data(files: list) -> List[List[DataNode]]:
    """
Собирает полученные данные в список узлов
    :param files: Список путей к файлам
    :return: Список содержащий список с узлами из каждого файла
    """
    input_data = []
    for file in files:
        file_obj = get_format(file)
        header, data = parse(file_obj)
        nodes, bounds = split_nodes(header)
        parse_nodes(nodes, bounds, data)
        input_data.append(nodes)
    return input_data
