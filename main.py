#!/usr/bin/env python
# coding=utf-8
"""
    Simple application (Extract, Transform, Load) for data organizing
"""
import logging
from argparse import ArgumentParser

from dumping import packing_data, dump
from extracting import get_path, extract_data, get_format

__author__ = "Vladislav Khutorskoy"
__license__ = "MIT"
__version__ = "0.1"

if __name__ == '__main__':
    arg_parser = ArgumentParser(
        prog="light data parser",
        description="Sorts and saves your files in a convenient format for you.")
    arg_parser.add_argument(
        "files",
        metavar='file',
        nargs='+',
        help="Specify files that you want to merge")
    arg_parser.add_argument(
        "-o", "--out",
        metavar="path",
        dest="output_file",
        help="Path to the file in which the processed data will be saved")
    arg_parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}")
    args = arg_parser.parse_args()

    # Prints to output.tsv if a output path isn't specified.
    output = get_format(get_path(args.output_file if args.output_file else "output.tsv"))

    files = [get_path(file) for file in args.files]
    data = extract_data(files)
    # new_data = packing_data(data, lambda l: l[0])  # basic_result
    new_data = packing_data(data, lambda l: ''.join(l[i] for i in range(3)), sum_equal_value=0)  # advanced_result
    dump(output, new_data)
