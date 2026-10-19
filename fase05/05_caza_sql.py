from pathlib import Path

import duckdb
import pandas as pd


DATA_DIR = Path('data/processed')
PARQUET_DIR = DATA_DIR / 'parquet'
PARQUET_DIR.mkdir(exist_ok=True)

hunts = pd.read_csv(DATA_DIR / 'hunts.csv')
hunts.to_parquet(PARQUET_DIR / 'hunts.parquet', engine='pyarrow', index=False)

print('Hunts')
print('  CSV:', (DATA_DIR / 'hunts.csv').stat().st_size, 'bytes')
print('  Parquet:', (PARQUET_DIR / 'hunts.parquet').stat().st_size, 'bytes')

# Comprueba que existe prey_type y que ninguna cacería tiene esa columna sin informar. No borres registros para ocultar errores
assert 'prey_type' in hunts.columns, \
    "Falta la columna obligatoria 'prey_type' en hunts.csv"

prey_values = hunts['prey_type'].astype('string').str.strip()

assert prey_values.notna().all() and prey_values.ne('').all(), \
    'Hay cacerías sin presa informada en hunts.csv'

connection = duckdb.connect()

if hunts.empty:
    print('\nNo hay cacerías completadas registradas.')
    hunt_summary = pd.DataFrame(columns=['prey_type', 'hunt_count']) # guarda las cabeceras sin datos
else:
    hunt_query = """
        SELECT
            prey_type,
            COUNT(*) AS hunt_count
        FROM read_parquet('data/processed/parquet/hunts.parquet')
        GROUP BY prey_type
        ORDER BY hunt_count DESC
    """

    hunt_summary = connection.execute(
        hunt_query
    ).fetchdf()

    assert hunt_summary['hunt_count'].sum() == len(hunts), \
    'El número total de cacerías en la consulta SQL no coincide con el número de registros en hunts.csv'

print('\nCACERÍAS POR TIPO DE PRESA')
print(hunt_summary)

Path('reports').mkdir(exist_ok=True)

hunt_summary.to_csv( # guardado en csv
    'reports/hunts_by_prey_sql.csv',
    index=False,
)

connection.close()