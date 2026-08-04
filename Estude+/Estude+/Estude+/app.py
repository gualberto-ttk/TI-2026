from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime
import json
import os
import uuid
import webbrowser
from threading import Timer
from central import central_bp
app = Flask(__name__)
app.register_blueprint(central_bp)
app.secret_key = os.environ.get(
    "SECRET_KEY",
    "estude_mais_2026"
)
app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO_DADOS = os.path.join(
    BASE_DIR,
    "data",
    "vagas.json"
)
ARQUIVO_CADERNOS = os.path.join(
    BASE_DIR,
    "data",
    "cadernos.json"
)

ARQUIVO_AGENDA = os.path.join(
    BASE_DIR,
    "data",
    "agenda.json"
)
PASTA_FOTOS = os.path.join(
    BASE_DIR,
    "static",
    "uploads",
    "perfis"
)
EXTENSOES = {
    "png",
    "jpg",
    "jpeg",
    "webp"
}
def ler_json(caminho, padrao):
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        return padrao


def salvar_json(caminho, dados):
    pasta = os.path.dirname(caminho)

    if pasta:
        os.makedirs(pasta, exist_ok=True)

    with open(caminho, "w", encoding="utf-8") as arquivo:
        json.dump(
            dados,
            arquivo,
            ensure_ascii=False,
            indent=2
        )


def carregar_dados():
    dados = ler_json(
        ARQUIVO_DADOS,
        {
            "series": [],
            "alunos": []
        }
    )

    dados.setdefault("series", [])
    dados.setdefault("alunos", [])

    return dados


def carregar_cadernos():
    cadernos = ler_json(
        ARQUIVO_CADERNOS,
        {}
    )

    if not isinstance(cadernos, dict):
        return {}

    return cadernos


def salvar_cadernos(cadernos):
    salvar_json(
        ARQUIVO_CADERNOS,
        cadernos
    )


def carregar_agenda():
    agenda = ler_json(
        ARQUIVO_AGENDA,
        {}
    )

    if not isinstance(agenda, dict):
        return {}

    return agenda


def salvar_agenda(agenda):
    salvar_json(
        ARQUIVO_AGENDA,
        agenda
    )


def eventos_do_usuario(agenda, email):
    eventos = agenda.setdefault(email, [])

    if not isinstance(eventos, list):
        eventos = []
        agenda[email] = eventos

    return eventos


def buscar_evento(eventos, evento_id):
    return next(
        (
            evento
            for evento in eventos
            if evento.get("id") == evento_id
        ),
        None
    )


def buscar_aluno(dados, email):
    return next(
        (
            aluno
            for aluno in dados["alunos"]
            if aluno.get("email") == email
        ),
        None
    )


def buscar_serie(dados, slug):
    return next(
        (
            serie
            for serie in dados["series"]
            if serie.get("slug") == slug
        ),
        None
    )


def buscar_anotacao(anotacoes, anotacao_id):
    return next(
        (
            anotacao
            for anotacao in anotacoes
            if anotacao.get("id") == anotacao_id
        ),
        None
    )


