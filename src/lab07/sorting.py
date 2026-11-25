def bubble_sort(nums: list) -> list:
    """Вернуть новый список, сортируя обменами соседних элементов."""
    result = list(nums)

    for end in range(len(result) - 1, 0, -1):
        for j in range(end):
            if result[j] > result[j + 1]:
                result[j], result[j + 1] = result[j + 1], result[j]

    return result


def insertion_sort(nums: list) -> list:
    """Вернуть новый список, вставляя элементы в отсортированную часть."""
    result = list(nums)

    for i in range(1, len(result)):
        value = result[i]
        j = i - 1

        while j >= 0 and result[j] > value:
            result[j + 1] = result[j]
            j -= 1

        result[j + 1] = value

    return result


def selection_sort(nums: list) -> list:
    """Вернуть новый список, выбирая на каждом шаге минимум остатка."""
    result = list(nums)

    for i in range(len(result) - 1):
        min_index = i

        for j in range(i + 1, len(result)):
            if result[j] < result[min_index]:
                min_index = j

        if min_index != i:
            result[i], result[min_index] = result[min_index], result[i]

    return result
