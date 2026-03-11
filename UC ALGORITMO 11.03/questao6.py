idade = int(input("Digite a sua idade: "))

if idade < 12:
    categoria = "Infantil"
elif idade >= 12 and idade < 18:
    categoria = "Juvenil"
elif idade >= 18 and idade < 60:
    categoria = "Adulto"
else:
    categoria = "Sênior"

print("Categoria:", categoria)
print("Bem-vindo à competição de natação!")