resposta = input("Você tem carteira de motorista? (S/N): ")

if resposta.lower() == "s":
    carteira = True
else:
    carteira = False

print("\nValor booleano:", carteira)
print("Tipo da variável:", type(carteira))