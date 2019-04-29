#!/usr/bin/env python
# coding=utf-8
"""
    Simple application (Extract, Transform, Load) for data organizing
"""

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
        "-a", "--advanced",
        dest="advanced_option",
        action="store_true",
        help="Parse files on advanced conditions")
    arg_parser.add_argument(
        "-u", "--use-union",
        dest="union_option",
        action="store_true",
        help="Path to the file in which the processed data will be saved")
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

    # Если выходого пути не указано, используем 'output.tsv'
    output = get_format(get_path(args.output_file if args.output_file else "output.tsv", create_if_not_exist=True))
    # Разрешаем и преобразовываем все входные пути к файлам
    files = [get_path(file) for file in args.files]
    data = extract_data(files)

    # Нужно ли использовать объединения данных заместо пересечения данных по умолчанию
    use_union = args.union_option if args.union_option else False

    # Проверяем наличие ключа для выполнения продвинутого задания
    if args.advanced_option:
        # Запаковываем данные в простой список со строками
        # Используем лямбду для функции сортировки
        new_data = packing_data(data, lambda l: ''.join(l[i] for i in range(3)), use_union=use_union,
                                sum_equal_value=0)  # advanced_result
    else:
        new_data = packing_data(data, lambda l: l[0], use_union=use_union)  # basic_result

    # Пишем выходные строки в файл нужным способом в зависимости от расширения файла
    dump(output, new_data)
