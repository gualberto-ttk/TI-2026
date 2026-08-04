import json
import os
import uuid
from datetime import datetime

import groq
from dotenv import load_dotenv
from groq import Groq

from flask import Blueprint, flash, jsonify, redirect, render_template, request, session, url_for

central_bp = Blueprint("central", __name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_PROGRESSO = os.path.join(BASE_DIR, "data", "progresso.json")

load_dotenv(os.path.join(BASE_DIR, ".env"))

GROQ_MODEL = os.environ.get("GROQ_MODEL", "llama-3.3-70b-versatile")
ASSISTENTE_INSTRUCOES = """
Você é o EstudeBot, assistente virtual educacional do Estude+.
Responda em português do Brasil, a menos que o aluno peça outro idioma.
Ajude com qualquer pergunta permitida: matérias escolares, explicações, exercícios,
resumos, redação, programação, organização, carreira e dúvidas gerais.
Use linguagem clara, correta e adequada ao nível do aluno.
Quando houver cálculo, mostre as etapas. Quando não souber ou faltar contexto,
diga isso claramente e peça a informação necessária.
Não invente fatos, fontes ou resultados. Evite respostas excessivamente longas,
mas aprofunde quando o aluno pedir.
""".strip()

NIVEIS = [
    ("Iniciante", 0, "fa-seedling"),
    ("Aprendiz", 150, "fa-book-open"),
    ("Estudante", 500, "fa-graduation-cap"),
    ("Especialista", 1200, "fa-medal"),
    ("Mestre", 2500, "fa-crown"),
    ("Lenda", 5000, "fa-trophy"),
]

RECOMPENSAS = [
    {"id": "tema-oceano", "nome": "Tema Oceano", "preco": 120, "icone": "fa-water", "descricao": "Cores azuis para personalizar o Estude+."},
    {"id": "tema-floresta", "nome": "Tema Floresta", "preco": 150, "icone": "fa-tree", "descricao": "Cores verdes para a plataforma."},
    {"id": "moldura-dourada", "nome": "Moldura Dourada", "preco": 300, "icone": "fa-certificate", "descricao": "Moldura especial para o perfil."},
    {"id": "titulo-dedicado", "nome": "Título Dedicado", "preco": 220, "icone": "fa-star", "descricao": "Título especial para seu perfil."},
    {"id": "som-chuva", "nome": "Som de Chuva", "preco": 80, "icone": "fa-cloud-rain", "descricao": "Som ambiente para o modo Focus."},
    {"id": "som-floresta", "nome": "Som de Floresta", "preco": 100, "icone": "fa-leaf", "descricao": "Som natural para suas sessões."},
]

def _ler():
    try:
        with open(ARQUIVO_PROGRESSO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"usuarios": {}}
    dados.setdefault("usuarios", {})
    return dados

def _salvar(dados):
    os.makedirs(os.path.dirname(ARQUIVO_PROGRESSO), exist_ok=True)
    temporario = ARQUIVO_PROGRESSO + ".tmp"
    with open(temporario, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=2)
    os.replace(temporario, ARQUIVO_PROGRESSO)

def _usuario_padrao():
    return {
        "xp": 0,
        "moedas": 0,
        "sessoes": [],
        "recompensas": [],
        "historico_chat": [],
        "carreira": None,
    }

def _usuario(dados):
    email = session.get("email")
    usuario = dados["usuarios"].setdefault(email, _usuario_padrao())
    for chave, valor in _usuario_padrao().items():
        usuario.setdefault(chave, valor.copy() if isinstance(valor, list) else valor)
    return usuario

def _exigir_login():
    if not session.get("email"):
        flash("Entre na sua conta para acessar este recurso.", "danger")
        return redirect(url_for("login"))
    return None

def _nivel(xp):
    atual = NIVEIS[0]
    proximo = None
    for indice, item in enumerate(NIVEIS):
        if xp >= item[1]:
            atual = item
            proximo = NIVEIS[indice + 1] if indice + 1 < len(NIVEIS) else None
    if proximo:
        faixa = max(proximo[1] - atual[1], 1)
        progresso = int(((xp - atual[1]) / faixa) * 100)
        faltam = max(proximo[1] - xp, 0)
    else:
        progresso, faltam = 100, 0
    return {
        "nome": atual[0], "xp_minimo": atual[1], "icone": atual[2],
        "proximo": proximo[0] if proximo else None,
        "progresso": max(0, min(progresso, 100)), "faltam": faltam,
    }

def _evolucao(usuario):
    sessoes = usuario.get("sessoes", [])
    minutos = sum(int(item.get("minutos", 0)) for item in sessoes)
    por_disciplina = {}
    por_dia = {}
    for item in sessoes:
        disciplina = item.get("disciplina") or "Estudo geral"
        por_disciplina[disciplina] = por_disciplina.get(disciplina, 0) + int(item.get("minutos", 0))
        dia = item.get("data", "")
        por_dia[dia] = por_dia.get(dia, 0) + int(item.get("minutos", 0))
    favorita = max(por_disciplina, key=por_disciplina.get) if por_disciplina else "Nenhuma ainda"
    return {
        "minutos": minutos,
        "horas": round(minutos / 60, 1),
        "sessoes": len(sessoes),
        "favorita": favorita,
        "por_disciplina": por_disciplina,
        "por_dia": por_dia,
        "ultimas": sorted(sessoes, key=lambda x: x.get("data_iso", ""), reverse=True)[:8],
    }

def _montar_historico_ia(historico, mensagem):
    itens = []

    for item in historico[-8:]:
        pergunta = str(item.get("pergunta", "")).strip()
        resposta = str(item.get("resposta", "")).strip()

        if pergunta:
            itens.append({"role": "user", "content": pergunta[:4000]})

        if resposta:
            itens.append({"role": "assistant", "content": resposta[:6000]})

    itens.append({"role": "user", "content": mensagem[:8000]})
    return itens

def _resposta_chat_ia(mensagem, historico):
    chave = os.environ.get("GROQ_API_KEY", "").strip()

    if not chave:
        raise RuntimeError(
            "A chave GROQ_API_KEY ainda não foi configurada no servidor."
        )

    cliente = Groq(
        api_key=chave,
        timeout=45.0,
        max_retries=2
    )

    mensagens = [
        {
            "role": "system",
            "content": ASSISTENTE_INSTRUCOES
        }
    ]
    mensagens.extend(_montar_historico_ia(historico, mensagem))

    resposta = cliente.chat.completions.create(
        model=GROQ_MODEL,
        messages=mensagens,
        temperature=0.4,
        max_completion_tokens=1200,
        top_p=1
    )

    if not resposta.choices:
        raise RuntimeError("A IA não retornou nenhuma resposta.")

    texto = str(
        resposta.choices[0].message.content or ""
    ).strip()

    if not texto:
        raise RuntimeError("A IA não retornou uma resposta em texto.")

    return texto

def _resultado_carreira(respostas):
    texto = " ".join(str(valor).lower() for valor in respostas.values())
    pontos = {"tecnologia": 0, "saude": 0, "humanas": 0, "negocios": 0, "criatividade": 0}
    palavras = {
        "tecnologia": ["matemática", "matematica", "computador", "tecnologia", "programar", "lógica", "logica"],
        "saude": ["biologia", "saúde", "saude", "cuidar", "corpo", "animais"],
        "humanas": ["história", "historia", "geografia", "sociedade", "ensinar", "pessoas"],
        "negocios": ["empresa", "dinheiro", "liderar", "vender", "organizar", "empreender"],
        "criatividade": ["arte", "desenho", "música", "musica", "criar", "vídeo", "video"],
    }
    for area, termos in palavras.items():
        pontos[area] = sum(1 for termo in termos if termo in texto)
    area = max(pontos, key=pontos.get)
    resultados = {
        "tecnologia": ("Tecnologia e Exatas", ["Desenvolvimento de Software", "Engenharia", "Ciência de Dados", "Segurança da Informação"]),
        "saude": ("Saúde e Ciências Biológicas", ["Medicina", "Enfermagem", "Fisioterapia", "Biologia"]),
        "humanas": ("Humanas e Educação", ["Direito", "Psicologia", "História", "Pedagogia"]),
        "negocios": ("Negócios e Gestão", ["Administração", "Contabilidade", "Economia", "Marketing"]),
        "criatividade": ("Artes e Comunicação", ["Design", "Publicidade", "Arquitetura", "Audiovisual"]),
    }
    nome, carreiras = resultados[area]
    return {"area": nome, "carreiras": carreiras, "pontuacao": pontos}

@central_bp.route("/focus")
def focus():
    bloqueio = _exigir_login()
    if bloqueio:
        return bloqueio
    dados = _ler(); usuario = _usuario(dados); _salvar(dados)
    return render_template("focus.html", nivel=_nivel(usuario["xp"]), xp=usuario["xp"], moedas=usuario["moedas"])

@central_bp.route("/focus/concluir", methods=["POST"])
def concluir_focus():
    bloqueio = _exigir_login()
    if bloqueio:
        return jsonify({"sucesso": False}), 401
    payload = request.get_json(silent=True) or {}
    try:
        minutos = int(payload.get("minutos", 0))
    except (TypeError, ValueError):
        minutos = 0
    if minutos < 1 or minutos > 240:
        return jsonify({"sucesso": False, "mensagem": "Tempo inválido."}), 400
    disciplina = str(payload.get("disciplina", "Estudo geral")).strip() or "Estudo geral"
    agora = datetime.now()
    dados = _ler(); usuario = _usuario(dados)
    usuario["sessoes"].append({
        "id": uuid.uuid4().hex, "disciplina": disciplina, "minutos": minutos,
        "data": agora.strftime("%d/%m/%Y"), "horario": agora.strftime("%H:%M"), "data_iso": agora.isoformat(),
    })
    xp_ganho = max(10, round(minutos * 0.8)); moedas = max(3, minutos // 5)
    usuario["xp"] += xp_ganho; usuario["moedas"] += moedas
    _salvar(dados)
    return jsonify({"sucesso": True, "xp_ganho": xp_ganho, "moedas_ganhas": moedas, "xp": usuario["xp"], "moedas": usuario["moedas"], "nivel": _nivel(usuario["xp"])["nome"]})

@central_bp.route("/evolucao")
def evolucao():
    bloqueio = _exigir_login()
    if bloqueio:
        return bloqueio
    dados = _ler(); usuario = _usuario(dados); _salvar(dados)
    return render_template("evolucao.html", evolucao=_evolucao(usuario), nivel=_nivel(usuario["xp"]), xp=usuario["xp"], moedas=usuario["moedas"])

@central_bp.route("/recompensas")
def recompensas():
    bloqueio = _exigir_login()
    if bloqueio:
        return bloqueio
    dados = _ler(); usuario = _usuario(dados); _salvar(dados)
    itens = []
    for item in RECOMPENSAS:
        copia = item.copy(); copia["adquirida"] = item["id"] in usuario["recompensas"]; itens.append(copia)
    return render_template("recompensas.html", recompensas=itens, nivel=_nivel(usuario["xp"]), xp=usuario["xp"], moedas=usuario["moedas"])

@central_bp.route("/recompensas/comprar/<recompensa_id>", methods=["POST"])
def comprar_recompensa(recompensa_id):
    bloqueio = _exigir_login()
    if bloqueio:
        return redirect(url_for("login"))
    item = next((x for x in RECOMPENSAS if x["id"] == recompensa_id), None)
    dados = _ler(); usuario = _usuario(dados)
    if not item:
        flash("Recompensa não encontrada.", "danger")
    elif recompensa_id in usuario["recompensas"]:
        flash("Você já possui essa recompensa.", "danger")
    elif usuario["moedas"] < item["preco"]:
        flash("Você ainda não possui moedas suficientes.", "danger")
    else:
        usuario["moedas"] -= item["preco"]; usuario["recompensas"].append(recompensa_id); _salvar(dados)
        flash("Recompensa desbloqueada!", "success")
    return redirect(url_for("central.recompensas"))

@central_bp.route("/chatbot")
def chatbot():
    bloqueio = _exigir_login()
    if bloqueio:
        return bloqueio
    dados = _ler(); usuario = _usuario(dados); _salvar(dados)
    return render_template("chatbot.html", historico=usuario["historico_chat"][-20:])

@central_bp.route("/chatbot/perguntar", methods=["POST"])
def perguntar_chatbot():
    bloqueio = _exigir_login()
    if bloqueio:
        return jsonify({"sucesso": False}), 401
    payload = request.get_json(silent=True) or {}
    mensagem = str(payload.get("mensagem", "")).strip()

    if not mensagem:
        return jsonify({"sucesso": False, "mensagem": "Digite uma pergunta."}), 400

    if len(mensagem) > 8000:
        return jsonify({
            "sucesso": False,
            "mensagem": "A pergunta ficou muito grande. Envie um texto menor."
        }), 400

    dados = _ler()
    usuario = _usuario(dados)

    try:
        resposta = _resposta_chat_ia(
            mensagem,
            usuario.get("historico_chat", [])
        )
    except groq.AuthenticationError:
        return jsonify({
            "sucesso": False,
            "mensagem": "A chave da Groq é inválida. Revise GROQ_API_KEY no servidor."
        }), 500
    except groq.PermissionDeniedError:
        return jsonify({
            "sucesso": False,
            "mensagem": "A chave não possui permissão para usar o modelo configurado."
        }), 403
    except groq.RateLimitError:
        return jsonify({
            "sucesso": False,
            "mensagem": "O limite gratuito da Groq foi atingido. Aguarde alguns minutos e tente novamente."
        }), 429
    except groq.APIConnectionError:
        return jsonify({
            "sucesso": False,
            "mensagem": "Não foi possível conectar à Groq. Tente novamente."
        }), 503
    except groq.APIStatusError as erro:
        print(
            "Erro da Groq:",
            erro.status_code,
            getattr(erro, "request_id", None),
            repr(erro)
        )
        return jsonify({
            "sucesso": False,
            "mensagem": "A Groq recusou a solicitação. Tente novamente em instantes."
        }), 502
    except Exception as erro:
        print("Erro no assistente virtual:", repr(erro))
        return jsonify({
            "sucesso": False,
            "mensagem": (
                str(erro)
                if isinstance(erro, RuntimeError)
                else "O assistente encontrou um erro inesperado."
            )
        }), 500

    usuario["historico_chat"].append({
        "pergunta": mensagem,
        "resposta": resposta,
        "data": datetime.now().strftime("%d/%m/%Y às %H:%M")
    })
    usuario["historico_chat"] = usuario["historico_chat"][-40:]
    _salvar(dados)
    return jsonify({"sucesso": True, "resposta": resposta})

@central_bp.route("/chatbot/limpar", methods=["POST"])
def limpar_chatbot():
    if not session.get("email"):
        return jsonify({
            "sucesso": False,
            "mensagem": "Sua sessão terminou. Entre novamente."
        }), 401
    dados = _ler()
    usuario = _usuario(dados)
    usuario["historico_chat"] = []
    _salvar(dados)
    return jsonify({
        "sucesso": True,
        "mensagem": "Conversa apagada."
    })

@central_bp.route("/carreira")
def carreira():
    bloqueio = _exigir_login()
    if bloqueio:
        return bloqueio
    dados = _ler(); usuario = _usuario(dados); _salvar(dados)
    return render_template("carreira.html", resultado=usuario.get("carreira"))

@central_bp.route("/carreira/calcular", methods=["POST"])
def calcular_carreira():
    bloqueio = _exigir_login()
    if bloqueio:
        return jsonify({"sucesso": False}), 401
    respostas = request.get_json(silent=True) or {}; resultado = _resultado_carreira(respostas)
    dados = _ler(); usuario = _usuario(dados); primeira_vez = usuario.get("carreira") is None
    usuario["carreira"] = resultado
    if primeira_vez:
        usuario["xp"] += 30; usuario["moedas"] += 10
    _salvar(dados)
    return jsonify({
        "sucesso": True,
        "resultado": resultado,
        "bonus": primeira_vez,
        "xp": usuario["xp"],
        "moedas": usuario["moedas"]
    })
