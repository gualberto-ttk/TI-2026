from flask import Flask, render_template
import webbrowser
import threading

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/pizzaria/<sabor>")
def pizzaria(sabor):

    if sabor == "calabresa":
        nome = "Pizza de Calabresa"
        foto = "calabresa.jpg"

    elif sabor == "margherita":
        nome = "Pizza Margherita"
        foto = "margherita.jpg"

    elif sabor == "frango":
        nome = "Pizza de Frango"
        foto = "frango.jpg"

    else:
        return "<h1>Sabor não disponível</h1><a href='/'>Voltar</a>"

    return render_template("pizza.html", nome=nome, foto=foto)

def abrir():
    webbrowser.open("http://127.0.0.1:5000")

if __name__ == "__main__":
    threading.Timer(1, abrir).start()
    app.run(debug=True)