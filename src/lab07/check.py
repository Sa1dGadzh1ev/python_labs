import random
from collections.abc import Callable

from src.lab07.search import binary_search, linear_search, two_sum_brute, two_sum_fast
from src.lab07.sorting import bubble_sort, insertion_sort, selection_sort
TRIALS = 100
SORT_CASES = ([], [7], [2, 1], [1, 2], [3, -1, 3, 0, -1], [4, 4, 4, 4])
SEARCH_CASES = (
    ([], 1),
    ([5], 5),
    ([5], 4),
    ([1, 3], 1),
    ([1, 3], 3),
    ([1, 3], 2),
    ([4, -2, 7, -2], -2),
    ([4, -2, 7, -2], 8),
    ([2, 2, 2, 2], 2),
)
TWO_SUM_CASES = (
    ([], 0, False),
    ([5], 10, False),
    ([5, 5], 10, True),
    ([0, 0], 0, True),
    ([-3, 4, -2, 8], -5, True),
    ([1, 4, 6, 9], 10, True),
    ([1, 2], 10, False),
    ([2, 7, 11, 15], 9, True),
)


def check_sorting(fn: Callable[[list[int]], list[int]], trials: int = TRIALS) -> None:
    """Сравнить сортировку с sorted и проверить, что вход не изменился."""
    name = getattr(fn, "__name__", type(fn).__name__)
    cases = [list(case) for case in SORT_CASES]
    for _ in range(trials):
        n = random.randint(0, 50)
        cases.append([random.randint(-100, 100) for _ in range(n)])

    for nums in cases:
        original = list(nums)
        expected = sorted(original)
        result = fn(nums)
        context = f"{name}, вход {original}"

        assert nums == original, f"{context}: исходный список изменился на {nums}"
        assert result is not nums, f"{context}: вернулся исходный список"
        assert result == expected, f"{context}: получено {result}, ожидалось {expected}"


def index_or_missing(nums: list[int], x: int) -> int:
    try:
        return nums.index(x)
    except ValueError:
        return -1


def check_search() -> None:
    """Проверить оба поиска на общих примерах и случайных списках."""
    cases = list(SEARCH_CASES)
    for trial in range(TRIALS):
        n = random.randint(0, 50)
        nums = [random.randint(-100, 100) for _ in range(n)]
        if nums and trial % 2 == 0:
            x = random.choice(nums)
        else:
            x = random.randint(-120, 120)
        cases.append((nums, x))

    for nums, x in cases:
        expected = index_or_missing(nums, x)
        result = linear_search(nums, x)
        assert result == expected, f"linear_search({nums}, {x}): {result}, ожидалось {expected}"

        ordered = sorted(nums)
        expected = index_or_missing(ordered, x)
        result = binary_search(ordered, x)
        context = f"binary_search({ordered}, {x}): индекс {result}"

        if expected == -1:
            assert result == -1, f"{context}, ожидалось -1"
        else:
            assert isinstance(result, int) and 0 <= result < len(ordered), f"{context} вне списка"
            assert ordered[result] == x, f"{context}, по нему лежит {ordered[result]}"


def check_two_sum(trials: int = TRIALS) -> None:
    """Проверить наличие пары, границы индексов и сумму значений."""
    cases = list(TWO_SUM_CASES)
    for trial in range(trials):
        if trial % 2 == 0:
            n = random.randint(2, 50)
            nums = [random.randint(-100, 100) for _ in range(n)]
            i, j = random.sample(range(n), 2)
            cases.append((nums, nums[i] + nums[j], True))
        else:
            n = random.randint(0, 50)
            nums = [random.randint(-100, 100) for _ in range(n)]
            target = random.randint(-200, 200)
            cases.append((nums, target, None))

    for nums, target, expected in cases:
        brute = two_sum_brute(nums, target)
        fast = two_sum_fast(nums, target)
        context = f"Two Sum для {nums}, target={target}"

        assert (brute is None) == (fast is None), f"{context}: brute={brute}, fast={fast}"
        if expected is not None:
            assert (brute is not None) == expected, f"{context}: ожидалось наличие пары {expected}"

        for name, pair in (("brute", brute), ("fast", fast)):
            if pair is None:
                continue

            assert isinstance(pair, tuple) and len(pair) == 2, f"{context}, {name}: {pair}"
            i, j = pair
            assert isinstance(i, int) and isinstance(j, int), f"{context}, {name}: индексы {pair} не целые"
            assert 0 <= i < j < len(nums), f"{context}, {name}: неверные индексы {pair}"
            assert nums[i] + nums[j] == target, f"{context}, {name}: неверная сумма для {pair}"


def main() -> None:
    random.seed(42)

    sorters = (bubble_sort, insertion_sort, selection_sort)
    for fn in sorters:
        check_sorting(fn)

    check_search()
    check_two_sum()

    checks = (
        len(sorters) * (len(SORT_CASES) + TRIALS)
        + len(SEARCH_CASES) + TRIALS
        + len(TWO_SUM_CASES) + TRIALS
    )
    print(f"OK: {checks} проверок")

if __name__ == "__main__":
    main()
