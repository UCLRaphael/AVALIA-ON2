import time
from tinydb import TinyDB
from tinydb.storages import JSONStorage
from tinydb.middlewares import CachingMiddleware

fila = TinyDB("data/fila.json", storage=CachingMiddleware(JSONStorage))
banco = TinyDB("data/banco.json", storage=CachingMiddleware(JSONStorage))

print("Lambda iniciada...")

while True:
    eventos = fila.all()

    if eventos:
        print(f"Processando {len(eventos)} eventos...")

        for evento in eventos:
            banco.insert(evento)

        fila.truncate()

    time.sleep(3)
