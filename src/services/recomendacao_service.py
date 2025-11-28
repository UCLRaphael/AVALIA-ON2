from flask import Flask, jsonify
from tinydb import TinyDB, Query

app = Flask(__name__)
db = TinyDB("data/banco.json")

@app.get("/recomendacao/<usuario>")
def recomendar(usuario):
    registros = db.search(Query().dados.usuario == usuario)

    return jsonify({
        "usuario": usuario,
        "recomendacoes": registros
    })

if __name__ == "__main__":
    app.run(port=5005, debug=True)
