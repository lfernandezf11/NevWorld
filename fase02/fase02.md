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


```powershell
python scripts/actividades/02_parte_caza.py
```

## 4. Detecta las conclusiones que los datos no sostienen

Responde justificando cada decisión:

1. «Hay seis filas, por tanto hay seis cazadores distintos». ¿Es necesariamente cierto?
2. «Una fila indica que ese aldeano estuvo cazando durante todo el día». ¿Qué registra realmente la fila?
3. «Borro del DataFrame original todas las filas con algún `NaN` y después selecciono las cacerías». ¿Por qué puede desaparecer información válida?
4. «El CSV está vacío, así que nadie intentó cazar». ¿Qué puedes afirmar realmente sobre el registro?

## Ampliación para l@s más rápid@s: obras que no llegaron a terminar

Diseña `construction_incidents.csv` para consultar **dónde y cuándo se registraron obras abandonadas o caducadas, conservando el motivo registrado**.

Investiga `construction_abandoned` y `construction_expired`. Esta vez necesitas dos tipos de evento en una tabla y debes conservar `type` para distinguirlos. Comprueba en el RAW si esos eventos incluyen `building_id` antes de darlo por supuesto.

Pista para filtrar varios tipos:

```python
mask = df['type'].isin(['TIPO_A', 'TIPO_B'])
```

Justifica las columnas, exporta sin índice y verifica el recuento. Explica por qué dos registros con las mismas coordenadas no demuestran, por sí solos, que se trate de la misma obra.

## Entrega y valoración

Mismos pasos que la Actividad 1. Entrega el script, `hunts.csv` y una ficha con el ejemplo RAW, tus decisiones de diseño, las comprobaciones y las cuatro respuestas. Si haces el reto, incluye también su CSV y justificación.