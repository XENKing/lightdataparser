"""
Функции извлечения данных
"""
import re
from pathlib import Path
from typing import List

from lightdataparser.datatype import DataNode, TsvObject, CsvObject, JsonObject, XmlObject
from lightdataparser.parsing import parse, split_nodes, parse_nodes


def get_paths(files: list, recusive: bool = False) -> list:
    """
Получает пути к файлу или папке
    :param files: Список строковых путей файлов
    :param recusive: Рекурсинвый проход через все вложенные директории
                    **Только для директории**
    :return: Список объектов типа Path
    """
    paths = []
    for file in files:
        try:
            path = Path(file).expanduser().resolve(strict=True)
        except FileNotFoundError as e:
            print("Failed to read: %s" % e)
        except PermissionError as e:
            print("PermissionError: %s" % e)
        else:
            if path.is_dir():
                path = [f for f in path.iterdir() if not f.is_dir()] if not recusive else [i for i in path.rglob("*")]
            paths.append(path)

    paths = sum(paths, [])
    return paths


def get_out_path(file: str, default_name: str = "output.tsv") -> Path:
    path = Path.cwd().joinpath(default_name)
    if not file:
        Path(path).touch()
        return path
    try:
        path = Path(file).resolve(strict=True)
    except FileNotFoundError:
        match = re.match(r"^(.*/+)?([^/]*)$", file)
        if match:
            directory = Path.cwd()
            if match.group(1):
                try:
                    directory = Path(match.group(1)).expanduser().resolve(strict=True)
                except FileNotFoundError:
                    pass
            path = directory.joinpath(match.group(2)) if match.group(2) else directory.joinpath(default_name)
    except Exception:
        pass
    else:
        if path.is_dir():
            path.joinpath(default_name)

    Path(path).touch()
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
