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
    
    return ' '.join(words)


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

    return tokens


def count_freq(tokens: list[str]) -> dict[str, int]:
    freq = {}    
    for token in tokens:
        if token in freq:
            freq[token] += 1
        else:
            freq[token] = 1
    
    return freq 


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
