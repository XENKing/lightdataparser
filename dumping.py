import csv
import re
from functools import singledispatch
from pathlib import Path
from typing import List

from datatype import CsvObject, DataNode


def packing_data(output_data: List[List[DataNode]], sort_func, use_union=False, **kwargs):
    def set_operator(sets, index, list_data):
        try:
            if use_union:
                sets[index] = sets[index].union(list_data)
            else:
                sets[index] = sets[index].intersection(list_data)
        except IndexError:
            sets.append(set(list_data))

    def decompose_header(data, data_func):
        sets = []
        for file in data:
            for it, node_data in enumerate(file):
                node_data.sort()
                set_operator(sets, it, data_func(node_data))
        return sets

    def sort_sets(sets):
        def natural_keys(text):
            return [int(c) if c.isdigit() else c for c in re.findall(r'(\d+)', str(text))]

        return [sorted(s, key=natural_keys) for s in sets]

    header_sets = decompose_header(output_data, lambda n: n.getheader())
    name_sets = []
    data = []
    for file_data in output_data:
        out_rows = []
        for idx, node in enumerate(file_data):
            name = node.name
            if "sum_equal_value" in kwargs and kwargs["sum_equal_value"] != idx:
                name = node.name+"S"
            name_list = [name + str(el) for el in sorted(header_sets[idx])]
            set_operator(name_sets, idx, name_list)
            for i, el in enumerate(node):
                try:
                    out_rows[i].extend(el[:len(header_sets[idx])])
                except IndexError:
                    out_rows.append(el[:len(header_sets[idx])])

        data.extend(out_rows)
    if "sum_equal_value" in kwargs:
        offset = 0
        not_include = (0, 0)
        for i, el in enumerate(header_sets):
            if kwargs["sum_equal_value"] == i:
                not_include = (offset, offset + len(el))
                break
            offset += len(el)
        sort_val = [sort_func(el) for el in data]
        duplicates = [(sort_val.index(el), i) for i, el in enumerate(sort_val) if i != sort_val.index(el)]
        duplicates.sort(reverse=True, key=lambda l: l[1])
        for a, b in duplicates:
            l, r = not_include
            for idx, (i, j) in enumerate(zip(data[a], data[b])):
                if idx not in range(l, r):
                    i = int(i)
                    data[a][idx] = i
                    data[a][idx] += int(j)
            data.pop(b)

    data.sort(key=sort_func)
    header = sum(sort_sets(name_sets), [])
    data.insert(0, header)
    return data


@singledispatch
def dump(file, data):
    print("Unsupported file type: {}".format(file))


@dump.register(CsvObject)
def _dump_csv(file, data):
    with open(file.path, 'w') as f:
        writer = csv.writer(f, delimiter=file.delimeter, quotechar=file.quotechar, quoting=csv.QUOTE_NONE)
        for row in data:
            writer.writerow(row)
