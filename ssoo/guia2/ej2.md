## Ejercicio 2

### a) Para planificar estos procesos, ¿convendría usar un algoritmo de Round Robin? ¿convendría usar uno de prioridades? Justifique su respuesta.

Diría que usar una sola cola con Round Robin podría funcionar, pero los procesos entre sí son distintos y tienen requerimientos distintos, P0 y P1 se bloquean pseudo-frecuentemente entonces necesitan quantums más cortos, pero P2 es cpu instensive una gran parte del tiempo. Es decir, el RR funciona masomenos hasta que P2 tenga escritura al disco. No sufriría Starvation y estaría _bien_.

Usar una cola de prioridades me parece más optimo. P1 se bloquea frecuentemente, entonces lo pondría en prioridad 0 con un quantum $q$, y después a P0 y P2 con $2 \cdot q$ o un poco más, se iría ajustando en base a lo que vea. Diría que el riesgo de starvation es bajo, dado q P1 es siempre el mismo proceos y se bloquea frecuentemente, pero si noto mucho starvation, implementaría un pequeño aging en caso de emergencia
