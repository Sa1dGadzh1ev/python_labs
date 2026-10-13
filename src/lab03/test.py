import sys
sys.path.append('src')

from lib.text import normalize, tokenize, count_freq, top_n

print("normalize")
print(f"{"ПрИвЕт\nМИр\t"} -> {normalize("ПрИвЕт\nМИр\t")}")
print(f"{"ёжик, Ёлка"} -> {normalize("ёжик, Ёлка")}")
print(f"{"Hello\r\nWorld"} -> {normalize("Hello\r\nWorld")}")
print(f"{"  двойные   пробелы  "} -> {normalize("  двойные   пробелы  ")}")

print("\ntokenize")
print(f"{"привет мир"} -> {tokenize("привет мир")}")
print(f"{"hello,world!!!"} -> {tokenize("hello,world!!!")}")
print(f"{"по-настоящему круто"} -> {tokenize("по-настоящему круто")}")
print(f"{"2025 год"} -> {tokenize("2025 год")}")
print(f"{"emoji 😀 не слово"} -> {tokenize("emoji 😀 не слово")}")

print("\ncount_freq + top_n")
case1 = count_freq(["a","b","a","c","b","a"])
print(f"{["a","b","a","c","b","a"]} -> {case1}")
print(f"n=2: {top_n(case1, n=2)}")
case2 = count_freq(["bb","aa","bb","aa","cc"])
print(f"{["bb","aa","bb","aa","cc"]} -> {case2}")
print(f"n=2: {top_n(case2, n=2)}")