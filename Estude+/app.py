from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash
)

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from werkzeug.utils import secure_filename

from datetime import datetime

import json
import os
import uuid
import threading
import webbrowser


app = Flask(__name__)

app.secret_key = os.environ.get(
    "SECRET_KEY",
    "estude_mais_2026"
)

app.config["MAX_CONTENT_LENGTH"] = 3 * 1024 * 1024


BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

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


# =========================================================
# CURRÍCULO DO SITE
# =========================================================

CURRICULO_SERIES = [

    # =====================================================
    # ENSINO FUNDAMENTAL I
    # =====================================================

    {
        "slug": "1-fundamental",
        "nome": "1º Ano do Ensino Fundamental",
        "grupo": "Fundamental I",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    {
        "slug": "2-fundamental",
        "nome": "2º Ano do Ensino Fundamental",
        "grupo": "Fundamental I",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    {
        "slug": "3-fundamental",
        "nome": "3º Ano do Ensino Fundamental",
        "grupo": "Fundamental I",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": [],
            "Inglês": []
        }
    },

    {
        "slug": "4-fundamental",
        "nome": "4º Ano do Ensino Fundamental",
        "grupo": "Fundamental I",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": [],
            "Inglês": []
        }
    },

    {
        "slug": "5-fundamental",
        "nome": "5º Ano do Ensino Fundamental",
        "grupo": "Fundamental I",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": [],
            "Inglês": []
        }
    },

    # =====================================================
    # ENSINO FUNDAMENTAL II
    # =====================================================

    {
        "slug": "6-fundamental",
        "nome": "6º Ano do Ensino Fundamental",
        "grupo": "Fundamental II",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Inglês": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    {
        "slug": "7-fundamental",
        "nome": "7º Ano do Ensino Fundamental",
        "grupo": "Fundamental II",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Inglês": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    {
        "slug": "8-fundamental",
        "nome": "8º Ano do Ensino Fundamental",
        "grupo": "Fundamental II",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Inglês": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    {
        "slug": "9-fundamental",
        "nome": "9º Ano do Ensino Fundamental",
        "grupo": "Fundamental II",
        "disciplinas": {
            "Língua Portuguesa": [],
            "Inglês": [],
            "Matemática": [],
            "Ciências": [],
            "História": [],
            "Geografia": [],
            "Arte": [],
            "Educação Física": [],
            "Ensino Religioso": []
        }
    },

    # =====================================================
    # ENSINO MÉDIO
    # =====================================================

    {
        "slug": "1-medio",
        "nome": "1º Ano do Ensino Médio",
        "grupo": "Ensino Médio",
        "disciplinas": {
            "Língua Portuguesa e Literatura": [],
            "Inglês": [],
            "Matemática": [],
            "Física": [],
            "Química": [],
            "Biologia": [],
            "História": [],
            "Geografia": [],
            "Filosofia": [],
            "Sociologia": [],
            "Arte": [],
            "Educação Física": []
        }
    },

    {
        "slug": "2-medio",
        "nome": "2º Ano do Ensino Médio",
        "grupo": "Ensino Médio",
        "disciplinas": {
            "Língua Portuguesa e Literatura": [],
            "Inglês": [],
            "Matemática": [],
            "Física": [],
            "Química": [],
            "Biologia": [],
            "História": [],
            "Geografia": [],
            "Filosofia": [],
            "Sociologia": [],
            "Arte": [],
            "Educação Física": []
        }
    },

    {
        "slug": "3-medio",
        "nome": "3º Ano do Ensino Médio",
        "grupo": "Ensino Médio",
        "disciplinas": {
            "Língua Portuguesa e Literatura": [],
            "Inglês": [],
            "Matemática": [],
            "Física": [],
            "Química": [],
            "Biologia": [],
            "História": [],
            "Geografia": [],
            "Filosofia": [],
            "Sociologia": [],
            "Arte": [],
            "Educação Física": []
        }
    }
]


# =========================================================
# FUNÇÕES DOS ARQUIVOS JSON
# =========================================================

def ler_json(caminho, padrao):
    try:
        with open(
            caminho,
            "r",
            encoding="utf-8"
        ) as arquivo:
            return json.load(arquivo)

    except (
        FileNotFoundError,
        json.JSONDecodeError
    ):
        return padrao


