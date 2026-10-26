import csv
from pathlib import Path


def read_text(path: str | Path, encoding: str = "utf-8") -> str:
    """Прочитать файл целиком и вернуть одну строку.
    Для другой кодировки передайте, например, encoding="cp1251".
    Ошибки FileNotFoundError и UnicodeDecodeError не перехватываются.
    """
    with open(path, "r", encoding=encoding) as file:
        text = file.read()

    return text


def ensure_parent_dir(path: str | Path) -> None:
    """Создать родительские папки файла, если их нет."""
    file_path = Path(path)
    parent_dir = file_path.parent

    parent_dir.mkdir(parents=True, exist_ok=True)


def write_csv(rows: list[tuple | list], path: str | Path, header: tuple[str, ...] | None = None,) -> None:
    """Записать CSV в UTF-8 с необязательным заголовком.
    При разной длине строк или несоответствии заголовка
    вызвать ValueError до открытия файла на запись.
    """
    if len(rows) > 0:
        exlength = len(rows[0])

        for row in rows:
            if len(row) != exlength:
                raise ValueError("Строки таблицы имеют разную длину")

        if header is not None:
            if len(header) != exlength:
                raise ValueError("Длина заголовка не совпадает с длиной строк")

    ensure_parent_dir(path)

    with open(path, "w", encoding="utf-8", newline="") as file:
        writer = csv.writer(file, delimiter=",")

        if header is not None:
            writer.writerow(header)

        for row in rows:
            writer.writerow(row)
