# El parte de caza también habla SQL

1. ¿Qué representa una fila del resultado? ¿Cuenta cacerías o unidades de comida?
Cada fila representa una cacería completada, no las unidades de comida generadas ni el tiempo dedicado a la caza. 

2. ¿Qué hace `AS hunt_count`? Si lo cambias por `AS total_cacerias`, ¿qué referencias posteriores debes actualizar?
Crea una columna con el conteo de cacerías por cada tipo de presa. Habría que modificar el 'order by' final de la query, y las cabeceras para el csv si hunts.csv está vacío. 

3. ¿Qué archivo ocupa menos en tu partida? ¿Demuestra eso que ese formato será siempre mejor?
El formato parquet ocupa más, pero un formato u otro será mejor en función de la situación y necesidades de consulta. 

