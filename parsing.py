import csv
import re
import json
from typing import Tuple, List
from xml.etree import ElementTree
from functools import singledispatch

import config
from datatype import DataNode, TsvObject, CsvObject, JsonObject, XmlObject


@singledispatch
def parse(file):
    print("Unsupported file type: {}".format(file))
    return {}, []


@parse.register(CsvObject)
def _parse_csv(file):
    with open(file.path, 'r') as f:
        data = list(csv.reader(f, delimiter=file.delimeter))
        header = compose_header(data.pop(0))
        return header, data


@parse.register(JsonObject)
def _parse_json(file):
    with open(file.path, 'r') as f:
        try:
            data = json.load(f)
        except ValueError as e:
            print("Can't load json data in %s: %s" % (file.path, e))
            return None
        data = next(iter(data.values()))
        nodes = list(next(iter(data)).keys())

        header = compose_header(nodes)
        data = [list(raw.values()) for raw in data]
        return header, data


@parse.register(XmlObject)
def _parse_xml(file):
    root = ElementTree.parse(file.path).getroot()
    nodes = [t.attrib[config.xml_node_header] for t in root.find(config.xml_node_group).findall(config.xml_node_item)]
    data = []
    for tag in root.findall(config.xml_node_group):
        data.append(list(t.find(config.xml_node_data).text for t in tag.findall(config.xml_node_item)))
    header = compose_header(nodes)
    return header, data

    # parse xml with regex
    # re.match(r"<(\S+)(?:\s+(\w+)=\"(\w+)?\")?[^>]*>\s*(\S*)\s*<\/\1>",str, re.I)


def compose_header(header: list) -> {}:
    keys = set()
    ids = dict()

    for el in header:
        match = re.match(r"([a-z]+)([0-9]+)", el, re.I)
        if match:
            key, index = match.groups()
            if key not in keys:
                keys.add(key)
                ids[key] = []
            ids[key].append(int(index))
    return ids


def split_nodes(header: dict) -> Tuple[List[DataNode], List[Tuple[int, int]]]:
    nodes = []
    bounds = []
    bound_offset = 0
    for key, value in header.items():
        nodes.append(DataNode(key, value))
        bounds.append((bound_offset, bound_offset + len(value)))
        bound_offset += len(value)
    return nodes, bounds


def parse_nodes(nodes: list, bounds: list, data: list):
    for raw in data:
        for node, bound in zip(nodes, bounds):
            node.append(raw[bound[0]:bound[1]])
