def linear_search(nums: list[int], x: int) -> int:
    """Вернуть индекс первого вхождения x или -1."""
    for index, value in enumerate(nums):
        if value == x:
            return index

    return -1


def binary_search(sorted_nums: list[int], x: int) -> int:
    """Вернуть индекс любого вхождения x или -1.

    Список должен быть отсортирован по возрастанию.
    На неотсортированном списке результат не определён.
    """
    lo = 0
    hi = len(sorted_nums) - 1

    while lo <= hi:
        mid = (lo + hi) // 2
        value = sorted_nums[mid]

        if value == x:
            return mid
        if value < x:
            lo = mid + 1
        else:
            hi = mid - 1

    return -1


def two_sum_brute(nums: list[int], target: int) -> tuple[int, int] | None:
    """Перебрать пары индексов i < j и вернуть пару с заданной суммой."""
    for i in range(len(nums) - 1):
        for j in range(i + 1, len(nums)):
            if nums[i] + nums[j] == target:
                return i, j

    return None


def two_sum_fast(nums: list[int], target: int) -> tuple[int, int] | None:
    """Найти пару индексов i < j за один проход со словарём."""
    seen: dict[int, int] = {}

    for j, value in enumerate(nums):
        needed = target - value
        if needed in seen:
            return seen[needed], j

        seen[value] = j

    return None
