from flask import Flask, render_template, request, redirect, url_for, session, flash
import json
import os
import threading
import subprocess
import time

app = Flask(__name__)
app.secret_key = "educacao_para_todos"

ARQUIVO = os.path.join(
    os.path.dirname(os.path.abspath(__file__)),
    "data",
    "vagas.json"
)


def carregar():
    try:
        with open(ARQUIVO, "r", encoding="utf-8") as arquivo:
            dados = json.load(arquivo)

        dados.setdefault("series", [])
        dados.setdefault("alunos", [])

        return dados

    except:
        return {"series": [], "alunos": []}


def salvar(dados):
    os.makedirs(os.path.dirname(ARQUIVO), exist_ok=True)

    with open(ARQUIVO, "w", encoding="utf-8") as arquivo:
        json.dump(dados, arquivo, ensure_ascii=False, indent=4)


def buscar_serie(dados, slug):
    return next(
        (serie for serie in dados["series"] if serie["slug"] == slug),
        None
    )


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
        series = [
            serie for serie in series
            if busca in serie["nome"].lower()
            or any(
                busca in disciplina.lower()
                or any(
                    busca in conteudo.lower()
                    for conteudo in conteudos
                )
                for disciplina, conteudos
                in serie["disciplinas"].items()
            )
        ]

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

        serie = buscar_serie(dados, serie_slug)

        if not nome or not email or not idade or not serie:
            flash("Preencha todos os campos corretamente.", "danger")

            return render_template(
                "cadastrar.html",
                series=dados["series"]
            )

        aluno = next(
            (
                aluno for aluno in dados["alunos"]
                if aluno["email"] == email
            ),
            None
        )

        if aluno:
            aluno.update({
                "nome": nome,
                "idade": idade,
                "serie": serie_slug
            })
        else:
            dados["alunos"].append({
                "nome": nome,
                "email": email,
                "idade": idade,
                "serie": serie_slug
            })

        salvar(dados)
        session["email"] = email

        flash("Cadastro realizado com sucesso!", "success")

        return redirect(
            url_for("detalhes_vaga", slug=serie_slug)
        )

    return render_template(
        "cadastrar.html",
        series=dados["series"]
    )


@app.route("/serie/<slug>")
def detalhes_vaga(slug):
    dados = carregar()
    serie = buscar_serie(dados, slug)

    if not serie:
        flash("Série não encontrada.", "danger")
        return redirect(url_for("listar_vagas"))

    email = session.get("email")

    aluno = next(
        (
            aluno for aluno in dados["alunos"]
            if aluno["email"] == email
        ),
        None
    )

    return render_template(
        "detalhes.html",
        serie=serie,
        aluno=aluno
    )


@app.route("/meu-cadastro", methods=["GET", "POST"])
def editar_vaga():
    dados = carregar()
    email = session.get("email")

    aluno = next(
        (
            aluno for aluno in dados["alunos"]
            if aluno["email"] == email
        ),
        None
    )

    if not aluno:
        flash("Faça seu cadastro primeiro.", "danger")
        return redirect(url_for("nova_vaga"))

    if request.method == "POST":
        nome = request.form.get("nome", "").strip()
        novo_email = request.form.get("email", "").strip().lower()
        idade = request.form.get("idade", "").strip()
        serie_slug = request.form.get("serie", "").strip()

        serie = buscar_serie(dados, serie_slug)

        if not nome or not novo_email or not idade or not serie:
            flash("Preencha todos os campos corretamente.", "danger")

            return render_template(
                "editar.html",
                aluno=aluno,
                series=dados["series"]
            )

        email_usado = next(
            (
                outro for outro in dados["alunos"]
                if outro["email"] == novo_email
                and outro is not aluno
            ),
            None
        )

        if email_usado:
            flash("Esse e-mail já está cadastrado.", "danger")

            return render_template(
                "editar.html",
                aluno=aluno,
                series=dados["series"]
            )

        aluno.update({
            "nome": nome,
            "email": novo_email,
            "idade": idade,
            "serie": serie_slug
        })

        salvar(dados)
        session["email"] = novo_email

        flash("Cadastro atualizado com sucesso!", "success")

        return redirect(
            url_for("detalhes_vaga", slug=serie_slug)
        )

    return render_template(
        "editar.html",
        aluno=aluno,
        series=dados["series"]
    )


@app.route("/minha-serie")
def minha_serie():
    dados = carregar()
    email = session.get("email")

    aluno = next(
        (
            aluno for aluno in dados["alunos"]
            if aluno["email"] == email
        ),
        None
    )

    if not aluno:
        flash("Faça seu cadastro primeiro.", "danger")
        return redirect(url_for("nova_vaga"))

    return redirect(
        url_for("detalhes_vaga", slug=aluno["serie"])
    )


@app.route("/sair")
def sair():
    session.clear()
    flash("Você saiu da plataforma.", "success")
    return redirect(url_for("inicio"))


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