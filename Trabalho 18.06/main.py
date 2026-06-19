from flask import Flask, render_template, request, redirect, session
from threading import Timer
import webbrowser

app = Flask(__name__)
app.secret_key = "abc123"

usuarios = {}
recados = []

@app.route("/")
def inicio():
    if "usuario" not in session:
        return redirect("/login")
    return render_template(
        "index.html",
        usuario=session["usuario"],
        recados=recados
    )

@app.route("/login", methods=["GET","POST"])
def login():
    erro=""
    nome=""

    if request.method=="POST":
        nome=request.form["nome"]
        senha=request.form["senha"]

        if nome in usuarios and usuarios[nome]==senha:
            session["usuario"]=nome
            return redirect("/")

        erro="Nome ou senha incorretos."

    return render_template("login.html",erro=erro,nome=nome)

@app.route("/criar", methods=["GET","POST"])
def criar():
    erro=""

    if request.method=="POST":
        nome=request.form["nome"]
        senha=request.form["senha"]

        if nome in usuarios:
            erro="Usuário já existe"
        else:
            usuarios[nome]=senha
            return redirect("/login")

    return render_template("criar.html",erro=erro)

@app.route("/recado", methods=["POST"])
def recado():
    if "usuario" not in session:
        return redirect("/login")

    recados.append({
        "nome":session["usuario"],
        "mensagem":request.form["mensagem"]
    })

    return redirect("/")

@app.route("/apagar/<int:id>")
def apagar(id):
    if id < len(recados):
        recados.pop(id)

    return redirect("/")

@app.route("/sair")
def sair():
    session.clear()
    return redirect("/login")

def abrir():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    Timer(1, abrir).start()
    app.run(debug=True, use_reloader=False)