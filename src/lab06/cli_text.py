import argparse
from pathlib import Path

from src.lib.text import normalize, tokenize, count_freq, top_n


def positive_int(value: str) -> int:
    """Проверяет, что аргумент — целое число больше нуля."""
    try:
        number = int(value)
    except ValueError:
        raise argparse.ArgumentTypeError("ожидалось целое число") from None

    if number <= 0:
        raise argparse.ArgumentTypeError("число должно быть больше нуля")

    return number


def cat_file(path: Path, numbered: bool = False) -> None:
    """Выводит файл построчно, при необходимости добавляя номера."""
    with path.open(encoding="utf-8", newline="") as file:
        for number, line in enumerate(file, start=1):
            if numbered:
                print(f"{number:>4}\t", end="")

            print(line, end="")


def print_stats(path: Path, top: int = 5) -> None:
    """Выводит статистику, используя функции из ЛР3 и ЛР5."""
    text = path.read_text(encoding="utf-8")

    normalized_text = normalize(text)
    tokens = tokenize(normalized_text)
    frequencies = count_freq(tokens)

    print(f"Всего слов: {len(tokens)}")
    print(f"Уникальных слов: {len(frequencies)}")
    print(f"Топ-{top}:")

    for word, count in top_n(frequencies, n=top):
        print(f"{word}: {count}")


def main(argv: list[str] | None = None) -> None:
    parser = argparse.ArgumentParser(description="Просмотр файлов и частоты слов")
    subparsers = parser.add_subparsers(dest="command", required=True,)

    # Команда cat.
    cat_parser = subparsers.add_parser("cat", help="Вывести содержимое файла",)
    cat_parser.add_argument("--input", type=Path, required=True, help="Путь к файлу в кодировке UTF-8",)
    cat_parser.add_argument("-n", action="store_true", help="Нумеровать строки с 1",)

    # Команда stats.
    stats_parser = subparsers.add_parser("stats", help="Посчитать частоты слов",)
    stats_parser.add_argument("--input", type=Path, required=True, help="Путь к файлу в кодировке UTF-8",)
    stats_parser.add_argument("--top", type=positive_int, default=5, help="Число слов в топе (по умолчанию: 5)",)

    args = parser.parse_args(argv)

    try:
        if args.command == "cat":
            cat_file(args.input, numbered=args.n)

        elif args.command == "stats":
            print_stats(args.input, top=args.top)

    except FileNotFoundError:
        parser.error(f"Входной файл не найден: {args.input}")

    except UnicodeError:
        parser.error(f"Не удалось прочитать файл как UTF-8: {args.input}")

    except OSError as error:
        parser.error(f"Ошибка чтения файла: {error}")

if __name__ == "__main__":
    main()