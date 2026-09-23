time = int(input("Минуты: "))
hour = time//60
minute = time%60
print(f"{hour}:{minute:02d}")