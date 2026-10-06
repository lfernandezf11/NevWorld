from pathlib import Path

import pandas as pd


DATASET = Path(
    'data/raw/nevworld_13735864442874539122_20261005_182756.jsonl'
)

if not DATASET.exists():
    raise FileNotFoundError(
        f'No se encuentra: {DATASET.resolve()}'
    )

df = pd.read_json(DATASET, lines=True)


'Tamaño del dataset'
filas, columnas = df.shape
print('\nTAMAÑO DEL DATASET')
print('Número total de eventos:', filas)
print('Número total de columnas:', columnas)

'Nombres de las columnas'
print('\nNOMBRES DE LAS COLUMNAS')
print(df.columns.tolist())

'Eventos registrados'
print('\nEVENTOS REGISTRADOS')
print('\nTipo del primer evento registrado:', df['type'].iloc[0])
print('\nEvento más frecuente registrado y cantidad:', df['type'].value_counts().iloc[0])
print('\nRecuento de todos los tipos de eventos registrados:', df['type'].value_counts())

'DATOS DE SESIÓN'
print('\nDATOS DE SESIÓN')
'run_id, semilla y versión del esquema de la primera fila'
print('\nrun_id de la primera fila:', df['run_id'].iloc[0])
print('semilla de la primera fila:', df['seed'].iloc[0])
print('versión del esquema de la primera fila:', df['schema_version'].iloc[0])

'Extremos de los ticks'
print('\nTick mínimo:', df['tick'].min())
print('Tick máximo:', df['tick'].max())

'Validación básica del dataset'
assert not df.empty, 'El dataset está vacío'
required = [
    'run_id', 'event_index', 'tick', 'type'
]

assert all(column in df.columns for column in required), \
    'Faltan columnas principales'
assert not df.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados'

ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, \
    'Los ticks retroceden'

print('\nVALIDACIÓN BÁSICA: OK')