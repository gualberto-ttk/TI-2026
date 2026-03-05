numeros = [80, 20, 30, 20, 40, 90, 50]

print("Lista:", numeros)

print("Quantidade de elementos:", len(numeros))

print("Quantidade de vezes que aparece 20:", numeros.count(20))

print("Posição do número 30:", numeros.index(30))

print("O número 100 está na lista?", 100 in numeros)


import random

numeros = [91, 34, 67, 15, 82]

print("Lista original:", numeros)

numeros.sort()
print("Ordem crescente:", numeros)

numeros.sort(reverse=True)
print("Ordem decrescente:", numeros)

numeros3 = [6, 7, 8, 9, 10]

random.shuffle(numeros3)
print("Lista embaralhada:", numeros3)

lista = [4, 12, 7, 20, 3, 15]

lista.sort()
print("Crescente:", lista)

lista.sort(reverse=True)
print("Decrescente:", lista)

random.shuffle(lista)
print("Embaralhada:", lista)