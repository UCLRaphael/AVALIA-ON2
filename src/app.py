from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from queue import Queue

app = Flask(__name__)

# FILA TEMPORÁRIA (Fila "entrada")
fila_eventos = Queue()

# BANCO (processados)
db = TinyDB('data/banco.json')
pedidos_table = db.table('pedidos')


# ------------------------------
# 1) Cliente envia evento (POSTMAN)
# ------------------------------
@app.route('/api/realizarPedido', methods=['POST'])
def realizar_pedido():
    if not request.is_json:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    dados = request.get_json()

    # Enfileira evento (microserviço A)
    fila_eventos.put(dados)

    return jsonify({
        "mensagem": "Pedido recebido e colocado na fila",
        "evento": dados
    }), 200


# ------------------------------
# 2) Processador ("Lambda") pega da fila
# ------------------------------
@app.route('/api/processar', methods=['POST'])
def processar_fila():
    resultados = []

    # Processar tudo o que tem na fila
    while not fila_eventos.empty():
        evento = fila_eventos.get()

        # salva no banco (microserviço B)
        pedidos_table.insert(evento)

        resultados.append(evento)

    return jsonify({
        "mensagem": "Eventos processados com sucesso",
        "processados": resultados
    }), 200


# ------------------------------
# 3) Pesquisa de pedidos no banco
# ------------------------------
@app.route('/api/pesquisaPedido', methods=['POST'])
def pesquisa_pedido():
    if not request.is_json:
        return jsonify({"erro": "Envie um JSON válido"}), 400

    dados = request.get_json()
    campo = dados.get("campo")
    valor = dados.get("valor")

    if not campo or not valor:
        return jsonify({"erro": "Envie {campo, valor}"}), 400

    Q = Query()
    resultado = pedidos_table.search(Q[campo] == valor)

    return jsonify({
        "resultado": resultado,
        "total_encontrado": len(resultado)
    })


# ------------------------------
# Início
# ------------------------------
if __name__ == '__main__':
    app.run(debug=True)