def salvar_json(caminho, dados):
    pasta = os.path.dirname(caminho)

    if pasta:
        os.makedirs(
            pasta,
            exist_ok=True
        )

    with open(
        caminho,
        "w",
        encoding="utf-8"
    ) as arquivo:
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

    dados.setdefault(
        "series",
        []
    )

    dados.setdefault(
        "alunos",
        []
    )

    series_atuais = {
        serie.get("slug"): serie
        for serie in dados["series"]
        if serie.get("slug")
    }

    series_atualizadas = []

    for serie_padrao in CURRICULO_SERIES:
        slug = serie_padrao["slug"]

        serie_existente = series_atuais.get(
            slug,
            {}
        )

        disciplinas_antigas = serie_existente.get(
            "disciplinas",
            {}
        )

        serie_atualizada = {
            "slug": slug,
            "nome": serie_padrao["nome"],
            "grupo": serie_padrao["grupo"],
            "disciplinas": {}
        }

        for disciplina in serie_padrao["disciplinas"]:
            conteudo_anterior = disciplinas_antigas.get(
                disciplina,
                []
            )

            if isinstance(
                conteudo_anterior,
                list
            ):
                serie_atualizada[
                    "disciplinas"
                ][disciplina] = conteudo_anterior

            else:
                serie_atualizada[
                    "disciplinas"
                ][disciplina] = []

        series_atualizadas.append(
            serie_atualizada
        )

    if dados["series"] != series_atualizadas:
        dados["series"] = series_atualizadas

        salvar_json(
            ARQUIVO_DADOS,
            dados
        )

    return dados


# =========================================================
# FUNÇÕES DE BUSCA
# =========================================================

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


# =========================================================
# LOGIN
# =========================================================

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


# =========================================================
# FOTOS DE PERFIL
# =========================================================

