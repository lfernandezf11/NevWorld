from pathlib import Path

import pandas as pd

# Partimos de archivos ya procesados, no del RAW.
DATA_DIR = Path('data/processed')
REPORTS_DIR = Path('reports')
REPORTS_DIR.mkdir(exist_ok=True)

# Guarda en variables los DataFrames de cada tabla procesada (lo que pandas genera es Series, que es como una columna de una tabla).
resources = pd.read_csv(DATA_DIR / 'resources.csv')
hunts = pd.read_csv(DATA_DIR / 'hunts.csv')

# INFORME DE CAZAS -------------------------------------------------------------
if not hunts.empty:
    # Recuento de eventos de caza por tipo de presa
    prey_counts = hunts['prey_type'].value_counts()  # por defecto ordena de mayor a menor frecuencia
    prey_percent = (hunts['prey_type'].value_counts(normalize=True) * 100).round(1)
    hunts_per_day = hunts['simulation_day'].value_counts().sort_index()  # ordena por las etiquetas de la Series. Permite mostrar los días cronológicamente

    print('\n\nRESUMEN DEL PARTE DE CAZA')
    print('Total de eventos de caza registrados:', len(hunts))
    print('Recuento por tipo de presa, de mayor a menor frecuencia:', prey_counts)
    print('Porcentaje de cada tipo de presa, redondeado a un decimal:', prey_percent)
    print('Recuento por día de simulación, ordenado por día:', hunts_per_day)
else:
    print('\nNo hay cacerías completadas registradas.')



# CAMBIOS EN RECURSOS DE COMIDA ------------------------------------------------------
food = resources[resources['resource_type'] == 'food']

if not food.empty:
    # Número de eventos de cambio de comida
    food_change_events = len(food)

    # Balance neto
    food_net_change = food['amount_delta'].sum()

    # Incrementos de comida
    food_gains = food[food['amount_delta'] > 0]['amount_delta'].sum()

    # Decrementos de comida en términos absolutos
    food_reductions = food[food['amount_delta'] < 0].copy()
    food_reductions = food_reductions['amount_delta'].abs().sum()  # Convierte a positivo para mostrar la cantidad de comida gastada

    print('\n\nCAMBIOS EN RECURSOS DE COMIDA')
    print('Eventos de cambio de comida:', food_change_events)
    print('Incrementos registrados:', food_gains)
    print('Reducciones registradas:', food_reductions)
    print('Balance neto:', food_net_change)
else:
    print('\nNo hay cambios en los recursos de comida registrados.')


# VALIDACIONES BÁSICAS ---------------------------------------------------------
# 1. Existen las columnas obligatorias
required_for_hunts = [
    'run_id', 'event_index', 'tick', 'villager_id', 'prey_type', 'simulation_day'
]
required_for_resources = [
    'run_id', 'event_index', 'tick', 'resource_type', 'amount_delta'
]

assert all(column in hunts.columns for column in required_for_hunts), \
    'Faltan columnas obligatorias en hunts.csv'
assert all(column in resources.columns for column in required_for_resources), \
    'Faltan columnas obligatorias en resources.csv'

# 2. No hay valores duplicados 
assert not hunts.duplicated(['run_id', 'event_index']).any(), \
    'Hay eventos de caza duplicados'
assert not resources.duplicated(['run_id', 'event_index']).any(), \
    'Hay recursos duplicados'

# 3. No hay valores ausentes en los campos utilizados
if not hunts.empty:
    assert not hunts[required_for_hunts].isna().any().any(), \
        'Hay valores ausentes en columnas necesarias de hunts.csv'
if not resources.empty:
    assert not resources[required_for_resources].isna().any().any(), \
        'Hay valores ausentes en columnas necesarias de resources.csv'

# VALIDACIONES ADICIONALES ---------------------------------------------------------
# 1. La suma de los recuentos por presa coincide con el total de cacerías.
assert prey_counts.sum() == len(hunts), \
    'La suma de los recuentos por tipo de presa no coincide con el total de cacerías registradas'

# 2. La suma de los recuentos por día coincide con el total de cacerías.
assert hunts_per_day.sum() == len(hunts), \
    'La suma de los recuentos por día no coincide con el total de cacerías registradas'

# 3. Los incrementos menos las reducciones coinciden con el balance de comida
assert food_gains - food_reductions == food_net_change, \
    'El balance neto de comida no coincide con la diferencia entre incrementos y reducciones'

# 4. Los porcentajes sin redondear suman aproximadamente 100 con un margen de error de 0.000001
assert abs(hunts['prey_type'].value_counts(normalize=True).sum() - 1) < 0.000001, \
    'Los porcentajes de cada tipo de presa no suman aproximadamente 100'

# RESUMEN DE MÉTRICAS ----------------------------------------------------------
# 1. Total de cacerías completadas registradas.
# 2. Número de eventos de cambio de comida
# 3. Incrementos de comida registrados
# 4. Reducciones de comida, como cantidad positiva
# 5. Balance neto de comida
summary = pd.DataFrame([ 
    {'metric': 'hunt_events', 'value': len(hunts)},
    {'metric': 'food_change_events', 'value': len(food)},
    {'metric': 'food_gains', 'value': food_gains},
    {'metric': 'food_reductions', 'value': food_reductions},
    {'metric': 'food_net_change', 'value': food_net_change},
])

summary.to_csv(REPORTS_DIR / 'hunting_summary.csv', index=False)


# AMPLIACIÓN ------------------------------------------------
snapshots = pd.read_csv(DATA_DIR / 'snapshots.csv')

if not snapshots.empty:
    snapshots = snapshots.sort_values(['tick', 'event_index']) # orden por tick y event_index
    first_snapshot = snapshots.iloc[0]
    last_snapshot = snapshots.iloc[-1]

    food_stock_change = last_snapshot['food_stock'] - first_snapshot['food_stock']

    print('\n\nDIFERENCIA DE STOCK DE COMIDA SEGÚN SNAPSHOTS')
    print(f"Primer snapshot (tick {first_snapshot['tick']}): {first_snapshot['food_stock']} -> Último snapshot (tick {last_snapshot['tick']}): {last_snapshot['food_stock']}")
    print(f"Cambio neto en el stock de comida: {food_stock_change}")

    balance_difference = food_net_change - food_stock_change
    print(f"Diferencia entre el balance neto de comida y el cambio en el stock de comida según snapshots: {balance_difference}")