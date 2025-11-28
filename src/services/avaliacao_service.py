from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

QUEUE_URL = "http://localhost:5001/queue/enviar"
avaliacoes = []

@app.post("/avaliar")
def avaliar():
    avaliacao = request.json
    avaliacoes.append(avaliacao)

    requests.post(QUEUE_URL, json={
        "tipo": "avaliacao_registrada",
        "dados": avaliacao
    })

    return jsonify(avaliacao)

@app.get("/avaliacoes")
def listar():
    return jsonify(avaliacoes)

if __name__ == "__main__":
    app.run(port=5004, debug=True)
