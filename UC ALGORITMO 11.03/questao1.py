salario_base = 3500.00
bonus = 800.00
desconto = 250.00

salario_bruto = salario_base + bonus
salario_liquido = salario_bruto - desconto

print("Salário bruto:", salario_bruto)
print("Salário líquido:", salario_liquido)

print("Tipo de salario_base:", type(salario_base))
print("Tipo de bonus:", type(bonus))
print("Tipo de desconto:", type(desconto))
print("Tipo de salario_bruto:", type(salario_bruto))
print("Tipo de salario_liquido:", type(salario_liquido))