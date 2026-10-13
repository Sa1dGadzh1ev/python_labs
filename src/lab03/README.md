# ЛАБОРАТОРНАЯ РАБОТА №3: ТЕКСТЫ И ЧАСТОТЫ СЛОВ

**Выполнил:** Гаджиев Саид БИВТ-26-6-3

---

## ЗАДАНИЕ A: РЕАЛИЗАЦИЯ ЧИСТЫХ АЛГОРИТМОВ (Модуль src/lib/text.py)

### ФУНКЦИЯ 1: normalize (Нормализация текста)

Создаём функцию для очистки текста. Сначала переводим всю строку в нижний регистр. Затем запускаем ручной цикл `for` по каждому символу: если видим букву "ё", меняем её на "е" (и "Ё" на "Е"). Если видим невидимые символы переноса строк `\n`, возврата каретки `\r` или табуляции `\t`, превращаем их в обычные пробелы. В конце ручным перебором букв избавляемся от лишних повторяющихся пробелов и склеиваем слова ровно через один пробел, автоматически обрезая края.

```python
def normalize(text: str, *, casefold: bool = True, yo2e: bool = True) -> str:
    if casefold:
        text = text.casefold()
    cleaned_chars = []
    for char in text:
        if yo2e and char == 'ё':
            cleaned_chars.append('е')
        elif yo2e and char == 'Ё':
            cleaned_char.append('Е')
        elif char in ('\t', '\n', '\r'):
            cleaned_chars.append(' ')
        else:
            cleaned_chars.append(char)
    temp_text = ''.join(cleaned_chars)
    words = []
    current_word = []
    for char in temp_text:
        if char == ' ':
            if current_word:
                words.append(''.join(current_word))
                current_word = []
        else:
            current_word.append(char)
    if current_word:
        words.append(''.join(current_word))
    
    return ' '.join(words)```
(../../images/lab03/task01.png)
---

### ФУНКЦИЯ 2: tokenize (Разбиение строки на токены)

Функция нарезает очищенный текст на список отдельных слов. Мы бежим указателем `i` по строке в цикле `while`. Наш кастомный алфавит (строка `valid_chars`) помогает понять, что перед нами разрешённая буква, цифра или подчёркивание. Если натыкаемся на дефис, мы заглядываем на один символ вперёд: если там идёт буква (как в слове "по-настоящему"), то мы считаем дефис частью слова и идём дальше. Если там пробел, знак препинания или другой дефис — слово закончилось, и мы делаем срез. Все эмодзи и грязь выпадают автоматически.

```python
def tokenize(text: str) -> list[str]:

    valid_chars = "abcdefghijklmnopqrstuvwxyz" \
                  "абвгдеёжзийклмнопрстуфхцчшщъыьэюя" \
                  "0123456789_"

    tokens = []
    ln = len(text)
    i = 0

    while i < ln:
        if text[i] not in valid_chars:
            i += 1
            continue

        start = i
        while i < ln:
            if text[i] in valid_chars:
                i += 1
            elif text[i] == '-':
                if i + 1 < ln and text[i+1] in valid_chars:
                    i += 2
                else:
                    break
            else:
                break
    

        tokens.append(text[start:i])

    return tokens```
(../../images/lab03/task02.png)
---

### ФУНКЦИЯ 3: count_freq (Подсчёт частоты слов)

Функция считает, сколько раз каждое слово встретилось в тексте. Заводим пустой словарь-блокнот. Перебираем слова из списка токенов по очереди: если слово уже есть в блокноте, мы увеличиваем его счётчик частоты на единицу (`+= 1`). Если слова ещё не было — создаём для него новую ячейку в словаре со значением 1.

```python
def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}    
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    
    return freq ```
(../../images/lab03/task03.png)
---

### ФУНКЦИЯ 4: top_n (Рейтинг слов и Тай-брейк)