def login_obrigatorio():
    if not session.get("email"):
        flash(
            "Entre na sua conta para acessar o caderno.",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    return None


def foto_valida(nome):
    return (
        "." in nome
        and nome.rsplit(".", 1)[1].lower() in EXTENSOES
    )


def salvar_foto(arquivo):
    if (
        not arquivo
        or not arquivo.filename
        or not foto_valida(arquivo.filename)
    ):
        return None

    os.makedirs(
        PASTA_FOTOS,
        exist_ok=True
    )

    nome_seguro = secure_filename(
        arquivo.filename
    )

    extensao = nome_seguro.rsplit(
        ".",
        1
    )[1].lower()

    nome_arquivo = (
        f"{uuid.uuid4().hex}.{extensao}"
    )

    arquivo.save(
        os.path.join(
            PASTA_FOTOS,
            nome_arquivo
        )
    )

    return (
        f"uploads/perfis/{nome_arquivo}"
    )


def anotacao_vazia():
    return {
        "id": "",
        "titulo": "",
        "tema": "",
        "conteudo": "",
        "nota1": "",
        "nota2": "",
        "nota3": "",
        "criado_em": "",
        "atualizado_em": ""
    }


def normalizar_anotacoes(valor):
    """
    Converte automaticamente o formato antigo:

    {
        "titulo": "...",
        "tema": "...",
        ...
    }

    para o novo formato:

    [
        {
            "id": "...",
            "titulo": "...",
            ...
        }
    ]
    """

    if isinstance(valor, list):
        anotacoes = []

        for anotacao in valor:
            if not isinstance(anotacao, dict):
                continue

            anotacao.setdefault(
                "id",
                uuid.uuid4().hex
            )

            anotacao.setdefault(
                "titulo",
                ""
            )

            anotacao.setdefault(
                "tema",
                ""
            )

            anotacao.setdefault(
                "conteudo",
                ""
            )

            anotacao.setdefault(
                "nota1",
                ""
            )

            anotacao.setdefault(
                "nota2",
                ""
            )

            anotacao.setdefault(
                "nota3",
                ""
            )

            anotacao.setdefault(
                "criado_em",
                anotacao.get(
                    "atualizado_em",
                    ""
                )
            )

            anotacao.setdefault(
                "atualizado_em",
                ""
            )

            anotacoes.append(anotacao)

        return anotacoes

    if isinstance(valor, dict):
        possui_conteudo = any(
            str(valor.get(campo, "")).strip()
            for campo in [
                "titulo",
                "tema",
                "conteudo",
                "nota1",
                "nota2",
                "nota3"
            ]
        )

        if not possui_conteudo:
            return []

        data_antiga = valor.get(
            "atualizado_em",
            ""
        )

        return [
            {
                "id": uuid.uuid4().hex,
                "titulo": valor.get(
                    "titulo",
                    ""
                ),
                "tema": valor.get(
                    "tema",
                    ""
                ),
                "conteudo": valor.get(
                    "conteudo",
                    ""
                ),
                "nota1": valor.get(
                    "nota1",
                    ""
                ),
                "nota2": valor.get(
                    "nota2",
                    ""
                ),
                "nota3": valor.get(
                    "nota3",
                    ""
                ),
                "criado_em": data_antiga,
                "atualizado_em": data_antiga
            }
        ]

    return []


def separar_chave_caderno(chave):
    if "::" not in chave:
        return "", chave

    slug, disciplina = chave.split(
        "::",
        1
    )

    return slug, disciplina


def nome_serie_por_slug(dados, slug):
    serie = buscar_serie(
        dados,
        slug
    )

    if serie:
        return serie.get(
            "nome",
            slug
        )

    return slug


@app.context_processor
def usuario_contexto():
    email = session.get("email")

    if not email:
        return {
            "usuario_atual": None
        }

    return {
        "usuario_atual": buscar_aluno(
            carregar_dados(),
            email
        )
    }


@app.route("/")
def inicio():
    dados = carregar_dados()

    return render_template(
        "index.html",
        series=dados["series"]
    )


@app.route("/series")
def listar_vagas():
    dados = carregar_dados()

    return render_template(
        "vagas.html",
        series=dados["series"]
    )


@app.route("/serie/<slug>")
def detalhes_vaga(slug):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()

    serie = buscar_serie(
        dados,
        slug
    )

    if not serie:
        flash(
            "Série não encontrada.",
            "danger"
        )

        return redirect(
            url_for("listar_vagas")
        )

    return render_template(
        "detalhes.html",
        serie=serie
    )


@app.route("/minha-serie")
def minha_serie():
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()

    aluno = buscar_aluno(
        dados,
        session["email"]
    )

    if not aluno:
        session.clear()

        return redirect(
            url_for("login")
        )

    return redirect(
        url_for(
            "detalhes_vaga",
            slug=aluno["serie"]
        )
    )


@app.route(
    "/caderno/<slug>/<path:disciplina>",
    methods=["GET", "POST"]
)
def caderno(slug, disciplina):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()
    serie = buscar_serie(dados, slug)

    if (
        not serie
        or disciplina not in serie.get("disciplinas", {})
    ):
        flash(
            "Disciplina não encontrada.",
            "danger"
        )

        return redirect(
            url_for("listar_vagas")
        )

    email = session["email"]
    cadernos = carregar_cadernos()

    cadernos.setdefault(email, {})

    chave = f"{slug}::{disciplina}"

    anotacoes = normalizar_anotacoes(
        cadernos[email].get(chave, [])
    )

    cadernos[email][chave] = anotacoes

    anotacao_id = (
        request.args.get("anotacao", "").strip()
        or request.form.get("anotacao_id", "").strip()
    )

    modo = request.args.get(
        "modo",
        ""
    ).strip().lower()

    visualizando = (
        modo == "visualizar"
        and bool(anotacao_id)
    )

    anotacao_atual = None

    if anotacao_id:
        anotacao_atual = buscar_anotacao(
            anotacoes,
            anotacao_id
        )

        if not anotacao_atual:
            flash(
                "Anotação não encontrada.",
                "danger"
            )

            return redirect(
                url_for(
                    "biblioteca_disciplina",
                    slug=slug,
                    disciplina=disciplina
                )
            )

    if request.method == "POST" and visualizando:
        return redirect(
            url_for(
                "caderno",
                slug=slug,
                disciplina=disciplina,
                anotacao=anotacao_id,
                modo="visualizar"
            )
        )

    if request.method == "POST":
        titulo = request.form.get(
            "titulo",
            ""
        ).strip()

        tema = request.form.get(
            "tema",
            ""
        ).strip()

        conteudo = request.form.get(
            "conteudo",
            ""
        ).strip()

        nota1 = request.form.get(
            "nota1",
            ""
        ).strip()

        nota2 = request.form.get(
            "nota2",
            ""
        ).strip()

        nota3 = request.form.get(
            "nota3",
            ""
        ).strip()

        if not any(
            [
                titulo,
                tema,
                conteudo,
                nota1,
                nota2,
                nota3
            ]
        ):
            flash(
                "Escreva alguma informação antes de salvar.",
                "danger"
            )

        else:
            agora = datetime.now().strftime(
                "%d/%m/%Y às %H:%M"
            )

            if anotacao_atual:
                anotacao_atual["titulo"] = (
                    titulo or "Anotação sem título"
                )

                anotacao_atual["tema"] = tema
                anotacao_atual["conteudo"] = conteudo
                anotacao_atual["nota1"] = nota1
                anotacao_atual["nota2"] = nota2
                anotacao_atual["nota3"] = nota3
                anotacao_atual["atualizado_em"] = agora

                id_salvo = anotacao_atual["id"]

                flash(
                    "Anotação atualizada com sucesso!",
                    "success"
                )

            else:
                nova_anotacao = {
                    "id": uuid.uuid4().hex,
                    "titulo": (
                        titulo or "Anotação sem título"
                    ),
                    "tema": tema,
                    "conteudo": conteudo,
                    "nota1": nota1,
                    "nota2": nota2,
                    "nota3": nota3,
                    "criado_em": agora,
                    "atualizado_em": agora
                }

                anotacoes.insert(
                    0,
                    nova_anotacao
                )

                id_salvo = nova_anotacao["id"]

                flash(
                    "Anotação salva na biblioteca!",
                    "success"
                )

            cadernos[email][chave] = anotacoes
            salvar_cadernos(cadernos)

            return redirect(
                url_for(
                    "caderno",
                    slug=slug,
                    disciplina=disciplina,
                    anotacao=id_salvo,
                    modo="visualizar"
                )
            )

    salvar_cadernos(cadernos)

    if anotacao_atual:
        caderno_atual = anotacao_atual
    else:
        caderno_atual = anotacao_vazia()

    return render_template(
        "caderno.html",
        serie=serie,
        disciplina=disciplina,
        caderno=caderno_atual,
        editando=(
            bool(anotacao_atual)
            and not visualizando
        ),
        visualizando=visualizando,
        total_anotacoes=len(anotacoes)
    )

@app.route("/biblioteca")
def biblioteca():
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()
    cadernos = carregar_cadernos()

    email = session["email"]

    dados_usuario = cadernos.get(
        email,
        {}
    )

    biblioteca_materias = []

    for chave, valor in dados_usuario.items():
        slug, disciplina = separar_chave_caderno(
            chave
        )

        anotacoes = normalizar_anotacoes(
            valor
        )

        if not anotacoes:
            continue

        biblioteca_materias.append(
            {
                "slug": slug,
                "serie_nome": nome_serie_por_slug(
                    dados,
                    slug
                ),
                "disciplina": disciplina,
                "quantidade": len(anotacoes),
                "anotacoes": anotacoes
            }
        )

        dados_usuario[chave] = anotacoes

    biblioteca_materias.sort(
        key=lambda item: (
            item["disciplina"].lower(),
            item["serie_nome"].lower()
        )
    )

    cadernos[email] = dados_usuario
    salvar_cadernos(cadernos)

    return render_template(
        "biblioteca.html",
        materias=biblioteca_materias,
        disciplina_atual=None,
        serie_atual=None
    )


@app.route(
    "/biblioteca/<slug>/<path:disciplina>"
)
def biblioteca_disciplina(
    slug,
    disciplina
):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()

    serie = buscar_serie(
        dados,
        slug
    )

    if (
        not serie
        or disciplina not in serie.get(
            "disciplinas",
            {}
        )
    ):
        flash(
            "Disciplina não encontrada.",
            "danger"
        )

        return redirect(
            url_for("biblioteca")
        )

    cadernos = carregar_cadernos()

    email = session["email"]

    chave = (
        f"{slug}::{disciplina}"
    )

    anotacoes = normalizar_anotacoes(
        cadernos.get(
            email,
            {}
        ).get(
            chave,
            []
        )
    )

    cadernos.setdefault(
        email,
        {}
    )[chave] = anotacoes

    salvar_cadernos(cadernos)

    materia = {
        "slug": slug,
        "serie_nome": serie["nome"],
        "disciplina": disciplina,
        "quantidade": len(anotacoes),
        "anotacoes": anotacoes
    }

    return render_template(
        "biblioteca.html",
        materias=[materia],
        disciplina_atual=disciplina,
        serie_atual=serie
    )


@app.route(
    "/biblioteca/<slug>/<path:disciplina>/excluir/<anotacao_id>",
    methods=["POST"]
)
def excluir_anotacao(
    slug,
    disciplina,
    anotacao_id
):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    cadernos = carregar_cadernos()

    email = session["email"]

    chave = (
        f"{slug}::{disciplina}"
    )

    anotacoes = normalizar_anotacoes(
        cadernos.get(
            email,
            {}
        ).get(
            chave,
            []
        )
    )

    quantidade_anterior = len(
        anotacoes
    )

    anotacoes = [
        anotacao
        for anotacao in anotacoes
        if anotacao.get("id") != anotacao_id
    ]

    cadernos.setdefault(
        email,
        {}
    )[chave] = anotacoes

    salvar_cadernos(cadernos)

    if len(anotacoes) < quantidade_anterior:
        flash(
            "Anotação excluída.",
            "success"
        )
    else:
        flash(
            "Anotação não encontrada.",
            "danger"
        )

    return redirect(
        url_for(
            "biblioteca_disciplina",
            slug=slug,
            disciplina=disciplina
        )
    )


@app.route("/calendario")
def calendario():
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()
    agenda = carregar_agenda()
    email = session["email"]
    eventos = eventos_do_usuario(agenda, email)

    eventos.sort(
        key=lambda item: (
            item.get("data", ""),
            item.get("horario", "")
        )
    )

    aluno = buscar_aluno(dados, email)
    serie = None
    disciplinas = []

    if aluno:
        serie = buscar_serie(
            dados,
            aluno.get("serie", "")
        )

    if serie:
        disciplinas = list(
            serie.get("disciplinas", {}).keys()
        )

    agora = datetime.now()

    return render_template(
        "calendario.html",
        eventos=eventos,
        disciplinas=disciplinas,
        hoje=agora.strftime("%Y-%m-%d"),
        ano_atual=agora.year,
        mes_atual=agora.month
    )


@app.route(
    "/calendario/criar",
    methods=["POST"]
)
def criar_evento():
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    titulo = request.form.get(
        "titulo",
        ""
    ).strip()

    data = request.form.get(
        "data",
        ""
    ).strip()

    horario = request.form.get(
        "horario",
        ""
    ).strip()

    disciplina = request.form.get(
        "disciplina",
        ""
    ).strip()

    descricao = request.form.get(
        "descricao",
        ""
    ).strip()

    prioridade = request.form.get(
        "prioridade",
        "media"
    ).strip().lower()

    if prioridade not in {
        "baixa",
        "media",
        "alta"
    }:
        prioridade = "media"

    if not titulo or not data:
        flash(
            "Informe o título e a data da atividade.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    try:
        datetime.strptime(
            data,
            "%Y-%m-%d"
        )
    except ValueError:
        flash(
            "A data informada é inválida.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    agenda = carregar_agenda()
    email = session["email"]
    eventos = eventos_do_usuario(
        agenda,
        email
    )

    agora = datetime.now()

    eventos.append(
        {
            "id": uuid.uuid4().hex,
            "titulo": titulo,
            "data": data,
            "horario": horario,
            "disciplina": disciplina,
            "descricao": descricao,
            "prioridade": prioridade,
            "concluido": False,
            "criado_em": agora.strftime(
                "%d/%m/%Y às %H:%M"
            ),
            "atualizado_em": ""
        }
    )

    salvar_agenda(agenda)

    flash(
        "Atividade adicionada ao calendário!",
        "success"
    )

    return redirect(
        url_for("calendario")
    )


@app.route(
    "/calendario/<evento_id>/editar",
    methods=["POST"]
)
def editar_evento(evento_id):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    agenda = carregar_agenda()
    email = session["email"]
    eventos = eventos_do_usuario(
        agenda,
        email
    )

    evento = buscar_evento(
        eventos,
        evento_id
    )

    if not evento:
        flash(
            "Atividade não encontrada.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    titulo = request.form.get(
        "titulo",
        ""
    ).strip()

    data = request.form.get(
        "data",
        ""
    ).strip()

    if not titulo or not data:
        flash(
            "Informe o título e a data.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    try:
        datetime.strptime(
            data,
            "%Y-%m-%d"
        )
    except ValueError:
        flash(
            "A data informada é inválida.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    prioridade = request.form.get(
        "prioridade",
        "media"
    ).strip().lower()

    if prioridade not in {
        "baixa",
        "media",
        "alta"
    }:
        prioridade = "media"

    evento["titulo"] = titulo
    evento["data"] = data
    evento["horario"] = request.form.get(
        "horario",
        ""
    ).strip()
    evento["disciplina"] = request.form.get(
        "disciplina",
        ""
    ).strip()
    evento["descricao"] = request.form.get(
        "descricao",
        ""
    ).strip()
    evento["prioridade"] = prioridade
    evento["atualizado_em"] = datetime.now().strftime(
        "%d/%m/%Y às %H:%M"
    )

    salvar_agenda(agenda)

    flash(
        "Atividade atualizada!",
        "success"
    )

    return redirect(
        url_for("calendario")
    )


@app.route(
    "/calendario/<evento_id>/concluir",
    methods=["POST"]
)
def concluir_evento(evento_id):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    agenda = carregar_agenda()
    email = session["email"]
    eventos = eventos_do_usuario(
        agenda,
        email
    )

    evento = buscar_evento(
        eventos,
        evento_id
    )

    if not evento:
        flash(
            "Atividade não encontrada.",
            "danger"
        )

        return redirect(
            url_for("calendario")
        )

    evento["concluido"] = not evento.get(
        "concluido",
        False
    )

    evento["atualizado_em"] = datetime.now().strftime(
        "%d/%m/%Y às %H:%M"
    )

    salvar_agenda(agenda)

    flash(
        "Atividade concluída!"
        if evento["concluido"]
        else "Atividade marcada como pendente.",
        "success"
    )

    return redirect(
        url_for("calendario")
    )


@app.route(
    "/calendario/<evento_id>/excluir",
    methods=["POST"]
)
def excluir_evento(evento_id):
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    agenda = carregar_agenda()
    email = session["email"]
    eventos = eventos_do_usuario(
        agenda,
        email
    )

    quantidade_anterior = len(eventos)

    agenda[email] = [
        evento
        for evento in eventos
        if evento.get("id") != evento_id
    ]

    salvar_agenda(agenda)

    if len(agenda[email]) < quantidade_anterior:
        flash(
            "Atividade excluída.",
            "success"
        )
    else:
        flash(
            "Atividade não encontrada.",
            "danger"
        )

    return redirect(
        url_for("calendario")
    )


@app.route(
    "/cadastro",
    methods=["GET", "POST"]
)
def nova_vaga():
    dados = carregar_dados()

    if request.method == "POST":
        nome = request.form.get(
            "nome",
            ""
        ).strip()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        idade = request.form.get(
            "idade",
            ""
        ).strip()

        serie = request.form.get(
            "serie",
            ""
        ).strip()

        senha = request.form.get(
            "senha",
            ""
        )

        confirmar = request.form.get(
            "confirmar_senha",
            ""
        )

        if not all(
            [
                nome,
                email,
                idade,
                serie,
                senha,
                confirmar
            ]
        ):
            flash(
                "Preencha todos os campos.",
                "danger"
            )

        elif buscar_aluno(
            dados,
            email
        ):
            flash(
                "Este e-mail já está cadastrado.",
                "danger"
            )

        elif senha != confirmar:
            flash(
                "As senhas não coincidem.",
                "danger"
            )

        elif len(senha) < 6:
            flash(
                "A senha deve ter pelo menos 6 caracteres.",
                "danger"
            )

        elif not buscar_serie(
            dados,
            serie
        ):
            flash(
                "Selecione uma série válida.",
                "danger"
            )

        else:
            dados["alunos"].append(
                {
                    "id": uuid.uuid4().hex,
                    "nome": nome,
                    "email": email,
                    "idade": idade,
                    "serie": serie,
                    "senha": generate_password_hash(
                        senha
                    ),
                    "foto": ""
                }
            )

            salvar_json(
                ARQUIVO_DADOS,
                dados
            )

            flash(
                "Cadastro concluído! Agora entre na sua conta.",
                "success"
            )

            return redirect(
                url_for("login")
            )

    return render_template(
        "cadastrar.html",
        series=dados["series"]
    )


@app.route(
    "/login",
    methods=["GET", "POST"]
)
def login():
    if request.method == "POST":
        dados = carregar_dados()

        email = request.form.get(
            "email",
            ""
        ).strip().lower()

        senha = request.form.get(
            "senha",
            ""
        )

        aluno = buscar_aluno(
            dados,
            email
        )

        if (
            aluno
            and check_password_hash(
                aluno["senha"],
                senha
            )
        ):
            session["email"] = aluno["email"]

            flash(
                f"Bem-vindo(a), {aluno['nome'].split()[0]}!",
                "success"
            )

            return redirect(
                url_for("minha_serie")
            )

        flash(
            "E-mail ou senha incorretos.",
            "danger"
        )

    return render_template(
        "login.html"
    )


@app.route(
    "/perfil",
    methods=["GET", "POST"]
)
def perfil():
    bloqueio = login_obrigatorio()

    if bloqueio:
        return bloqueio

    dados = carregar_dados()

    aluno = buscar_aluno(
        dados,
        session["email"]
    )

    if not aluno:
        session.clear()

        return redirect(
            url_for("login")
        )

    if request.method == "POST":
        novo_email = request.form.get(
            "email",
            ""
        ).strip().lower()

        outro = buscar_aluno(
            dados,
            novo_email
        )

        if outro and outro is not aluno:
            flash(
                "Esse e-mail já está em uso.",
                "danger"
            )

            return redirect(
                url_for("perfil")
            )

        aluno["nome"] = request.form.get(
            "nome",
            aluno["nome"]
        ).strip()

        aluno["email"] = novo_email

        aluno["idade"] = request.form.get(
            "idade",
            aluno["idade"]
        ).strip()

        aluno["serie"] = request.form.get(
            "serie",
            aluno["serie"]
        )

        foto = salvar_foto(
            request.files.get("foto")
        )

        if foto:
            aluno["foto"] = foto

        senha_atual = request.form.get(
            "senha_atual",
            ""
        )

        nova_senha = request.form.get(
            "nova_senha",
            ""
        )

        confirmar = request.form.get(
            "confirmar_senha",
            ""
        )

        if nova_senha:
            if not check_password_hash(
                aluno["senha"],
                senha_atual
            ):
                flash(
                    "A senha atual está incorreta.",
                    "danger"
                )

                return redirect(
                    url_for("perfil")
                )

            if (
                nova_senha != confirmar
                or len(nova_senha) < 6
            ):
                flash(
                    "Confira a nova senha e a confirmação.",
                    "danger"
                )

                return redirect(
                    url_for("perfil")
                )

            aluno["senha"] = generate_password_hash(
                nova_senha
            )

        email_antigo = session["email"]

        session["email"] = novo_email

        salvar_json(
            ARQUIVO_DADOS,
            dados
        )

        if email_antigo != novo_email:
            cadernos = carregar_cadernos()

            if email_antigo in cadernos:
                cadernos[novo_email] = cadernos.pop(
                    email_antigo
                )

                salvar_cadernos(
                    cadernos
                )

        flash(
            "Perfil atualizado.",
            "success"
        )

        return redirect(
            url_for("perfil")
        )

    return render_template(
        "editar.html",
        aluno=aluno,
        series=dados["series"]
    )


@app.route("/sair")
def sair():
    session.clear()

    flash(
        "Você saiu da sua conta.",
        "success"
    )

    return redirect(
        url_for("inicio")
    )


@app.route("/sobre")
def sobre():
    return render_template(
        "sobre.html"
    )


@app.route("/acessibilidade")
def acessibilidade():
    return render_template(
        "acessibilidade.html"
    )


@app.route("/termos")
def termos():
    return render_template(
        "termos.html"
    )


@app.route("/privacidade")
def privacidade():
    return render_template(
        "privacidade.html"
    )


def abrir_navegador():
    webbrowser.open_new(
        "http://127.0.0.1:5000"
    )


if __name__ == "__main__":
    if os.environ.get(
        "WERKZEUG_RUN_MAIN"
    ) == "true":
        Timer(
            1,
            abrir_navegador
        ).start()

    app.run(
        debug=True
    )
