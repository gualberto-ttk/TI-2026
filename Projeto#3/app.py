from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
import json
import os
import threading
import subprocess
import time

app = Flask(__name__)
app.secret_key = "estude_mais_2026"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ARQUIVO = os.path.join(BASE_DIR, "data", "vagas.json")


def carregar():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)
    except (FileNotFoundError, json.JSONDecodeError):
        dados = {"series": [], "alunos": []}

    dados.setdefault("series", [])
    dados.setdefault("alunos", [])

    return dados


def salvar(dados):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def buscar_serie(dados, slug):
    return next(
        (
            serie
            for serie in dados["series"]
            if serie.get("slug") == slug
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


def exigir_login():
    return session.get("email")


def criar_material(disciplina, titulo):
    materiais = {
        "Português": {
            "icone": "fa-solid fa-pen-nib",
            "introducao": (
                f"Nesta aula você estudará {titulo}, um conteúdo importante "
                "para melhorar sua leitura, escrita e interpretação."
            ),
            "passos": [
                f"Entender o que é {titulo}.",
                "Observar como esse conteúdo aparece em frases e textos.",
                "Analisar exemplos simples.",
                "Resolver uma atividade de revisão."
            ],
            "explicacao": (
                f"{titulo} faz parte dos estudos da Língua Portuguesa. "
                "Para aprender esse assunto, é importante observar exemplos, "
                "identificar suas características e praticar com frases e textos."
            ),
            "exemplo": (
                f"Leia uma frase ou pequeno texto e tente identificar onde "
                f"o conteúdo de {titulo} aparece."
            ),
            "atividade": (
                f"Crie três frases usando o que você aprendeu sobre {titulo}. "
                "Depois, releia e verifique se utilizou o conteúdo corretamente."
            )
        },

        "Matemática": {
            "icone": "fa-solid fa-calculator",
            "introducao": (
                f"Nesta aula você aprenderá {titulo} por meio de explicações, "
                "exemplos e exercícios simples."
            ),
            "passos": [
                f"Conhecer o conceito de {titulo}.",
                "Entender as regras e etapas de resolução.",
                "Acompanhar um exemplo.",
                "Praticar com exercícios."
            ],
            "explicacao": (
                f"{titulo} é um conteúdo da Matemática que exige atenção às "
                "regras e à ordem das etapas. Leia cada questão com cuidado, "
                "organize os valores e confira o resultado ao terminar."
            ),
            "exemplo": (
                f"Escolha valores simples e monte um exemplo relacionado a "
                f"{titulo}. Resolva uma etapa de cada vez e confira o resultado."
            ),
            "atividade": (
                f"Crie e resolva três exercícios sobre {titulo}: um fácil, "
                "um intermediário e um mais desafiador."
            )
        },

        "Ciências": {
            "icone": "fa-solid fa-flask",
            "introducao": (
                f"Nesta aula você conhecerá melhor {titulo} e sua relação "
                "com a natureza, a saúde e o cotidiano."
            ),
            "passos": [
                f"Compreender o significado de {titulo}.",
                "Observar onde esse assunto aparece no cotidiano.",
                "Conhecer exemplos importantes.",
                "Fazer uma atividade de revisão."
            ],
            "explicacao": (
                f"{titulo} é um tema importante das Ciências. Esse conteúdo "
                "ajuda a compreender fenômenos, seres vivos, o ambiente e "
                "situações presentes no dia a dia."
            ),
            "exemplo": (
                f"Pense em uma situação do cotidiano relacionada a {titulo} "
                "e explique como ela acontece."
            ),
            "atividade": (
                f"Faça um pequeno resumo sobre {titulo} e escreva dois exemplos "
                "encontrados na natureza ou no cotidiano."
            )
        },

        "História": {
            "icone": "fa-solid fa-landmark",
            "introducao": (
                f"Nesta aula você estudará {titulo} e entenderá sua importância "
                "para a sociedade e para o conhecimento do passado."
            ),
            "passos": [
                f"Identificar o contexto de {titulo}.",
                "Conhecer os principais acontecimentos.",
                "Entender suas consequências.",
                "Produzir um resumo."
            ],
            "explicacao": (
                f"O estudo de {titulo} ajuda a compreender mudanças ocorridas "
                "ao longo do tempo, as ações humanas e seus efeitos na sociedade."
            ),
            "exemplo": (
                f"Organize os fatos ligados a {titulo} em uma pequena linha do tempo."
            ),
            "atividade": (
                f"Escreva um parágrafo explicando por que {titulo} é importante "
                "para compreender a sociedade."
            )
        },

        "Geografia": {
            "icone": "fa-solid fa-earth-americas",
            "introducao": (
                f"Nesta aula você estudará {titulo} e sua relação com o espaço "
                "geográfico, a natureza e a sociedade."
            ),
            "passos": [
                f"Conhecer o conceito de {titulo}.",
                "Observar sua presença no espaço geográfico.",
                "Analisar exemplos.",
                "Fazer uma atividade."
            ],
            "explicacao": (
                f"{titulo} é um tema que ajuda a compreender os lugares, "
                "as paisagens e as relações entre as pessoas e o ambiente."
            ),
            "exemplo": (
                f"Observe o lugar onde você vive e identifique algo relacionado "
                f"ao tema {titulo}."
            ),
            "atividade": (
                f"Descreva dois exemplos de {titulo} presentes em sua cidade "
                "ou região."
            )
        },

        "Biologia": {
            "icone": "fa-solid fa-dna",
            "introducao": (
                f"Nesta aula você estudará {titulo}, um tema relacionado aos "
                "seres vivos e aos processos da vida."
            ),
            "passos": [
                f"Conhecer o conceito de {titulo}.",
                "Entender como esse processo ocorre.",
                "Observar exemplos biológicos.",
                "Revisar o conteúdo."
            ],
            "explicacao": (
                f"{titulo} é um conteúdo da Biologia que ajuda a compreender "
                "o funcionamento, a organização e a diversidade dos seres vivos."
            ),
            "exemplo": (
                f"Escolha um ser vivo e explique como ele se relaciona com "
                f"o conteúdo de {titulo}."
            ),
            "atividade": (
                f"Monte um esquema com as principais informações sobre {titulo}."
            )
        },

        "Física": {
            "icone": "fa-solid fa-atom",
            "introducao": (
                f"Nesta aula você estudará {titulo} e sua aplicação nos "
                "fenômenos observados no cotidiano."
            ),
            "passos": [
                f"Conhecer o conceito de {titulo}.",
                "Identificar as grandezas envolvidas.",
                "Analisar um exemplo.",
                "Resolver uma atividade."
            ],
            "explicacao": (
                f"{titulo} é um assunto da Física usado para compreender "
                "movimentos, energia, forças e outros fenômenos naturais."
            ),
            "exemplo": (
                f"Observe uma situação cotidiana relacionada a {titulo} "
                "e identifique o que está acontecendo."
            ),
            "atividade": (
                f"Escreva um exemplo de aplicação de {titulo} no cotidiano "
                "e explique seu funcionamento."
            )
        },

        "Química": {
            "icone": "fa-solid fa-vial",
            "introducao": (
                f"Nesta aula você estudará {titulo} e compreenderá sua relação "
                "com as substâncias e suas transformações."
            ),
            "passos": [
                f"Conhecer o conceito de {titulo}.",
                "Identificar seus elementos principais.",
                "Observar exemplos.",
                "Fazer uma revisão."
            ],
            "explicacao": (
                f"{titulo} é um conteúdo da Química que ajuda a entender "
                "a matéria, sua composição, suas propriedades e transformações."
            ),
            "exemplo": (
                f"Procure no cotidiano uma substância ou transformação "
                f"relacionada a {titulo}."
            ),
            "atividade": (
                f"Liste três exemplos relacionados a {titulo} e explique "
                "por que eles fazem parte desse conteúdo."
            )
        }
    }

    padrao = {
        "icone": "fa-solid fa-book-open",
        "introducao": (
            f"Nesta aula você estudará {titulo}, um conteúdo importante "
            f"da disciplina de {disciplina}."
        ),
        "passos": [
            f"Compreender o conceito de {titulo}.",
            "Observar exemplos.",
            "Anotar as informações principais.",
            "Resolver uma atividade."
        ],
        "explicacao": (
            f"{titulo} é um dos conteúdos estudados em {disciplina}. "
            "Leia atentamente, faça anotações e revise os exemplos para "
            "compreender melhor o assunto."
        ),
        "exemplo": (
            f"Procure um exemplo de {titulo} em seu material escolar "
            "ou em uma situação do cotidiano."
        ),
        "atividade": (
            f"Escreva um resumo de cinco linhas sobre {titulo} e destaque "
            "as informações mais importantes."
        )
    }

    return materiais.get(disciplina, padrao)


@app.route("/")
def inicio():
    dados = carregar()

    return render_template(
        "index.html",
        series=dados["series"]
    )


@app.route("/series")
def listar_vagas():
    dados = carregar()
    busca = request.args.get("busca", "").strip().lower()
    series = dados["series"]

    if busca:
        resultado = []

        for serie in series:
            encontrou = busca in serie.get("nome", "").lower()
            disciplinas = serie.get("disciplinas", {})

            for disciplina, conteudos in disciplinas.items():
                if busca in disciplina.lower():
                    encontrou = True

                if any(
                    busca in str(conteudo).lower()
                    for conteudo in conteudos
                ):
                    encontrou = True

            if encontrou:
                resultado.append(serie)

        series = resultado

    return render_template(
        "vagas.html",
        series=series,
        busca=busca
    )


@app.route("/cadastro", methods=["GET", "POST"])
def nova_vaga():
    dados = carregar()

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        email = request.form.get("email", "").strip().lower()
        idade = request.form.get("idade", "").strip()
        serie_slug = request.form.get("serie", "").strip()
        senha = request.form.get("senha", "")
        confirmar_senha = request.form.get("confirmar_senha", "")

        serie = buscar_serie(dados, serie_slug)

        if not nome or not email or not idade or not serie_slug or not senha:
            flash("Preencha todos os campos.", "danger")

        elif not serie:
            flash("Selecione uma série válida.", "danger")

        elif buscar_aluno(dados, email):
            flash("Este e-mail já está cadastrado.", "danger")

        elif senha != confirmar_senha:
            flash("As senhas não são iguais.", "danger")

        elif len(senha) < 6:
            flash("A senha deve ter pelo menos 6 caracteres.", "danger")

        else:
            dados["alunos"].append({
                "nome": nome,
                "email": email,
                "idade": idade,
                "serie": serie_slug,
                "senha": generate_password_hash(senha)
            })

            salvar(dados)

            flash(
                "Cadastro confirmado! Agora entre na sua conta.",
                "success"
            )

            return redirect(url_for("login"))

    return render_template(
        "cadastrar.html",
        series=dados["series"]
    )


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("email"):
        return redirect(url_for("minha_serie"))

    if request.method == "POST":
        dados = carregar()
        email = request.form.get("email", "").strip().lower()
        senha = request.form.get("senha", "")
        aluno = buscar_aluno(dados, email)

        if aluno and check_password_hash(aluno.get("senha", ""), senha):
            session["email"] = email

            flash(
                f"Bem-vindo, {aluno['nome']}!",
                "success"
            )

            return redirect(
                url_for(
                    "detalhes_vaga",
                    slug=aluno["serie"]
                )
            )

        flash("E-mail ou senha incorretos.", "danger")

    return render_template("login.html")


@app.route("/serie/<slug>")
def detalhes_vaga(slug):
    if not exigir_login():
        flash("Faça login para acessar os conteúdos.", "danger")
        return redirect(url_for("login"))

    dados = carregar()
    aluno = buscar_aluno(dados, session["email"])
    serie = buscar_serie(dados, slug)

    if not aluno:
        session.clear()
        return redirect(url_for("login"))

    if not serie:
        flash("Série não encontrada.", "danger")
        return redirect(url_for("listar_vagas"))

    return render_template(
        "detalhes.html",
        serie=serie,
        aluno=aluno
    )


@app.route(
    "/serie/<slug>/disciplina/<path:disciplina>/conteudo/<int:indice>"
)
def ver_conteudo(slug, disciplina, indice):
    if not exigir_login():
        flash("Faça login para acessar este conteúdo.", "danger")
        return redirect(url_for("login"))

    dados = carregar()
    aluno = buscar_aluno(dados, session["email"])
    serie = buscar_serie(dados, slug)

    if not aluno:
        session.clear()
        return redirect(url_for("login"))

    if not serie:
        flash("Série não encontrada.", "danger")
        return redirect(url_for("listar_vagas"))

    disciplinas = serie.get("disciplinas", {})
    conteudos = disciplinas.get(disciplina)

    if not conteudos or indice < 0 or indice >= len(conteudos):
        flash("Conteúdo não encontrado.", "danger")

        return redirect(
            url_for(
                "detalhes_vaga",
                slug=slug
            )
        )

    titulo = conteudos[indice]
    material = criar_material(disciplina, titulo)

    anterior = indice - 1 if indice > 0 else None
    proximo = indice + 1 if indice < len(conteudos) - 1 else None

    return render_template(
        "conteudo.html",
        serie=serie,
        aluno=aluno,
        disciplina=disciplina,
        titulo=titulo,
        material=material,
        indice=indice,
        anterior=anterior,
        proximo=proximo,
        total=len(conteudos)
    )


@app.route("/minha-serie")
def minha_serie():
    if not exigir_login():
        return redirect(url_for("login"))

    dados = carregar()
    aluno = buscar_aluno(dados, session["email"])

    if not aluno:
        session.clear()
        return redirect(url_for("login"))

    return redirect(
        url_for(
            "detalhes_vaga",
            slug=aluno["serie"]
        )
    )


@app.route("/meu-cadastro", methods=["GET", "POST"])
def editar_vaga():
    if not exigir_login():
        return redirect(url_for("login"))

    dados = carregar()
    aluno = buscar_aluno(dados, session["email"])

    if not aluno:
        session.clear()
        return redirect(url_for("login"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        idade = request.form.get("idade", "").strip()
        serie_slug = request.form.get("serie", "").strip()
        serie = buscar_serie(dados, serie_slug)

        if not nome or not idade or not serie:
            flash("Preencha os campos corretamente.", "danger")

        else:
            aluno["nome"] = nome
            aluno["idade"] = idade
            aluno["serie"] = serie_slug

            salvar(dados)

            flash("Cadastro atualizado com sucesso!", "success")

            return redirect(
                url_for(
                    "detalhes_vaga",
                    slug=serie_slug
                )
            )

    return render_template(
        "editar.html",
        aluno=aluno,
        series=dados["series"]
    )


@app.route("/sair")
def sair():
    session.clear()
    flash("Você saiu da sua conta.", "success")
    return redirect(url_for("login"))


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/acessibilidade")
def acessibilidade():
    return render_template("acessibilidade.html")


def abrir_navegador():
    time.sleep(2)

    subprocess.run(
        'start "" "http://127.0.0.1:5000"',
        shell=True
    )


if __name__ == "__main__":
    threading.Thread(
        target=abrir_navegador,
        daemon=True
    ).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )