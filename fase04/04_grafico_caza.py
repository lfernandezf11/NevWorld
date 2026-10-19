from pathlib import Path

import matplotlib.pyplot as plt
import pandas as pd


DATA_DIR = Path('data/processed')
CHARTS_DIR = Path('reports/charts')
CHARTS_DIR.mkdir(parents=True, exist_ok=True)

hunts = pd.read_csv(DATA_DIR / 'hunts.csv')

# VALIDACIONES BÁSICAS ---------------------------------------------------------
required_for_hunts = [
    'run_id', 'event_index', 'tick', 'villager_id', 'prey_type', 'simulation_day'
]

assert all(column in hunts.columns for column in required_for_hunts), \
    'Faltan columnas obligatorias en hunts.csv'
assert not hunts.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos de caza duplicados'
assert not hunts[required_for_hunts].isna().any().any(), \
    'Hay valores ausentes en columnas necesarias de hunts.csv'

if hunts.empty:
    print('\nNo hay cacerías completadas registradas. No se generará el gráfico.')
else:
    prey_counts = hunts['prey_type'].value_counts()

    plt.figure(figsize=(8, 4))

    prey_counts.plot.bar(color='steelblue')
    plt.title('Cacerías completadas registradas por tipo de presa')
    plt.xlabel('Tipo de presa')
    plt.ylabel('Número de cacerías registradas')

    plt.xticks(rotation=30, ha='right')

    plt.tight_layout()
    plt.savefig(CHARTS_DIR / '05_hunts_by_prey.png')
    plt.close()
