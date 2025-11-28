from flask import Flask, request, jsonify
from tinydb import TinyDB

app = Flask(__name__)
queue_db = TinyDB("data/fila.json")

@app.post("/queue/enviar")
def enviar_evento():
    data = request.json
    queue_db.insert(data)
    return jsonify({"status": "enfileirado", "dados": data})
    
if __name__ == "__main__":
    app.run(port=5001, debug=True)
