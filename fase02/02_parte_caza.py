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

# Consulta de eventos registrados
print('\nRecuento de todos los tipos de eventos registrados:', df['type'].value_counts())
# Registro de caza en dataset raw_data
