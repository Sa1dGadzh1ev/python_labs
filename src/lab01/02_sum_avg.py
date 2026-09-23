a_str = input("a: ").replace(",", ".")
b_str = input("b: ").replace(",", ".")
a = float(a_str)
b = float(b_str)
total_sum = a + b
avg = total_sum / 2
print(f"sum={total_sum:.2f}; avg={avg:.2f}")

