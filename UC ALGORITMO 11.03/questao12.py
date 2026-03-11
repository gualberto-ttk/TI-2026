total = 0
quantidade = 0

while True:
    deposito = float(input("Digite o valor do depósito (0 para encerrar): "))
    
    if deposito == 0:
        break
    
    total += deposito
    quantidade += 1

print("Total depositado:", total)
print("Quantidade de depósitos:", quantidade)