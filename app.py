from flask import Flask, render_template, jsonify, request
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.get_json()
    senha = dados["senha"]

    pontos = 0

    # Tamanho da senha
    if len(senha) >= 8:
        pontos += 20

    if len(senha) >= 12:
        pontos += 10

    # Verificações
    if re.search(r'[A-Z]', senha):
        pontos += 20

    if re.search(r'[0-9]', senha):
        pontos += 20

    if re.search(r'[!@#$%^&*]', senha):
        pontos += 30

    # Classificação
    if pontos <= 30:
        nivel = "fraca"
    elif pontos <= 60:
        nivel = "media"
    elif pontos <= 80:
        nivel = "forte"
    else:
        nivel = "muito forte"

    return jsonify({
        "pontos": pontos,
        "nivel": nivel,
        "tem_maiuscula": bool(re.search(r'[A-Z]', senha)),
        "tem_numero": bool(re.search(r'[0-9]', senha)),
        "tem_simbolo": bool(re.search(r'[!@#$%^&*]', senha))
    })

if __name__ == "__main__":
    app.run(debug=True)