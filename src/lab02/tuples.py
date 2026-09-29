def format_record(rec: tuple[str, str, float]) -> str:
    if len(rec) != 3:
        raise ValueError("Запись должна содержать ровно 3 элемента")
    fio, group, gpa = rec 

    if not isinstance(fio, str) or not isinstance(group, str):
        raise TypeError("ФИО и группа должны быть строками")
    if not fio.strip() or not group.strip():
        raise ValueError("ФИО и группа не могут быть пустыми")
    if not isinstance(gpa, (int, float)):
        raise TypeError("GPA должен быть числом")


    words = fio.split() 
    if not words:
        raise ValueError("ФИО не содержит слов")
    
    last_name = words[0].capitalize() 

    initials = "".join([word[0].upper() + "." for word in words[1:]])
    
    return f"{last_name} {initials}, гр. {group.strip()}, GPA {gpa:.2f}"



if __name__ == "__main__":
    print("ТЕСТИРОВАНИЕ TUPLES")
    print("П1:", format_record(("Иванов Иван Иванович", "BIVT-25", 4.6)))
    print("П2:", format_record(("Петров Пётр", "ИКВО-12", 5.0)))
    print("П3:", format_record(("Петров Пётр Петрович", "ИКВО-12", 5.0)))
    print("П4:", format_record(("  сидорова анна   сергеевна ", "ABB-01", 3.999)))
    
    print("ТЕСТИРОВАНИЕ ОШИБОК")
    try:
        print("Тест на пустое ФИО:")
        format_record(("", "BIVT-25", 4.5))
    except ValueError as e:
        print(f" ValueError: {e}")
        
    try:
        print("Тест на неверный тип GPA:")
        format_record(("Иванов И.И.", "BIVT-25", "отлично"))
    except TypeError as e:
        print(f" TypeError: {e}")