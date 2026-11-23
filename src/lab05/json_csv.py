import csv
import json
from pathlib import Path


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Загружает JSON-массив, проверяет записи и сохраняет их в CSV."""
    json_path = Path(json_path)
    csv_path = Path(csv_path)

    if json_path.suffix.lower() != ".json":
        raise ValueError("Ожидался файл с расширением .json")

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Ожидался файл с расширением .csv")

    with json_path.open(encoding="utf-8") as f:
        items = json.load(f)

    if not isinstance(items, list):
        raise ValueError("Ожидался JSON-массив словарей")

    if not items:
        raise ValueError("JSON-массив пуст: нет записей для конвертации")

    fieldnames = []

    for item in items:
        if not isinstance(item, dict):
            raise ValueError("Ожидался JSON-массив словарей")

        for key, value in item.items():
            if not key.strip():
                raise ValueError("Название колонки не должно быть пустым")

            if isinstance(value, (list, dict)):
                raise ValueError("Вложенные списки и словари не поддерживаются")

            if key not in fieldnames:
                fieldnames.append(key)

    if not fieldnames:
        raise ValueError("В JSON нет полей для заголовка")

    try:
        same_file = csv_path.samefile(json_path)
    except FileNotFoundError:
        same_file = False

    if same_file:
        raise ValueError("Входной и выходной пути должны различаться")

    csv_path.parent.mkdir(parents=True, exist_ok=True)

    with csv_path.open("w", encoding="utf-8", newline="") as out:
        writer = csv.DictWriter(out, fieldnames=fieldnames, restval="")
        writer.writeheader()
        writer.writerows(items)

def csv_to_json(csv_path: str, json_path: str) -> None:
    """Проверяет CSV и записывает JSON по одной записи."""
    csv_path = Path(csv_path)
    json_path = Path(json_path)

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Ожидался файл с расширением .csv")

    if json_path.suffix.lower() != ".json":
        raise ValueError("Ожидался файл с расширением .json")

    _check_distinct_files(csv_path, json_path)

    try:
        with csv_path.open(encoding="utf-8", newline="") as f:
            reader = csv.reader(f, delimiter=",", strict=True)
            header = next(reader, None)

            if not header:
                raise ValueError("Пустой CSV или отсутствует заголовок")

            if any(not name.strip() for name in header):
                raise ValueError("Название колонки не должно быть пустым")

            if len(set(header)) != len(header):
                raise ValueError("Названия колонок не должны повторяться")

            with _atomic_output(json_path) as out:
                out.write("[")
                first = True

                for row in reader:
                    if len(row) != len(header):
                        raise ValueError("Количество полей не совпадает с заголовком")

                    if not first:
                        out.write(",")

                    record = dict(zip(header, row))
                    text = json.dumps(record, ensure_ascii=False, indent=2)
                    out.write("\n" + indent(text, "  "))
                    first = False

                if not first:
                    out.write("\n")

                out.write("]")

    except csv.Error as error:
        raise ValueError("Некорректный CSV") from error