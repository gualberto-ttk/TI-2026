def rank_jogador(pontos, derrotas):
    pontos = pontos - derrotas*10  # tira pontos

    if pontos < 0:
        return "Banido"
    if pontos < 100:
        return "Bronze"
    if pontos < 300:
        return "Prata"
    if pontos < 600:
        return "Ouro"
    return "Diamante"


def saldo_final(saldo, saque):
    if saque > saldo:
        return "Saldo insuficiente"

    if saque > 1000:
        saque = saque * 1.02  # taxa simples

    return saldo - saque


def tipo_magia(fogo, agua):
    if fogo and agua:
        return "Vapor"
    if fogo:
        return "Fogo"
    if agua:
        return "Água"
    return "Sem magia"


def pontuacao_total(pontos, tempo):
    if tempo < 30:
        pontos = pontos + 50
    if tempo > 100:
        pontos = pontos - 20

    if pontos > 200:
        return "Recorde"

    return pontos


def verificar_acesso(usuario, senha, tentativas):
    if tentativas >= 3:
        return "Bloqueado"

    if usuario == "admin":
        if senha == "1234":
            return "Acesso total"
        else:
            return "Senha incorreta"

    return "Usuário inválido"


def lancar_foguete(combustivel, clima, sistema_ok):
    if combustivel < 100:
        return "Combustível insuficiente"

    if clima != "bom":
        return "Clima desfavorável"

    if sistema_ok == False:
        return "Falha no sistema"

    return "Lançamento autorizado"