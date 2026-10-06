# Radiografía de una partida de NevWorld

Has terminado una partida y el juego ha generado un archivo JSONL. Tu misión es abrirlo con pandas y preparar una ficha que permita a otra persona comprender qué contiene ese registro.

Utiliza **los datos de tu propia partida** y las operaciones vistas en el tema. No modifiques el archivo RAW.

## Teoría de apoyo

JSONL guarda un evento en cada línea. pandas lo carga con `pd.read_json(..., lines=True)` en un **DataFrame**, una tabla de filas y columnas. La variable `df` recibe ese nombre como abreviatura de DataFrame: cada fila representa un evento y cada columna, un campo.

| Para… | Utiliza… |
| --- | --- |
| Representar y comprobar la ruta | `Path(...)` y `exists()` |
| Ver los primeros eventos | `df.head()` |
| Obtener filas y columnas | `df.shape` |
| Consultar los nombres de los campos | `df.columns.tolist()` |
| Contar eventos de cada tipo | `df['type'].value_counts()` |
| Leer un valor de la primera fila | `df['campo'].iloc[0]` |
| Obtener los extremos de los ticks | `df['tick'].min()` y `max()` |

Los eventos pueden tener campos diferentes: un `NaN` representa una ausencia, no necesariamente un error ni un cero. El tick mide tiempo simulado; varios eventos pueden compartirlo.

## Enunciado

Crea `scripts/actividades/01_radiografia.py` en tu proyecto `bigdata-game`. Carga el JSONL que has guardado en `data/raw`, comprobando antes que la ruta existe. Puedes apoyarte en el script del tema.

Aplica las cuatro validaciones básicas del tema: que la tabla no esté vacía, que existan las columnas principales, que no se repita la pareja `run_id` y `event_index`, y que los ticks no retrocedan al ordenar por `event_index`. Hazlo antes de consultar la primera fila.

Después, muestra las primeras filas y obtén los datos necesarios para completar esta ficha:

| Dato de mi partida | Resultado |
| --- | --- |
| Nombre del archivo JSONL | `data/raw/nevworld_13735864442874539122_20261005_182756.jsonl` |
| Número total de eventos | 7722 |
| Número de columnas | 36 |
| Nombres de las columnas | `schema_version`<br>`run_id`<br>`seed`<br>`event_index`<br>`tick`<br>`type`<br>`started_at_utc`<br>`building_id`<br>`building_type`<br>`cell_x`<br>`cell_y`<br>`width`<br>`height`<br>`villager_id`<br>`activity`<br>`resource_type`<br>`population`<br>`constructed_buildings`<br>`wood_stock`<br>`food_stock`<br>`gold_stock`<br>`day`<br>`amount_before`<br>`amount_after`<br>`amount_delta`<br>`prey_type`<br>`actor_id`<br>`target_id`<br>`interaction_type`<br>`topic`<br>`relationship_actor_to_target_after`<br>`relationship_target_to_actor_after`<br>`need_type`<br>`state`<br>`cause`<br>`name` |
| Tipo del primer evento registrado | `simulation_started` |
| Tipo de evento más frecuente y cantidad | `villager_activity_changed`: 4995 |
| Recuento de todos los tipos de evento | `villager_activity_changed`: 4995<br>`world_snapshot`: 887<br>`villager_need_changed`: 749<br>`resource_changed`: 417<br>`social_interaction`: 283<br>`villager_drank`: 147<br>`villager_ate`: 112<br>`construction_abandoned`: 67<br>`hunt_completed`: 42<br>`construction_expired`: 11<br>`building_created`: 8<br>`villager_created`: 2<br>`simulation_started`: 1<br>`villager_died`: 1 |
| `run_id`, semilla y versión del esquema de la primera fila | `run_id`: `20261005_182756_13735864442874539122_8c0b492d4b8c4cf0847993511f08579b`<br>`semilla`: `1.373586444287454e+19`<br>`versión del esquema`: `2` |
| Tick mínimo y tick máximo | mín 0, máx 532228|
| Resultado de las validaciones | OK |

Termina la ficha respondiendo con tus palabras:

1. ¿Qué te permite afirmar el recuento sobre tu partida? ¿Por qué el tipo más frecuente no tiene que ser el más importante?
2. ¿Por qué una celda vacía no significa necesariamente que el registro esté mal?
3. ¿Qué sabes ahora del archivo y qué pregunta sobre tu partida necesitaría un análisis posterior?

Ejecuta desde la raíz de `bigdata-game`, con el entorno de Python que tenga pandas instalado:

```powershell
python NevWorld/fase01/01_radiografia.py
```

**Entrega:** Cread un repositorio en Github con una carpeta llamada NevWorld, y una subcarpeta llamada fase01, en la que incluiréis el script y la ficha en un archivo de texto, con tus respuestas y resultados reales. Si alguna validación falla, anota el error y explica qué comprobación no se cumple; no alteres el RAW para hacerla pasar.