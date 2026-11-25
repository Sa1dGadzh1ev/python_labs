import multiprocessing
import random
import timeit
from collections.abc import Callable
from multiprocessing.connection import Connection

from src.lab04.io_txt_csv import write_csv
from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort

SORT_LIMIT = 60
Row = tuple[str, int, str, str]


def add_row(rows: list[Row], task: str, n: int, impl: str, seconds: float | None) -> None:
    duration = f"> {SORT_LIMIT}" if seconds is None else f"{seconds:.6f}"
    rows.append((task, n, impl, duration))


def measure_sort(fn: Callable, data: list[int], sender: Connection) -> None:
    """Замерить одну сортировку в дочернем процессе и передать секунды."""
    with sender:
        sender.send(timeit.timeit(lambda: fn(data), number=1))


def measure_sort_with_limit(fn: Callable, data: list[int]) -> float | None:
    """Остановить сортировку, если она не успела прислать результат."""
    context = multiprocessing.get_context("spawn")
    receiver, sender = context.Pipe(duplex=False)

    with receiver, sender:
        process = context.Process(target=measure_sort, args=(fn, data, sender))
        process.start()
        sender.close()

        try:
            if receiver.poll(SORT_LIMIT):
                seconds = receiver.recv()
            else:
                process.terminate()
                seconds = None
        except BaseException:
            process.terminate()
            raise
        finally:
            process.join()
            process.close()

    return seconds


def bench_sorts(n: int) -> list[Row]:
    lo, hi = -10_000, 10_000
    data = [random.randint(lo, hi) for _ in range(n)]
    rows = []

    seconds = timeit.timeit(lambda: sorted(data), number=1)
    add_row(rows, "sort", n, "sorted", seconds)

    for fn in (bubble_sort, insertion_sort, selection_sort):
        if n == 100_000:
            seconds = measure_sort_with_limit(fn, data)
        else:
            seconds = timeit.timeit(lambda: fn(data), number=1)

        add_row(rows, "sort", n, fn.__name__, seconds)

    return rows


def bench_search() -> list[Row]:
    n = 100_000
    data = [random.randrange(1_000_000) for _ in range(n)]
    queries = [random.choice(data) for _ in range(5_000)]
    queries.extend(random.randint(-1_000_000, -1) for _ in range(5_000))
    random.shuffle(queries)

    def run_queries(fn: Callable, nums: list[int]) -> None:
        for query in queries:
            fn(nums, query)

    rows = []
    seconds = timeit.timeit(lambda: run_queries(linear_search, data), number=1)
    add_row(rows, "search", n, "linear_search", seconds)

    seconds = timeit.timeit(lambda: sorted(data), number=1)
    add_row(rows, "search_prepare", n, "sorted", seconds)

    ordered = sorted(data)
    seconds = timeit.timeit(lambda: run_queries(binary_search, ordered), number=1)
    add_row(rows, "search", n, "binary_search", seconds)

    return rows


def bench_two_sum(n: int) -> list[Row]:
    data = [random.randrange(1_000_000) for _ in range(n - 2)]
    data.extend([-2, -3])
    target = -5
    rows = []

    for fn in (two_sum_brute, two_sum_fast):
        seconds = timeit.timeit(lambda: fn(data, target), number=1)
        add_row(rows, "two_sum", n, fn.__name__, seconds)

    return rows


def main() -> None:
    random.seed(42)
    rows = []

    for n in (1_000, 10_000, 100_000):
        rows.extend(bench_sorts(n))

    rows.extend(bench_search())

    for n in (1_000, 10_000):
        rows.extend(bench_two_sum(n))

    header = ("task", "n", "impl", "seconds")
    path = "data/lab07/bench.csv"
    write_csv(rows, path, header=header)

    print(f"{header[0]:<14} {header[1]:>7}  {header[2]:<16} {header[3]:>10}")
    print("-" * 51)
    for task, n, impl, seconds in rows:
        print(f"{task:<14} {n:>7}  {impl:<16} {seconds:>10}")

    print(f"\nCSV: {path}")


if __name__ == "__main__":
    main()
