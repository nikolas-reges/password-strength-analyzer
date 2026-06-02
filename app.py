from flask import Flask, render_template, jsonify, request
from zxcvbn import zxcvbn
import re

app = Flask(__name__)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/analisar", methods=["POST"])
def analisar():
    dados = request.get_json()
    senha = dados.get("senha", "")

    # Análise REAL com o algoritmo zxcvbn
    resultado = zxcvbn(senha)
    score = resultado["score"]  # Retorna de 0 (muito fraca) a 4 (muito forte)

    # Converte o score numérico para o nível em texto
    niveis = {0: "fraca", 1: "fraca", 2: "media", 3: "forte", 4: "muito forte"}
    nivel = niveis.get(score, "fraca")

    # Calcula uma porcentagem aproximada para a barra de progresso do seu HTML
    pontos = int((score / 4) * 100) if senha else 0

    # Dicas reais de segurança geradas pelo algoritmo (Tradução rápida)
    feedback = resultado["feedback"]["suggestions"]
    aviso = resultado["feedback"]["warning"]

    return jsonify({
        "pontos": pontos,
        "nivel": nivel,
        "tem_maiuscula": bool(re.search(r'[A-Z]', senha)),
        "tem_numero": bool(re.search(r'[0-9]', senha)),
        "tem_simbolo": bool(re.search(r'[!@#$%^&*]', senha)),
        "tempo_cracking": resultado["crack_times_display"]["offline_fast_hashing_1e10_per_second"],
        "sugestoes": feedback,
        "aviso": aviso
    })

if __name__ == "__main__":
    app.run(debug=True, port=5002)