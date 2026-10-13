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

# Crear la tabla de cazas
hunts = event_table('hunt_completed', ['villager_id', 'prey_type'])

# VALIDACIONES ---------------------------
# 1. El número de filas coincide con el número de eventos del tipo elegido
assert (df['type'] == 'hunt_completed').sum() == len(hunts), \
    'No se registraron todas las cazas'

# 2.No se repite la pareja run_id, event_index.
assert not hunts.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos duplicados'

# 3. Los campos obligatorios no tienen celdas ausentes.
required = [
    'run_id', 'event_index', 'tick', 'villager_id', 'prey_type'
]
if not hunts.empty:
    assert hunts[required].notna().all().all(), \
    'Hay celdas ausentes en las columnas obligatorias'

    # 4. simulation_day coincide con la división entera indicada
    assert (hunts['simulation_day'] == hunts['tick'] // 12000).all(), \
        'simulation_day no coincide con tick // 12000'

print('\nVALIDACIÓN BÁSICA DE CAZAS: OK')

# Después de la validación, guardar el CSV sin exportar el índice de pandas
output = OUTPUT_DIR / 'hunts.csv'
hunts.to_csv(output, index=False)

# Mostrar la ruta del archivo generado y su numero de filas
print(f'\nArchivo generado: {output.resolve()}')
print(f'Número de filas: {len(hunts)}')