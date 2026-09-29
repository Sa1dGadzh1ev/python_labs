def min_max(nums: list[float | int]) -> tuple[float | int, float | int]:
    if not nums:
        raise ValueError("Список не должен быть пустым")
    return min(nums), max(nums)


def unique_sorted(nums: list[float | int]) -> list[float | int]:
    return sorted(list(set(nums)))


def flatten(mat: list[list | tuple]) -> list:
    result = []
    for item in mat:
        if not isinstance(item, (list, tuple)):
            raise TypeError("Элемент матрицы должен быть списком или кортежем")
        result.extend(item)
    return result




if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ MIN_MAX")
    print("К1:", min_max([3, -1, 5, 5, 0]))            
    print("К2:", min_max([42]))                       
    print("К3:", min_max([-5, -2, -9]))               
    print("К4:", min_max([1.5, 2, 2.0, -3.1]))         
    try:
        print("К5 (ошибка):")
        min_max([])                                       
    except ValueError as e:
        print(f"  Найдена ошибка: {e}")

    print("ТЕСТИРОВАНИЕ UNIQUE_SORTED")
    print("К1:", unique_sorted([3, 1, 2, 1, 3]))      
    print("К2:", unique_sorted([]))                   
    print("К3:", unique_sorted([-1, -1, 0, 2, 2]))    
    print("К4:", unique_sorted([1.0, 1, 2.5, 2.5, 0])) 

    print("ТЕСТИРОВАНИЕ FLATTEN")
    print("К1:", flatten([[1, 2], [3, 4]]))          
    print("К2:", flatten([[1, 2], (3, 4, 5)]))        
    print("К3:", flatten([[1], [], [2, 3]]))          
    try:
        print("К4 (ошибка):")
        flatten([[1, 2], "ab"])                           
    except TypeError as e:
        print(f"  Найдена ошибка: {e}")