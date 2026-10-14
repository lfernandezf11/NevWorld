# El informe de caza: de las tablas a las conclusiones

| Pregunta | Tabla y columnas necesarias | Operación y motivo |
| --- | --- | --- |
| ¿Cuántas cacerías completadas se registraron? | `hunts`: una fila por cada cacería completada | `len(hunts)`, porque cuenta cuántas filas/cacerías hay en la tabla |
| ¿Cuántas corresponden a cada tipo de presa? | `hunts['prey_type']` | `hunts['prey_type'].value_counts()`, porque cuenta cuántas veces aparece cada presa |
| ¿Qué porcentaje representa cada presa? | `hunts['prey_type']` | `hunts['prey_type'].value_counts(normalize=True) * 100`, porque calcula qué parte del total representa cada presa |
| ¿Cuántas cacerías se registraron en cada día observado? | `hunts['simulation_day']` | `hunts['simulation_day'].value_counts().sort_index()`, porque cuenta cacerías por día y ordena los días cronológicamente |
| ¿Cuánto aumentó, disminuyó y cambió en términos netos la comida? | `resources['resource_type']` y `resources['amount_delta']` | Filtrar `resource_type == 'food'`; sumar positivos para aumentos, usar `.abs()` en negativos para reducciones, y sumar todo para el balance neto |


## 2. Resume el parte de caza

Explica qué representa una fila de `hunts.csv` y cuál es el denominador de los porcentajes.

Cada fila representa un evento de caza completado. 
El porcentaje por tipo de presa se realiza sobre el total de cacerías, que es el denominador. 

## 5. Defiende tus conclusiones

Responde utilizando tus resultados reales:

1. ¿Qué presa o presas tienen el mayor recuento? Si hay empate, indícalo; si no hay datos, explica por qué no puedes responder.

deer     32 >> mayor recuento
sheep    10

2. ¿El porcentaje de una presa representa porcentaje de cacerías, de aldeanos o de tiempo? Justifica el denominador.

Representa porcentaje de cacerías respecto al número total de cacerías registradas. 

3. ¿El día con más cacerías fue necesariamente el día en que se dedicó más tiempo a cazar?

No, el tiempo no de caza no determina que se complete o no la misma. 

4. ¿El balance neto indica las existencias finales de comida? ¿Qué información faltaría?

Indica la diferencia entre las ganancias y las reducciones de comida. Para calcular las existencias finales tendríamos que conocer la cantidad inicial antes de los eventos de cambio de comida. 

5. ¿Puedes demostrar que todos los incrementos de comida se deben a la caza? ¿Qué vínculo entre eventos necesitarías para justificarlo?

Con los datos actuales no puedo relacionar los registros de hunts con los cambios en resources de tipo comida. Necesitaría que un índice relacionara ambos eventos, por ejemplo, con una columna en el registro de comida que apunte al event_index con el que se relaciona. 

## Ampliación para l@s más rápid@s: contrastar con las fotografías

Antes de usar `.iloc`, comprueba si hay filas. Con una sola fotografía, explica por qué la diferencia de cero no demuestra estabilidad durante toda la partida.

Que exista solo una fotografía no indica que no haya habido cambios antes o después del instante reflejado, sólo que no hay otros snapshots para comparar.

Compara esa diferencia con tu balance de comida. ¿Tienen necesariamente el mismo intervalo de observación? Explica por qué una discrepancia no prueba por sí sola un error. No fuerces la igualdad con un `assert`.

El balance de comida se reevalúa en cada evento de cambio, mientras que el stock de comida se calcula en cada intervalo entre snapshots. Una discrepancia entre ambos valores puede implicar que han ocurrido eventos de cambio de comida antes o después que aún no se han visto reflejados.