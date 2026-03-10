matricula1 = 2026001
nome1 = "Ana Silva"
telefone1 = "9999-8888"

aluno = {
    "matricula": 2026001,
    "nome": "Ana Silva",
    "telefone": "9999-8888"
}

print(aluno)

contato = {
    "@camilaqueiroz": "Camila Queiroz",
    "@brunamarquezine": "Bruna M.",
    "@sheronmenezes": "Sheron M.",
    "@paolaoliveira": "Paola O."

}

print(contato)
print(type(contato))

print(contato["@camilaqueiroz"])

print(contato.get("@paolaoliveira"))
print(contato.get("@inexistente"))
print(contato.get("@inexistente", "Não encontrato"))

contato["@giovanna"] = "Giovanna"
print("Após add: ", contato)

contato["@paolaoliveira"] = "Paola Oliveira"
print("Após add: ", contato)

contato.update({
    "@brunamarquezine": "Bruna Marquezine",
    "@camilaqueiroz": "Camila Q."
})

print("Após atualização ", contato)

removido = contato.pop ("@paolaoliveira")
print(f"Removido: {removido}")
print("Após o pop: ", contato)

del contato["@camilaqueiroz"]
print("Após o del: ", contato)

copia = dict(contato)
contato.clear()
print("Após clear: ", contato)
print("Cópia: ", copia)

print("Número de contato: ", len(contato))

if "@joao" in contato:
    print(f"Encontrato: {contato['joao']}")

if "@inexistente" in contato:
    print("Existe")

else:
    print("Não existe.")