from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

QUEUE_URL = "http://localhost:5001/queue/enviar"

produtos = []

@app.post("/produtos")
def criar_produto():
    produto = request.json
    produtos.append(produto)

    # envia evento para fila
    requests.post(QUEUE_URL, json={
        "tipo": "produto_criado",
        "dados": produto
    })

    return jsonify(produto)

@app.get("/produtos")
def listar():
    return jsonify(produtos)

if __name__ == "__main__":
    app.run(port=5002, debug=True)