Сортируем слова по рейтингу без использования готовых методов сортировки Python. Применяем честный алгоритм "Пузырька" (Bubble Sort) с двойным циклом. Главный критерий — у кого частота больше, тот летит вверх списка (влево). Если частоты абсолютно одинаковые (ситуация тай-брейка), включается второе условие: мы сравниваем строки по алфавиту, чтобы слова на букву "А" вставали выше слов на букву "Я". В конце через развёрнутое безопасное условие `limit` отрезаем ровно N элементов, защищая программу от вылета за границы списка, если слов в тексте меньше, чем запрошенный топ.

```python
def top_n(freq: dict[str, int], n: int = 5) -> list[tuple[str, int]]:

    
    items = list(freq.items())
    num_items = len(items)

    for i in range(num_items):
        for j in range(0, num_items - i -1):
            left_word, left_count = items[j]
            right_word, right_count = items[j+1]

            swap = False

            if left_count < right_count:
                swap = True

            elif left_count == right_count:
                if left_word > right_word:
                    swap = True
            
            if swap:
                items[j], items[j+1] = items[j+1], items[j]

    result = []

    if n < num_items:
        limit = n
    else:
        limit = num_items

    for k in range(limit):
        result.append(items[k])

    return result
```

(../../images/lab03/task03.png)
---
# ЗАДАНИЕ B: РАБОТА СО STDIN И ИНТЕРФЕЙС (Скрипт src/lab03/text_stats.py)

Скрипт считывает поток данных целиком с помощью функции `sys.stdin.read()`, что позволяет передавать в программу многострочные тексты любой длины через терминал Юникс-систем. Скрипт связывает наши алгоритмы с консолью и поддерживает два режима вывода через глобальный переключатель `TABLE_MODE`.

```python
import sys
sys.path.append('src')

from lib.text import normalize, tokenize, count_freq, top_n

TABLE_MODE = True

def main():
    input_text = sys.stdin.read()
    
    norm_text = normalize(input_text)
    tokens = tokenize(norm_text)
    freq_dict = count_freq(tokens)
    top_5 = top_n(freq_dict, n=5)
    
    total_words = len(tokens)
    unique_words = len(freq_dict)
    
    print(f"Всего слов: {total_words}")
    print(f"Уникальных слов: {unique_words}")
    print("Топ-5:")
    
    if not top_5:
        return

    if not TABLE_MODE:
        for word, count in top_5:
            print(f"{word}:{count}")
    else:
        max_word_len = len("слово")  # Базовая ширина под шапку "слово" (5 букв)
        for word, _ in top_5:
            if len(word) > max_word_len:
                max_word_len = len(word)
                
        print(f"{'слово':<{max_word_len}} | частота")
        print("-" * max_word_len + "-+--------")
        
        for word, count in top_5:
            print(f"{word:<{max_word_len}} | {count}")

if __name__ == "__main__":
    main()

```

### Тест №1: Проверка базового текстового формата вывода (TABLE_MODE = False)
`TABLE_MODE` была переведена в состояние `False`. В программу через терминал с помощью одинарных кавычек был передан текст с ловушками на регистр, буквы Ё, внутренние дефисы и одинаковую частоту:

```bash
echo 'Питон — это круто! Питон по-настоящему крут, а ёжик учит питон. Круто!' | python3 src/lab03/text_stats.py
```

(../../images/lab03/task05.png)

### Тест №2: Дополнительный табличный формат вывода со звёздочкой (TABLE_MODE = True)
Константа `TABLE_MODE` переведена в состояние `True`. Программа динамически вычисляет длину самого длинного слова в Топ-5 (`max_word_len`), чтобы задать фиксированную ширину первой колонки. С помощью форматирования f-строк со знаком `<` все слова выравниваются по левому краю, благодаря чему разделительные палочки `|` выстраиваются идеально ровно друг под другом.

```bash
echo 'Питон — это круто! Питон по-настоящему крут, а ёжик учит питон. Круто!' | python3 src/lab03/text_stats.py
```
(../../images/lab03/task06.png)
