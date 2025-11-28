from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

QUEUE_URL = "http://localhost:5001/queue/enviar"

compras = []

@app.post("/comprar")
def comprar():
    compra = request.json
    compras.append(compra)

    requests.post(QUEUE_URL, json={
        "tipo": "compra_realizada",
        "dados": compra
    })

    return jsonify(compra)

@app.get("/compras")
def listar():
    return jsonify(compras)

if __name__ == "__main__":
    app.run(port=5003, debug=True)
