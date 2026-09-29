def check_rectangular(mat: list[list[float | int]]):
    if not mat or not mat[0]:
        return
    expected_len = len(mat[0])
    for row in mat:
        if len(row) != expected_len:
            raise ValueError("Матрица должна быть прямоугольной")


def transpose(mat: list[list[float | int]]) -> list[list]:
    if not mat:
        return []
    check_rectangular(mat)
    return [list(col) for col in zip(*mat)]


def row_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return[]
    check_rectangular(mat)

    return[sum(row) for row in mat]


def col_sums(mat: list[list[float | int]]) -> list[float]:
    if not mat:
        return []
    check_rectangular(mat)
    
    return [sum(col) for col in zip(*mat)]












if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ TRANSPOSE")
    print("П1:", transpose([[1, 2, 3]]))          
    print("П2:", transpose([[1], [2], [3]]))      
    print("П3:", transpose([[1, 2], [3, 4]]))     
    print("П4:", transpose([]))                   
    try:
        print("П5 (ошибка):")
        transpose([[1, 2], [3]])                  
    except ValueError as e:
        print(f"  Найдена ошибка: {e}")

    print("ТЕСТИРОВАНИЕ ROW_SUMS")
    print("П1:", row_sums([[1, 2, 3], [4, 5, 6]])) 
    print("П2:", row_sums([[-1, 1], [10, -10]]))   
    print("П3:", row_sums([[0, 0], [0, 0]]))       
    try:
        print("П4 (ошибка):")
        row_sums([[1, 2], [3]])                    
    except ValueError as e:
        print(f"  Успешно поймали ошибку: {e}")

    print("ТЕСТИРОВАНИЕ COL_SUMS")
    print("П1:", col_sums([[1, 2, 3], [4, 5, 6]])) 
    print("П2:", col_sums([[-1, 1], [10, -10]]))   
    print("П3:", col_sums([[0, 0], [0, 0]]))       
    try:
        print("П4 (ошибка):")
        col_sums([[1, 2], [3]])                    
    except ValueError as e:
        print(f"  Найдена ошибка: {e}")
