COMPRAS = ["arroz", "feijão", "macarrão", "leite", "pão"]

print("Lista de compras atual:")
for item in COMPRAS:
    print("-", item)

novo_item = input("\nDigite um novo item para adicionar à lista: ")

COMPRAS.append(novo_item)

print("\nLista de compras atualizada:")
for item in COMPRAS:
    print("-", item)