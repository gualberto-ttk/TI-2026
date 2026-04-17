p = float(input())
a = float(input())

i = p / (a * a)

if i < 18.5:
    print("magro")
elif i <= 24.9:
    print("normal")
else:
    print("acima")