altura = float(input("Digiyete a sua altura: "))
altura = altura * 100

print(f"Sua altura é de {altura} cm")

nome = "Daniel"
idade = 16

texto = "Meu nome é {} e tenho {} anos".format(nome, idade)
texto = "Meu nome é {n} e tenho {i} anos".format(n=nome, i=idade)
textp = "Meu nome é %s e tenho %d anos" % (nome, idade)
print(texto)