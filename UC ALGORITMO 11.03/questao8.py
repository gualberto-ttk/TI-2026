valor_compra = float(input("Digite o valor da compra: "))

if valor_compra < 100:
    desconto = 0
elif valor_compra < 500:
    desconto = valor_compra * 0.05
elif valor_compra < 1000:
    desconto = valor_compra * 0.10
else:
    desconto = valor_compra * 0.15

valor_final = valor_compra - desconto

print("Valor original:", valor_compra)
print("Desconto aplicado:", desconto)
print("Valor final da compra:", valor_final)