def soma_segura(a, b):
    try:
        # tenta somar os dois valores
        soma = a + b
        return soma
    except TypeError:
        # caso não sejam números válidos
        print("Entrada inválida")
        return 0


def divisao(x, y):
    try:
        # tenta fazer a divisão
        resultado = x / y
        return resultado
    except ZeroDivisionError:
        # caso tente dividir por zero
        return "Não divida por zero!"