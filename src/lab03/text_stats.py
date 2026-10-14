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
        max_word_len = len("слово")  
        for word, _ in top_5:
            if len(word) > max_word_len:
                max_word_len = len(word)
                
        print(f"{'слово':<{max_word_len}} | частота")
        print("-" * max_word_len + "-+--------")
        
        for word, count in top_5:
            print(f"{word:<{max_word_len}} | {count}")

if __name__ == "__main__":
    main()
