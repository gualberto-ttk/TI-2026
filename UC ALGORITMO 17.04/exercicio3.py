total = 0
v = float(input("valor (0 para parar): "))

while v != 0:
    total += v
    v = float(input("valor (0 para parar): "))

print("total:", total)