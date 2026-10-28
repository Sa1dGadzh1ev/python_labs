import csv
import json
from pathlib import Path


def read_json_objects(f):
    """Читает JSON-массив по одному словарю, включая многострочные объекты."""
    state = "start"
    chars = []
    depth = 0
    in_string = False
    escaped = False

    while True:
        chunk = f.read(65536)
        if not chunk:
            break

        for char in chunk:
            if state == "object":
                chars.append(char)

                if in_string:
                    if escaped:
                        escaped = False
                    elif char == "\\":
                        escaped = True
                    elif char == '"':
                        in_string = False
                elif char == '"':
                    in_string = True
                elif char == "{":
                    depth += 1
                elif char == "}":
                    depth -= 1

                    if depth == 0:
                        item = json.loads("".join(chars))
                        chars = []
                        state = "separator"
                        yield item

                continue

            if char in " \t\r\n":
                continue

            if state == "start" and char == "[":
                state = "first"

            elif state in ("first", "next") and char == "{":
                chars = [char]
                depth = 1
                in_string = False
                escaped = False
                state = "object"

            elif state == "first" and char == "]":
                state = "end"

            elif state == "separator" and char == ",":
                state = "next"

            elif state == "separator" and char == "]":
                state = "end"

            else:
                raise ValueError("Ожидался JSON-массив словарей")

    if state == "start":
        raise ValueError("Пустой JSON или неподдерживаемая структура")

    if state != "end":
        raise ValueError("Пустой или незавершённый JSON")


def json_to_csv(json_path: str, csv_path: str) -> None:
    """Преобразует JSON в CSV за два прохода без загрузки всего списка."""
    json_path = Path(json_path)
    csv_path = Path(csv_path)

    if json_path.suffix.lower() != ".json":
        raise ValueError("Ожидался файл с расширением .json")

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Ожидался файл с расширением .csv")

    with json_path.open(encoding="utf-8") as f:
        fieldnames = []
        has_items = False

        for item in read_json_objects(f):
            has_items = True

            for key, value in item.items():
                if not key.strip():
                    raise ValueError("Название колонки не должно быть пустым")

                if isinstance(value, (list, dict)):
                    raise ValueError("Вложенные списки и словари не поддерживаются")

                if key not in fieldnames:
                    fieldnames.append(key)

        if not has_items:
            raise ValueError("Пустой JSON или неподдерживаемая структура")

        if not fieldnames:
            raise ValueError("В JSON нет полей для заголовка")

        f.seek(0)
        csv_path.parent.mkdir(parents=True, exist_ok=True)

        with csv_path.open("w", encoding="utf-8", newline="") as out:
            writer = csv.DictWriter(out, fieldnames=fieldnames, restval="")
            writer.writeheader()

            for item in read_json_objects(f):
                writer.writerow(item)


def csv_to_json(csv_path: str, json_path: str) -> None:
    """Проверяет CSV и записывает JSON по одной записи."""
    csv_path = Path(csv_path)
    json_path = Path(json_path)

    if csv_path.suffix.lower() != ".csv":
        raise ValueError("Ожидался файл с расширением .csv")

    if json_path.suffix.lower() != ".json":
        raise ValueError("Ожидался файл с расширением .json")

    with csv_path.open(encoding="utf-8", newline="") as f:
        reader = csv.reader(f, delimiter=",", strict=True)

        try:
            header = next(reader, None)

            if not header:
                raise ValueError("Пустой CSV или отсутствует заголовок")

            names = []

            for name in header:
                if not name.strip():
                    raise ValueError("Название колонки не должно быть пустым")

                if name in names:
                    raise ValueError("Названия колонок не должны повторяться")

                names.append(name)

            for row in reader:
                if len(row) != len(header):
                    raise ValueError("Количество полей не совпадает с заголовком")

        except csv.Error as error:
            raise ValueError("Некорректный CSV") from error

        f.seek(0)
        reader = csv.reader(f, delimiter=",", strict=True)
        next(reader)

        json_path.parent.mkdir(parents=True, exist_ok=True)

        with json_path.open("w", encoding="utf-8") as out:
            out.write("[")
            first = True

            for row in reader:
                if not first:
                    out.write(",")

                out.write("\n  {")

                for i in range(len(header)):
                    if i > 0:
                        out.write(",")

                    out.write("\n    ")
                    json.dump(header[i], out, ensure_ascii=False, indent=2)
                    out.write(": ")
                    json.dump(row[i], out, ensure_ascii=False, indent=2)

                out.write("\n  }")
                first = False

            if not first:
                out.write("\n")

            out.write("]")