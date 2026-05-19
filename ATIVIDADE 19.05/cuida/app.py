from flask import Flask, render_template
import webbrowser

app = Flask(__name__)

# alguns lanches do sistema
lanches = {

    "pizza": {
    "nome": "Pizza 🍕",
    "preco": "R$ 45",
    "descricao": "Pizza artesanal com queijo.",
    "imagem": "pizza.jpg",
    "mensagem": "A favorita da galera."
    },

    "x-burguer": {
    "nome": "X-Burguer 🍔",
    "preco": "R$ 30",
    "descricao": "Hambúrguer com queijo e molho.",
    "imagem": "burguer.jpg",
    "mensagem": "Muito bom 😋"
    },

    "batata": {
    "nome": "Batata 🍟",
    "preco": "R$ 18",
    "descricao": "Batata frita crocante.",
    "imagem": "batata.jpg",
    "mensagem": "Combina com tudo."
    },

    "milkshake": {
    "nome": "Milkshake 🥤",
    "preco": "R$ 20",
    "descricao": "Milkshake cremoso de chocolate.",
    "imagem": "milkshake.jpg",
    "mensagem": "Bem geladinho."
    }
}


# pedidos fictícios
pedidos = [

{"cliente": "Ana", "pedido": "Pizza", "valor": "R$ 45"},

{"cliente": "Pedro", "pedido": "X-Burguer", "valor": "R$ 30"},

{"cliente": "Lucas", "pedido": "Milkshake", "valor": "R$ 20"}

]


# página inicial
@app.route("/")
def index():

 return render_template("index.html")


# página do cardápio
@app.route("/cardapio")
def cardapio():

    return render_template(
       "cardapio.html",
        lanches=lanches
    )


# rota dinâmica dos lanches
@app.route("/lanche/<nome>")
def lanche(nome):

    item = lanches.get(nome.lower())

    return render_template(
        "lanche.html",
        item=item,
        nome=nome
    )


# página de pedidos
@app.route("/pedidos")
def pedidos_page():

    return render_template(
        "pedidos.html",
        pedidos=pedidos
    )


# cliente e cidade
@app.route("/cliente/<nome>/<cidade>")
def cliente(nome, cidade):

    entrega_disponivel = False

    if cidade.lower() == "natal":
        entrega_disponivel = True

    return render_template(
        "cliente.html",
        nome=nome,
        cidade=cidade,
        entrega_disponivel=entrega_disponivel
    )


# contato
@app.route("/contato")
def contato():

    return render_template("contato.html")


if __name__ == "__main__":
    webbrowser.open("http://127.0.0.1:5000")
    app.run(debug=True)