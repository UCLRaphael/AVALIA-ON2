from flask import Flask, request, jsonify
from tinydb import TinyDB, Query
from filaPedidos import fila_pedidos

app = Flask(__name__)

@app.route('/api/pesquisaProduto', methods=['POST'])
def pesquisa_produto():
    # Verifica se o corpo da requisição é JSON
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 400

    dados = request.get_json()  # Lê o JSON enviado

    db = TinyDB('banco.json')
    produtos = db.table('produtos')
    
    # produtos.insert(dados)

    todos = produtos.all()
    # produto_query = dados.get('produto', '')
    # print(produto_query)
    # Produtos = Query()

    # # RESOLVER AQUI A LÓGICA DE PESQUISA
    # TODO: Implementar a lógica de pesquisa conforme necessário
    #https://tinydb.readthedocs.io/en/latest/
    # resultado = db.search(Produtos.nome == produto_query)
    # resposta = {
    #     "mensagem": "JSON recebido com sucesso!",
    #     "dados_recebidos": dados,
    #     "resultado_pesquisa": resultado,
    #     "total": todos
    # }

    return jsonify(todos), 200

@app.route('/api/realizarPedido', methods=['POST'])
def realizar_pedido():
    if not request.is_json:
        return jsonify({"erro": "O corpo da requisição deve ser JSON"}), 400

    dados = request.get_json()

    fila_pedidos.put(dados)

    resposta = {
        "mensagem": "Pedido realizado com sucesso!",
        "dados_recebidos": dados
    }

    return jsonify(resposta), 200   

if __name__ == '__main__':
    app.run(debug=True)