def foto_valida(nome):
    return (
        "." in nome
        and nome.rsplit(
            ".",
            1
        )[1].lower() in EXTENSOES
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

    caminho_completo = os.path.join(
        PASTA_FOTOS,
        nome_arquivo
    )

    arquivo.save(
        caminho_completo
    )

    return (
        f"uploads/perfis/{nome_arquivo}"
    )


# =========================================================
# USUÁRIO DISPONÍVEL NOS TEMPLATES
# =========================================================

@app.context_processor
def usuario_contexto():
    email = session.get("email")

    if not email:
        return {
            "usuario_atual": None
        }

    dados = carregar_dados()

    usuario = buscar_aluno(
        dados,
        email
    )

    return {
        "usuario_atual": usuario
    }


# =========================================================
# PÁGINA INICIAL
# =========================================================

@app.route("/")
def inicio():
    return render_template(
        "index.html"
    )


# =========================================================
# LISTA DE SÉRIES
# =========================================================

@app.route("/series")
def listar_vagas():
    dados = carregar_dados()

    return render_template(
        "vagas.html",
        series=dados["series"]
    )


# =========================================================
# DISCIPLINAS DA SÉRIE
# =========================================================

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


# =========================================================
# SÉRIE DO USUÁRIO
# =========================================================

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

        flash(
            "Usuário não encontrado. Entre novamente.",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    serie = buscar_serie(
        dados,
        aluno.get("serie")
    )

    if not serie:
        flash(
            "A série cadastrada não foi encontrada.",
            "danger"
        )

        return redirect(
            url_for("listar_vagas")
        )

    return redirect(
        url_for(
            "detalhes_vaga",
            slug=serie["slug"]
        )
    )


# =========================================================
# CADERNO DE CADA DISCIPLINA
# =========================================================

@app.route(
    "/caderno/<slug>/<disciplina>",
    methods=["GET", "POST"]
)
def caderno(slug, disciplina):
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
        or disciplina not in serie["disciplinas"]
    ):
        flash(
            "Disciplina não encontrada.",
            "danger"
        )

        return redirect(
            url_for("listar_vagas")
        )

    cadernos = ler_json(
        ARQUIVO_CADERNOS,
        {}
    )

    email = session["email"]

    chave = (
        f"{slug}::{disciplina}"
    )

    caderno_padrao = {
        "titulo": "",
        "tema": "",
        "conteudo": "",
        "nota1": "",
        "nota2": "",
        "nota3": "",
        "atualizado_em": ""
    }

    caderno_atual = cadernos.get(
        email,
        {}
    ).get(
        chave,
        caderno_padrao
    )

    if request.method == "POST":
        caderno_atual = {
            "titulo": request.form.get(
                "titulo",
                ""
            ).strip(),

            "tema": request.form.get(
                "tema",
                ""
            ).strip(),

            "conteudo": request.form.get(
                "conteudo",
                ""
            ).strip(),

            "nota1": request.form.get(
                "nota1",
                ""
            ).strip(),

            "nota2": request.form.get(
                "nota2",
                ""
            ).strip(),

            "nota3": request.form.get(
                "nota3",
                ""
            ).strip(),

            "atualizado_em": datetime.now().strftime(
                "%d/%m/%Y às %H:%M"
            )
        }

        cadernos.setdefault(
            email,
            {}
        )[chave] = caderno_atual

        salvar_json(
            ARQUIVO_CADERNOS,
            cadernos
        )

        flash(
            "Caderno salvo com sucesso!",
            "success"
        )

        return redirect(
            url_for(
                "caderno",
                slug=slug,
                disciplina=disciplina
            )
        )

    return render_template(
        "conteudo.html",
        serie=serie,
        disciplina=disciplina,
        caderno=caderno_atual
    )


# =========================================================
# CADASTRO
# =========================================================

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
            novo_aluno = {
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

            dados["alunos"].append(
                novo_aluno
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


# =========================================================
# ENTRAR
# =========================================================

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


# =========================================================
# PERFIL
# =========================================================

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

        flash(
            "Usuário não encontrado.",
            "danger"
        )

        return redirect(
            url_for("login")
        )

    if request.method == "POST":
        novo_email = request.form.get(
            "email",
            aluno["email"]
        ).strip().lower()

        outro_usuario = buscar_aluno(
            dados,
            novo_email
        )

        if (
            outro_usuario
            and outro_usuario.get("id") != aluno.get("id")
        ):
            flash(
                "Esse e-mail já está em uso.",
                "danger"
            )

            return redirect(
                url_for("perfil")
            )

        novo_nome = request.form.get(
            "nome",
            aluno["nome"]
        ).strip()

        nova_idade = request.form.get(
            "idade",
            aluno["idade"]
        ).strip()

        nova_serie = request.form.get(
            "serie",
            aluno["serie"]
        ).strip()

        if not novo_nome:
            flash(
                "Informe seu nome.",
                "danger"
            )

            return redirect(
                url_for("perfil")
            )

        if not novo_email:
            flash(
                "Informe seu e-mail.",
                "danger"
            )

            return redirect(
                url_for("perfil")
            )

        if not buscar_serie(
            dados,
            nova_serie
        ):
            flash(
                "Selecione uma série válida.",
                "danger"
            )

            return redirect(
                url_for("perfil")
            )

        aluno["nome"] = novo_nome
        aluno["email"] = novo_email
        aluno["idade"] = nova_idade
        aluno["serie"] = nova_serie

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

            if len(nova_senha) < 6:
                flash(
                    "A nova senha deve ter pelo menos 6 caracteres.",
                    "danger"
                )

                return redirect(
                    url_for("perfil")
                )

            if nova_senha != confirmar:
                flash(
                    "A nova senha e a confirmação não coincidem.",
                    "danger"
                )

                return redirect(
                    url_for("perfil")
                )

            aluno["senha"] = generate_password_hash(
                nova_senha
            )

        email_anterior = session["email"]

        session["email"] = novo_email

        salvar_json(
            ARQUIVO_DADOS,
            dados
        )

        if (
            email_anterior != novo_email
            and os.path.exists(ARQUIVO_CADERNOS)
        ):
            cadernos = ler_json(
                ARQUIVO_CADERNOS,
                {}
            )

            if email_anterior in cadernos:
                cadernos[novo_email] = cadernos.pop(
                    email_anterior
                )

                salvar_json(
                    ARQUIVO_CADERNOS,
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


# =========================================================
# SAIR
# =========================================================

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


# =========================================================
# PÁGINAS INSTITUCIONAIS
# =========================================================

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


# =========================================================
# ABRIR O NAVEGADOR AUTOMATICAMENTE
# =========================================================

def abrir_navegador():
    webbrowser.open_new(
        "http://127.0.0.1:5000"
    )


# =========================================================
# INICIAR O FLASK
# =========================================================

if __name__ == "__main__":
    carregar_dados()

    threading.Timer(
        1.5,
        abrir_navegador
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )