import argparse
import csv
from pathlib import Path

from src.lab05.json_csv import json_to_csv, csv_to_json
from src.lab05.csv_xlsx import csv_to_xlsx


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Конвертация JSON, CSV и XLSX")
    subparsers = parser.add_subparsers(dest="command", required=True,)

    converters = {
        "json2csv": (json_to_csv, "Преобразовать JSON в CSV",),
        "csv2json": (csv_to_json, "Преобразовать CSV в JSON",),
        "csv2xlsx": (csv_to_xlsx, "Преобразовать CSV в XLSX",),
    }

    for name, (function, description) in converters.items():
        command_parser = subparsers.add_parser(name, help=description,)
        command_parser.add_argument("--in", dest="input", type=Path, required=True, help="Путь к входному файлу",)
        command_parser.add_argument("--out", dest="output", type=Path, required=True, help="Путь к выходному файлу",)
        command_parser.set_defaults(handler=function)

    args = parser.parse_args(argv)

    try:
        if args.input.resolve() == args.output.resolve():
            parser.error("Входной и выходной пути должны различаться")

        args.handler(args.input, args.output)

    except FileNotFoundError as error:
        parser.error(f"Файл или каталог не найден: {error.filename}")

    except UnicodeError:
        parser.error("Не удалось прочитать или записать текст в кодировке UTF-8")

    except (ValueError, csv.Error) as error:
        parser.error(f"Некорректные данные: {error}")

    except OSError as error:
        parser.error(f"Ошибка работы с файлом: {error}")

    print(f"Готово: {args.output}")


if __name__ == "__main__":
    main()