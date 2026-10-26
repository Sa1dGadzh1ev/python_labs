import argparse

from src.lab04.io_txt_csv import read_text, write_csv
from src.lib.text import normalize, tokenize, count_freq, top_n


def main() -> None:
    """Прочитать один файл и сохранить отчёт по частотам слов."""

    parser = argparse.ArgumentParser(description="Статистика слов")

    parser.add_argument("--in", dest="input_path", default="data/lab04/input.txt",)

    parser.add_argument("--out", dest="out_path", default="data/lab04/report.csv",)

    parser.add_argument("--encoding", default="utf-8",)

    args = parser.parse_args()

    input_path = args.input_path
    out_path = args.out_path
    encoding = args.encoding

    text = read_text(input_path, encoding=encoding)
    normalized_text = normalize(text)
    tokens = tokenize(normalized_text)
    freq = count_freq(tokens)

    total_words = len(tokens)
    unique_words = len(freq)

    rows = top_n(freq, unique_words)

    write_csv(rows, out_path, header=("word", "count"),)

    print("Всего слов:", total_words)
    print("Уникальных слов:", unique_words)
    print("Топ-5:")

    top_words = top_n(freq, 5)

    for pair in top_words:
        word = pair[0]
        count = pair[1]

        print(f"{word}:{count}")


if __name__ == "__main__":
    main()