from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/cadastro', methods=['GET', 'POST'])
def cadastro():
    mensagem = ""

    if request.method == 'POST':
        nickname = request.form.get('nickname')
        jogo = request.form.get('jogo')
        email = request.form.get('email')

        if not nickname or not jogo or not email:
            mensagem = "Preencha todos os campos obrigatórios."
        elif len(nickname) < 4:
            mensagem = "Preencha todos os campos obrigatórios."
        else:
            mensagem = "Inscrição realizada com sucesso!"

    return render_template('cadastro.html', mensagem=mensagem)

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/validacao', methods=['POST'])
def cadastro():

    nome = request.form.get('nome', '' ).strip().title()
    email = request.form.get('email', '').strip().lower()
    cidade = request.form.get('cidade', '').strip().title()

    return f"""
    Nome: {nome}<br>
    Email: {email}<br>
    Cidade: {cidade}
    """

if __name__ == '__main__':
    app.run(debug=True)