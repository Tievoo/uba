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

## Mensajes (guía 6)
- ★ Pedido + respuesta: el mensaje lleva adjunto el canal de respuesta del cliente (ej 2, 4c).
- ★ Canal nil en select = case deshabilitado. Cola vacía → `out = nil`, así no se elige el send (ej 5).
- ★ Valor del send calculado antes del select (con cola vacía, `cola[0]` explota aunque el canal sea nil).
- Varios clientes en un mismo canal se mezclan: si cada uno necesita su respuesta, canal propio.

## LTS / LTL (guía 7)
- ★ `□◇φ` y `◇□φ` se deciden SOLO en la parte periódica: □◇ = aparece en el período, ◇□ = vale en todo el período.
- ★ `□(p U q)` falla si hay UNA posición sin p ni q (∅) antes de la próxima q. Revisar posición por posición.
- `○○q` = mirar la posición 3 (la traza arranca en 1).
- `p U q`: si q vale en la posición actual, es true sin mirar p.
- ★ `X U ◇ψ ≡ ◇ψ` (◇ a la DERECHA del U): si ◇ψ vale después, vale desde ahora → X no se mira. `X U ψ` en general NO se simplifica.
- ★ Implicación con premisa falsa = verdadera. "El antecedente nunca vale" ⇒ válida, no contradictoria.
- `¬□¬a ≡ ◇a` (no "siempre a"). `¬a ∧ □¬a ≡ □¬a`, `a ∨ ◇a ≡ ◇a`.
