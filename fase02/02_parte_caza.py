from pathlib import Path

import pandas as pd

DATASET = Path(
    'data/raw/nevworld_13735864442874539122_20261005_182756.jsonl'
)

if not DATASET.exists():
    raise FileNotFoundError(
        f'No se encuentra: {DATASET.resolve()}'
    )

# Crear directorio de salida
OUTPUT_DIR = Path('data/processed')
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Leer el RAW
df = pd.read_json(DATASET, lines=True)

# Consultar eventos registrados
print('\nRecuento de tipos de eventos registrados')
print(df['type'].value_counts())


def event_table(event_type, columns):
    # Conservar run_id, event_index y tick
    selected = ['run_id', 'event_index', 'tick', *columns]

    output_columns = [*selected, 'simulation_day']
    available = [
            column for column in selected
            if column in df.columns
        ]
    table = df.loc[
        df['type'] == event_type,
        available,
    ].copy()

    # Anadir simulation_day mediante tick // 12000

    if 'tick' in table.columns:
        table['simulation_day'] = table['tick'] // 12000

    # Conserva ese orden y crea con valores vacios las columnas que falten.
    return table.reindex(columns=output_columns)

# Crear la tabla de cazas y generar el CSV
hunts = event_table('hunt_completed', ['villager_id', 'prey_type'])

output = OUTPUT_DIR / 'hunts.csv'
hunts.to_csv(output, index=False)

# Mostrar la ruta del archivo generado y su numero de filas
print(f'\nArchivo generado: {output.resolve()}')
print(f'Número de filas: {len(hunts)}')

# Validación básica del dataset
assert not df.empty, 'El dataset está vacío'
required = [
    'run_id', 'event_index', 'tick', 'type', 'villager_id', 'prey_type'
]

# Comprobar que el número de filas coincide con el númro de eventos del tipo elegido
# Cuenta cuántas filas cumplen una condición.
assert (df['type'] == 'hunt_completed').sum() == len(hunts), 'No se registraron todas las cazas'
# Comprueba que los campos obligatorios no tengan celdas ausentes.
if not hunts.empty:
    assert all(column in hunts.columns for column in required), \
        'Faltan columnas principales'

assert hunts[required].notna().all().all()
assert all(column in df.columns for column in required), \
    'Faltan columnas principales'
assert not df.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados'

ordered = df.sort_values('event_index')
assert ordered['tick'].is_monotonic_increasing, \
    'Los ticks retroceden'

print('\nVALIDACIÓN BÁSICA: OK')
