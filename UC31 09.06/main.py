from flask import Flask, render_template, request
import webbrowser
from threading import Timer

app = Flask(__name__)

@app.route("/")
def inicio():
    nome = request.cookies.get("nome")
    tema = request.cookies.get("tema", "claro")
    return render_template("inicio.html", nome=nome, tema=tema)

if __name__ == "__main__":
    Timer(1, lambda: webbrowser.open("http://127.0.0.1:5000")).start()
    app.run(debug=True, use_reloader=False)