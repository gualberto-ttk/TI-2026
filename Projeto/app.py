from flask import Flask, render_template, request, redirect, url_for, flash
from threading import Timer
from uuid import uuid4
import json
import os
import webbrowser


app = Flask(__name__)
app.secret_key = "chave-secreta-incluivagas"

PASTA_PROJETO = os.path.dirname(os.path.abspath(__file__))
CAMINHO_JSON = os.path.join(PASTA_PROJETO, "data", "vagas.json")


def carregar_vagas():
    if not os.path.exists(CAMINHO_JSON):
        return []

    try:
        with open(CAMINHO_JSON, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)

    except (json.JSONDecodeError, OSError):
        return []


def salvar_vagas(vagas):
    pasta_data = os.path.dirname(CAMINHO_JSON)
    os.makedirs(pasta_data, exist_ok=True)

    with open(CAMINHO_JSON, "w", encoding="utf-8") as arquivo:
        json.dump(vagas, arquivo, ensure_ascii=False, indent=4)


def buscar_vaga_por_id(vaga_id):
    vagas = carregar_vagas()

    for vaga in vagas:
        if vaga.get("id") == vaga_id:
            return vaga

    return None


@app.route("/")
def inicio():
    vagas = carregar_vagas()
    vagas_recentes = list(reversed(vagas))[:3]

    return render_template(
        "index.html",
        total_vagas=len(vagas),
        vagas_recentes=vagas_recentes
    )


@app.route("/vagas")
def listar_vagas():
    vagas = carregar_vagas()

    pesquisa = request.args.get("termo", "").strip()
    modalidade = request.args.get("modalidade", "").strip()
    tipo_deficiencia = request.args.get("tipo_deficiencia", "").strip()

    if pesquisa:
        pesquisa_minuscula = pesquisa.lower()

        vagas = [
            vaga for vaga in vagas
            if pesquisa_minuscula in vaga.get("titulo", "").lower()
            or pesquisa_minuscula in vaga.get("empresa", "").lower()
            or pesquisa_minuscula in vaga.get("cidade", "").lower()
        ]

    if modalidade:
        vagas = [
            vaga for vaga in vagas
            if vaga.get("modalidade") == modalidade
        ]

    if tipo_deficiencia:
        vagas = [
            vaga for vaga in vagas
            if tipo_deficiencia in vaga.get("tipos_deficiencia", [])
        ]

    return render_template(
        "vagas.html",
        vagas=vagas,
        termo=pesquisa,
        modalidade=modalidade,
        tipo_deficiencia=tipo_deficiencia
    )


@app.route("/vagas/nova", methods=["GET", "POST"])
def cadastrar_vaga():
    if request.method == "POST":
        nova_vaga = {
            "id": str(uuid4()),
            "titulo": request.form.get("titulo", "").strip(),
            "empresa": request.form.get("empresa", "").strip(),
            "cidade": request.form.get("cidade", "").strip(),
            "estado": request.form.get("estado", "").strip(),
            "modalidade": request.form.get("modalidade", "").strip(),
            "tipo_contrato": request.form.get("tipo_contrato", "").strip(),
            "salario": request.form.get("salario", "").strip(),
            "contato": request.form.get("contato", "").strip(),
            "descricao": request.form.get("descricao", "").strip(),
            "requisitos": request.form.get("requisitos", "").strip(),
            "beneficios": request.form.get("beneficios", "").strip(),
            "tipos_deficiencia": request.form.getlist("tipos_deficiencia")
        }

        campos_obrigatorios = [
            nova_vaga["titulo"],
            nova_vaga["empresa"],
            nova_vaga["cidade"],
            nova_vaga["modalidade"],
            nova_vaga["contato"],
            nova_vaga["descricao"]
        ]

        if not all(campos_obrigatorios):
            flash("Preencha todos os campos obrigatórios.", "danger")

            return render_template(
                "cadastrar.html",
                dados=nova_vaga
            )

        vagas = carregar_vagas()
        vagas.append(nova_vaga)
        salvar_vagas(vagas)

        flash("Vaga cadastrada com sucesso!", "success")

        return redirect(url_for("listar_vagas"))

    return render_template("cadastrar.html", dados={})


