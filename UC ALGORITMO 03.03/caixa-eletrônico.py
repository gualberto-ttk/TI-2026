senha_correta = "123456"

for i in range(3):
    senha = input()
    if senha == senha_correta:
        print("Olá, usuário. Seja bem-vindo ao nosso banco!")
        break
    elif i == 0:
        print("Senha incorreta! Você ainda tem 2 tentativas.")
    elif i == 1:
        print("Senha incorreta! Você ainda tem 1 tentativa.")
    else:
        print("Sua senha foi bloqueada! Por favor, dirija-se a um de nossos caixas.")