# El parte de caza: Del registro a una tabla útil
El evento que registra una cacería es del tipo `hunt_completed`.

Como ejemplo ilustrativo tomaremos el siguiente registro del dataset original: 
`{"schema_version":2,"run_id":"20261005_182756_13735864442874539122_8c0b492d4b8c4cf0847993511f08579b","seed":"13735864442874539122","event_index":90,"tick":2826,"type":"hunt_completed","villager_id":1403,"prey_type":"deer"}`

Completa esta ficha **antes de escribir la llamada a `event_table()`**:

| Pregunta | Campo o valor elegido | Justificación |
| --- | --- | --- |
| ¿Qué evento demuestra que la cacería terminó? | `hunt_completed` | Se traduce como 'cacería completada' |
| ¿Quién la completó? | `villager_id` | Identifica de forma única a un aldeano |
| ¿Qué presa aparece registrada? | `prey_type` | Se traduce como 'tipo de presa' |
| ¿Cuándo ocurrió? | `tick`| Tick es un contador de tiempo de la simulación |
| ¿A qué partida pertenece? | `run_id`| Es el identificador único de la ejecución recogida |
| ¿Cómo localizo el evento original sin confundirlo con otro? | `run_id` y `event-index` | Identifica la partida y la posición del evento dentro de la partida |

Explica también por qué `activity`, `food_stock` y `amount_delta` no son necesarios para este parte. ¿Permite el evento saber por sí solo cuánta comida produjo la cacería?

Estos campos no son necesarios porque no atañen a este tipo de evento, sino a `villager_activity_changed`, `world_snapshot` y `resource_changed`, respectivamente.

El evento por sí solo no permite saber qué cantidad de comida se ha producido.

## 3. Demuestra que funciona
Abre el CSV exportado. Elige dos filas —o todas si hay menos de dos— y localiza sus eventos originales mediante `run_id` y `event_index`. Comprueba aldeano, presa y tick. Anota la comparación; si no hay filas, explica qué has podido comprobar y qué no.

Los datos RAW y los procesados coinciden.

```powershell
python NevWorld/fase02/02_parte_caza.py
```

## 4. Detecta las conclusiones que los datos no sostienen

Responde justificando cada decisión:

1. «Hay seis filas, por tanto hay seis cazadores distintos». ¿Es necesariamente cierto?

Un único cazador puede completar varias cazas.

2. «Una fila indica que ese aldeano estuvo cazando durante todo el día». ¿Qué registra realmente la fila?

La fila registra que una caza fue completada, no el tiempo de la actividad.

3. «Borro del DataFrame original todas las filas con algún `NaN` y después selecciono las cacerías». ¿Por qué puede desaparecer información válida?

NaN no implica necesariamente que el dato sea inválido o incorrecto.

4. «El CSV está vacío, así que nadie intentó cazar». ¿Qué puedes afirmar realmente sobre el registro?

Nadie completó una cacería, pero no sabemos si intentó cazar.

## Ampliación para l@s más rápid@s: obras que no llegaron a terminar
Incluyo `cell_x` y `cell_y` porque son las coordenadas de las edificaciones y son propias de estos eventos. 

Justifica las columnas, exporta sin índice y verifica el recuento. Explica por qué dos registros con las mismas coordenadas no demuestran, por sí solos, que se trate de la misma obra.

## Entrega y valoración

Mismos pasos que la Actividad 1. Entrega el script, `hunts.csv` y una ficha con el ejemplo RAW, tus decisiones de diseño, las comprobaciones y las cuatro respuestas. Si haces el reto, incluye también su CSV y justificación.