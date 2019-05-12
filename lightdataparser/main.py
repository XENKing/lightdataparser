from argparse import ArgumentParser
from lightdataparser.dumping import packing_data, dump
from lightdataparser.extracting import *

__version__ = "0.5"


def main(args=None):
    arg_parser = ArgumentParser(
        prog="light data parser",
        description="sorts and saves your files in a convenient format for you.")
    arg_parser.add_argument(
        "files",
        metavar='file',
        nargs='+',
        help="specify files or directory to merge")
    arg_parser.add_argument(
        "-r", "--recursive",
        dest="recursive_option",
        action="store_true",
        help="recursive search of files in subfolders at the specified path")
    arg_parser.add_argument(
        "-a", "--advanced",
        dest="advanced_option",
        action="store_true",
        help="use parse test_files on advanced conditions")
    arg_parser.add_argument(
        "-u", "--use-union",
        dest="union_option",
        action="store_true",
        help="path to the file in which the processed data will be saved")
    arg_parser.add_argument(
        "-o", "--out",
        metavar="path",
        dest="output_file",
        help="path to the file in which the processed data will be saved")
    arg_parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}")

    # Если выходого пути не указано, используем 'output.tsv'
    args = arg_parser.parse_args()
    output_file = get_out_path(args.output_file)
    output = get_format(output_file)

    # Разрешаем и преобразовываем все входные пути к файлам
    files = get_paths(args.files, args.recursive_option)
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
