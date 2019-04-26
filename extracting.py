from pathlib import Path
from typing import List

from datatype import DataNode, TsvObject, CsvObject, JsonObject, XmlObject
from parsing import parse, split_nodes, parse_nodes


def get_path(file: str) -> Path:
    path = None
    try:
        path = Path(file).resolve(strict=True)
    except FileNotFoundError as e:
        print("Failed to read: %s" % e)
    return path


def get_format(file: Path):
    if file.suffix == ".tsv":
        return TsvObject(file)
    elif file.suffix == ".csv":
        return CsvObject(file)
    elif file.suffix == ".json":
        return JsonObject(file)
    elif file.suffix == ".xml":
        return XmlObject(file)


def extract_data(files: list) -> List[List[DataNode]]:
    input_data = []
    for file in files:
        file_obj = get_format(file)
        header, data = parse(file_obj)
        nodes, bounds = split_nodes(header)
        parse_nodes(nodes, bounds, data)
        input_data.append(nodes)
    return input_data
