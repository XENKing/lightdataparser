"""
Функции извлечения данных
"""

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
            path = Path(file).resolve(strict=True)
        except FileNotFoundError as e:
            print("Failed to read: %s" % e)
        except PermissionError as e:
            print("PermissionError: %s" % e)
        except Exception as e:
            print(e)
        else:
            if path.is_dir():
                path = [f for f in path.iterdir()] if not recusive else [i for i in path.rglob("*")]
            paths.append(path)

    paths = sum(paths, [])
    return paths


def get_out_path(file: str, default_name: str = "output.tsv") -> Path:
    try:
        path = Path(file).resolve(strict=True)
    except FileNotFoundError:
        for name in reversed(file.split('/')):
            if name is not '':
                Path(Path.cwd().joinpath(name)).touch()
                break
        Path(Path.cwd().joinpath(file)).touch()
        path = Path(file).resolve(strict=True)
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
