# Notas para el machete — PCP 2do parcial

★ = lo que costó o se preguntó. Se agrega al terminar/revisar cada ejercicio; el machete final se arma el domingo.

## Guía 5 — STM
- ★ **Buffer `TVar (Maybe t)`: `get` TOMA** (lee y deja `Nothing`), no solo lee. `put` solo escribe si está vacío. Patrón: `readTVar` → `case` → `writeTVar` según el caso, todo en la misma transacción.
- No bloqueante = avisar con el retorno (`Maybe`/`Bool`); bloqueante = `retry` en la rama que no puede seguir.
- ★ `modifyTVar v (+1)` ok, pero `(-1)` es el NÚMERO -1, no una función → usar `writeTVar v (x - 1)` (si ya leíste x) o `subtract 1`.
- ★ Bolitas (Ej 3): "cuántos están jugando" = contador que se toca en **su propio** `atomically` (entrar / salir). Si sumás y restás dentro de la misma transacción, nadie ve el cambio. Salir también puede tener que esperar (`check`) para no romper el invariante.
- Dos permisos atómicos (Ej 2): los dos `acquire` en el mismo `atomically`; si el segundo hace `retry`, se deshace el primero.
- ★ Preferencias (Ej 5): `opcionA \`orElse\` opcionB`; cada opción hace `check` (= retry si falla). Si las dos fallan, duerme hasta que cambie algo que leyó cualquiera.
- Fumadores (Ej 4): mesa = `TVar (Maybe Ingrediente)` con lo que FALTA; fumador `check (m == Just mio)`.