@app.route("/vagas/<vaga_id>")
def detalhes_vaga(vaga_id):
    vaga = buscar_vaga_por_id(vaga_id)

    if vaga is None:
        flash("Vaga não encontrada.", "warning")
        return redirect(url_for("listar_vagas"))

    return render_template("detalhes.html", vaga=vaga)


@app.route("/vagas/<vaga_id>/editar", methods=["GET", "POST"])
def editar_vaga(vaga_id):
    vagas = carregar_vagas()

    vaga = next(
        (vaga for vaga in vagas if vaga.get("id") == vaga_id),
        None
    )

    if vaga is None:
        flash("Vaga não encontrada.", "warning")
        return redirect(url_for("listar_vagas"))

    if request.method == "POST":
        vaga["titulo"] = request.form.get("titulo", "").strip()
        vaga["empresa"] = request.form.get("empresa", "").strip()
        vaga["cidade"] = request.form.get("cidade", "").strip()
        vaga["estado"] = request.form.get("estado", "").strip()
        vaga["modalidade"] = request.form.get("modalidade", "").strip()
        vaga["tipo_contrato"] = request.form.get("tipo_contrato", "").strip()
        vaga["salario"] = request.form.get("salario", "").strip()
        vaga["contato"] = request.form.get("contato", "").strip()
        vaga["descricao"] = request.form.get("descricao", "").strip()
        vaga["requisitos"] = request.form.get("requisitos", "").strip()
        vaga["beneficios"] = request.form.get("beneficios", "").strip()

        vaga["tipos_deficiencia"] = request.form.getlist(
            "tipos_deficiencia"
        )

        campos_obrigatorios = [
            vaga["titulo"],
            vaga["empresa"],
            vaga["cidade"],
            vaga["modalidade"],
            vaga["contato"],
            vaga["descricao"]
        ]

        if not all(campos_obrigatorios):
            flash("Preencha todos os campos obrigatórios.", "danger")
            return render_template("editar.html", vaga=vaga)

        salvar_vagas(vagas)

        flash("Vaga atualizada com sucesso!", "success")

        return redirect(
            url_for("detalhes_vaga", vaga_id=vaga_id)
        )

    return render_template("editar.html", vaga=vaga)


@app.route("/vagas/<vaga_id>/excluir", methods=["POST"])
def excluir_vaga(vaga_id):
    vagas = carregar_vagas()

    quantidade_antes = len(vagas)

    vagas = [
        vaga for vaga in vagas
        if vaga.get("id") != vaga_id
    ]

    if len(vagas) == quantidade_antes:
        flash("Vaga não encontrada.", "warning")
    else:
        salvar_vagas(vagas)
        flash("Vaga excluída com sucesso!", "success")

    return redirect(url_for("listar_vagas"))


@app.route("/sobre")
def sobre():
    return render_template("sobre.html")


@app.route("/acessibilidade")
def acessibilidade():
    recursos = [
        "Aumento e redução do tamanho da fonte",
        "Modo de alto contraste",
        "Navegação pelo teclado",
        "Layout responsivo",
        "Textos alternativos nas imagens",
        "Formulários com identificação",
        "HTML semântico",
        "Botões e links de fácil identificação"
    ]

    return render_template(
        "acessibilidade.html",
        recursos=recursos
    )


@app.errorhandler(404)
def pagina_nao_encontrada(erro):
    return render_template("404.html"), 404


def abrir_site():
    webbrowser.open("http://127.0.0.1:5000/")


if __name__ == "__main__":
    Timer(1.5, abrir_site).start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=True,
        use_reloader=False
    )