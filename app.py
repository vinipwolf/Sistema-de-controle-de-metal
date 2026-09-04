from flask import Flask, render_template, request
from banco import consultar_estoque, cadastrar_cliente

app = Flask(__name__)

@app.route("/")
def inicio():
    return render_template("index.html")

@app.route("/estoque")
def estoque():
    dados_estoque = consultar_estoque()

    return render_template("estoque.html", estoque=dados_estoque)

@app.route("/cadastrar-cliente", methods=["GET", "POST"])
def cadastrar_cliente_web():
    if request.method == "POST":
        nome = request.form["nome"]

        id_cliente = cadastrar_cliente(nome)

        if id_cliente is not None:
            return f"Cliente cadastrado com sucesso! ID: {id_cliente}"

        return "Erro ao cadastrar cliente."

    return render_template("cadastrar_cliente.html")

if __name__ == "__main__":
    app.run(debug=True)