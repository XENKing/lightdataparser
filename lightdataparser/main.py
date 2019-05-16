from argparse import ArgumentParser
from lightdataparser.dumping import packing_data, dump
from lightdataparser.extracting import *

__version__ = "0.7"


def main(using_gui=False, args=None):
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
        help="use parser files on advanced conditions")
    arg_parser.add_argument(
        "-u", "--use-union",
        dest="union_option",
        action="store_true",
        help="Use union instead of default intersection")
    arg_parser.add_argument(
        "-o", "--out",
        metavar="path",
        dest="output_file",
        help="path to the file in which the processed data will be saved")
    arg_parser.add_argument(
        "-v", "--version",
        action="version",
        version=f"%(prog)s {__version__}")

    if using_gui:
        for key, value in args.items():
            if key == 'output_file':
                output_file = get_out_path(value)
            elif key == 'advanced_option':
                advanced_option = value
            elif key == 'union_option':
                use_union = value
            elif key == 'recursive_option':
                recursive_option = value
            elif key == 'input_path':
                files = value
    else:
        args = arg_parser.parse_args()
        # Если выходого пути не указано, используем 'output.tsv'
        output_file = get_out_path(args.output_file)
        # Разрешаем и преобразовываем все входные пути к файлам
        files = args.files
        # Нужно ли использовать объединения данных заместо пересечения данных по умолчанию
        use_union = args.union_option if args.union_option else False
        advanced_option = args.advanced_option
        recursive_option = args.recursive_option

    files_path = get_paths(files, recursive_option)
    data = extract_data(files_path)

    output = get_format(output_file)
    # Проверяем наличие ключа для выполнения продвинутого задания
    if advanced_option:
        # Запаковываем данные в простой список со строками
        # Используем лямбду для функции сортировки
        new_data = packing_data(data, lambda l: ''.join(l[i] for i in range(3)), use_union=use_union,
                                sum_equal_value=0)  # advanced_result
    else:
        new_data = packing_data(data, lambda l: l[0], use_union=use_union)  # basic_result

    # Пишем выходные строки в файл нужным способом в зависимости от расширения файла
    status = dump(output, new_data)
    return output_file.name, status
