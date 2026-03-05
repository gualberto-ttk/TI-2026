nomes = ["Ana", "Bruno", "Carlos", "Diana"]
print("Nomes:", nomes)

nomes.remove ("Ana")
print ("Lista atualizada: ", nomes)

removido = nomes.pop(1)
print(f"Removido: {removido}")
print("Apos pop(): ", nomes)

del nomes[0]
print("Após del nome[0] ", nomes)

nomes.clear()
print("Lista atualizada: ", nomes)