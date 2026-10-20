# Calcula sus huellas y tamaños
from pathlib import Path
from hashlib import sha256

# Esta ruta se interpreta desde la raíz de bigdata-game.
# pathA = Path('data/intercambio/envio/partida_A.jsonl')
# pathB = Path('data/intercambio/envio/partida_B.jsonl')
# # La huella representa los bytes del archivo que acabamos de leer.
# huellaA = sha256(pathA.read_bytes()).hexdigest()
# huellaB = sha256(pathB.read_bytes()).hexdigest()
# print(pathA.name, pathA.stat().st_size, huellaA)
# print(pathB.name, pathB.stat().st_size, huellaB)

# # Alternativa: 
# # for path in (pathA, pathB):
# #     print(path.name, path.stat().st_size, sha256(path.read_bytes()).hexdigest())

# # Comprueba que las dos huellas coinciden aunque los nombres sean diferentes
# assert huellaA == huellaB, 'Las huellas de partida_A y partida_B no coinciden'

# Cambio: event-index 16 amount delta de 4 a 5 en partida_A

# COMPROBAR DATOS RECIBIDOS ------------------------------------------------
pathAReceived = Path('data/intercambio/recibido/partida_A.jsonl')
pathBReceived = Path('data/intercambio/recibido/partida_B.jsonl')

# El receptor adapta su script para recorrer los dos archivos recibidos y comparar cada huella actual con la referencia correspondiente. Las huellas esperadas pueden guardarse en un diccionario de Python, con el nombre de archivo como clave.
expected_hashes = {
    'partida_A.jsonl': '2417b7d4d90b8c804c8f2556d1236e24e84211bcddf3342f34f7ad91d95432bb',
    'partida_B.jsonl': '2417b7d4d90b8c804c8f2556d1236e24e84211bcddf3342f34f7ad91d95432bb',
}

received_hashes = {
    path.name: sha256(path.read_bytes()).hexdigest()
    for path in (pathAReceived, pathBReceived)
}

# Debe mostrar para cada archivo:
# - Nombre y tamaño recibido.
# - Huella esperada y huella calculada.
# - `COINCIDE` o `NO COINCIDE`.
# Si falta un archivo, indica `NO RECIBIDO`;

for name, expected_hash in expected_hashes.items():
    received_hash = received_hashes.get(name)
    if received_hash is None:
        print(f'Archivo {name} no recibido')
        continue

    size = Path('data/intercambio/recibido') / name

    print(f'Archivo: {name}, Tamaño: {size.stat().st_size} bytes')
    print(f'Huella esperada: {expected_hash}')
    print(f'Huella recibida: {received_hash}')
    if expected_hash == received_hash:
        print('Resultado: COINCIDE\n')
    else:
        print('Resultado: NO COINCIDE\n')