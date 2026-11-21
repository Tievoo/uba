# Machete 2do parcial

Para copiar a mano: 4 columnas de 32 renglones (frente izq/der, dorso izq/der), una por ejercicio del parcial.
No repite nada de la hoja útil (API STM, helpers, reglas y sintaxis de canales, enunciado del teorema maestro).
Versión desarrollada (2026-11-16): menos ítems, más explicación; sin tabla de recurrencias (se saca con el maestro).

## Frente, columna izquierda — STM (ej 1)
```text
# CÓMO ARMARLO
Una TVar por cada cosa compartida; si son varias, un data con
   todas adentro (data Centro = ...), creadas con newTVarIO.
Cada operación es una función -> STM a: leer, chequear, escribir.
Si no puedo seguir: retry. Duerme hasta que cambie alguna TVar
   que LEÍ (no hay signal/notify, no hace falta avisar a nadie).
check c = "sigo solo si vale c". Lista vacía: case [] -> retry.
Preferencia: op1 `orElse` op2 (si op1 hace retry prueba op2; si
   las dos, retry de todo). El orden ES la prioridad. Sirve
   también para elegir entre dos lugares (dos centros, dos colas).
Esperar a que OTRO haga algo conmigo: TVar Bool propia que viaja
   en el pedido; el otro la pone True; yo hago check en OTRO
   atomically (en el mismo, el retry deshace también mi pedido).
Estado propio de un thread (racha, contador): TVar local creada
   en ese thread, no va en el data compartido.
IO (print, atender, threadDelay) SIEMPRE afuera: la transacción
   devuelve el valor y el IO va después del atomically.
# TRAMPAS
leer en un atomically y escribir en otro = race (alguien se mete
   en el medio). Lo que tiene que ser atómico va en UNO solo.
cola llena / vacía -> retry, nunca busy-wait con un loop.
main no espera a los threads: async + wait sobre cada uno.
# JUSTIFICAR (lo piden siempre)
race: cada operación es un atomically -> atómica y aislada; si
   dos chocan, una aborta y reintenta. Invariante: en UNA sola.
deadlock: no hay locks; solo puede trabarse alguien en retry.
   Mostrar que lo que espera (lugar en la cola, que lo atiendan)
   eventualmente pasa porque otro thread lo produce.
starvation: SÍ puede. Una transacción se aborta si al commitear
   otra cambió algo que leyó; si eso pasa siempre, no avanza
   nunca. Y retry no es FIFO: despiertan todos y gana cualquiera.
   Traza: A lee la cola, B commitea antes, A aborta, y así siempre
```

## Frente, columna derecha — Mensajes (ej 2)
```text
# CÓMO ARMARLO
1. Diagrama: cajitas = procesos, flechas = canales. Se usa en la
   justificación de deadlock: hacerlo SIEMPRE.
2. Estado compartido -> vive en UN proceso servidor; sus datos
   solo los toca él, así que no hay race.
3. Pedido = struct. Si espera respuesta, lleva su PROPIO canal de
   respuesta, creado por el cliente (uno compartido las mezcla).
4. Servidor: for { select { un case por tipo de pedido } }
# NO ATENDER UN TIPO DE PEDIDO POR AHORA: guarda con nil
antes del select: in = pedidos; if no puedo { in = nil }
   recibir de nil bloquea para siempre = ese case queda apagado.
   Se reabre cuando otro case cambia el estado (ej: liberar).
Si la condición depende del CONTENIDO del pedido: recibirlo igual,
   guardarlo en una cola de pendientes y contestar más tarde.
# RECURSO CONTADO (N lugares)
canal con buffer N precargado: tomar = receive (bloquea si no
   hay), liberar = send. O servidor con guarda nil.
# TIEMPO: timestamp y calcular al consultar, o Ticker como case
# TRAMPAS
dos procesos que se hacen send mutuo sin buffer = deadlock.
el servidor solo hace send a quien está esperando la respuesta;
   si no, se traba el servidor entero.
select elige al azar entre los listos: no es FIFO ni prioridad.
# JUSTIFICAR NO DEADLOCK: por cada operación bloqueante
a. ¿quién la destraba? (mi send lo completa el receive de otro)
b. los servidores entre dos receives solo responden a quien está
   esperando -> siempre vuelven al select.
c. el diagrama no tiene ciclos de sends: los pedidos van al
   servidor y las respuestas vuelven por el canal propio.
d. guardas nil: mostrar que se reabren (ej: los lugares vuelven
   porque todo hincha termina pagando y la barra libera).
```

## Dorso, columna izquierda — LTS / LTL (ej 3)
```text
# ARMAR EL LTS
estado = (pc de cada proceso, variables compartidas). Mismo pc
   con otra variable = OTRO estado.
1 transición por acción que toca algo compartido; lo local se
   pega al paso siguiente (aclararlo por escrito).
canal sin buffer: send y receive = UNA acción compartida, los
   dos avanzan juntos. Bloqueado en el send = sigue en pide.
await / lock: la transición existe solo si vale la condición.
Primero cada componente suelto, después la composición por BFS
   desde el inicial. Revisar estados sin salida (= deadlock).
Proposiciones: decir en qué estados vale cada una.
Item LTL: escribirla y decir si es safety o liveness.
# LTL
□◇p: p infinitas veces · ◇□p: desde algún momento, p siempre.
p U q: q llega y p vale hasta antes. p W q: igual pero q puede no
   llegar nunca (□p alcanza). "no ... antes de", safety -> W.
Chequear: el consecuente no puede ser falso en el mismo estado
   de la premisa. □(p → ¬p W q) es FALSA apenas vale p.
entre dos p hay q: □(p → p W (¬p W q))  (p dura varios estados)
no vuelve a pedir sin usar: □(espera → ¬pide W usa)
○ = próximo paso del SISTEMA (puede ser de otro proceso).
# VERIFICAR
safety rota: ESCRIBIR la traza finita inicial -> estado malo.
liveness rota: prefijo (lazo)^ω donde nunca vale lo pedido; la
   traza tiene que activar la premisa.
fair choice: un estado visitado ∞ veces toma TODAS sus salidas ∞
   veces. Lazo injusto: pasa ∞ por s y nunca toma una salida
   habilitada de s -> bajo fair la propiedad pasa a valer.
fair NO salva safety ni estados sin salida.
"vale sin fairness": mostrar que TODA traza infinita lo cumple
   (ej: servidor en ciclo fijo; entre sus pasos solo hay finitos
   pasos locales de los clientes).
```

## Dorso, columna derecha — Paralelismo (ej 4)
```text
# FORK-JOIN
class X extends RecursiveTask<T> (devuelve) o RecursiveAction
   (escribe en un arreglo de salida; ahí join = esperar).
compute(): caso base; mid; izq = new X(A, lo, mid); izq.fork();
   r = new X(A, mid, hi).compute(); l = izq.join(); combinar.
fork se le hace a una TAREA nueva, no al resultado de llamar.
join recién después del compute: max(l.join(), r.compute()) es
   secuencial (Java evalúa los argumentos en orden).
lo que no depende de las mitades (ej: cruza) va entre fork y join
pasar índices, no copiar subarreglos (copiar suma Θ(n) de work).
una sola llamada recursiva cuyo resultado necesito: nada que
   forkear, W = S y paralelismo Θ(1).
# WORK Y SPAN
W (= T1) suma todo. S (= T∞) = camino más largo.
W(n) = a·W(n/b) + WORK del combinar (se suman todas)
S(n) = S(n/b) + SPAN del combinar (paralelo: cuenta UNA copia)
Justificar: las mitades son independientes (leen rangos
   disjuntos, no escriben nada compartido) -> paralelas; el
   combinar usa las dos -> va después del join, entra al span.
combinar secuencial: span = work (cruza, merge: Θ(n) -> S Θ(n)).
   combinar en fork-join: span menor (suma de matrices Θ(log n)).
Maestro (hoja útil): escribir a, b, n^(log_b a), f, caso y ε;
   caso 3: chequear regularidad a·f(n/b) ≤ c·f(n) con c < 1.
paralelismo = W/S = speedup máximo con infinitos procesadores.
# COTAS
T_P ≥ T1/P (work law) · T_P ≥ T∞ (span law)
greedy: T_P ≤ T1/P + T∞ (≈ para estimar) · speedup = T1/T_P
si P > W/S, agregar procesadores ya no ayuda (manda el span).
concluir comparando W, S y W/S de cada variante, no solo T_P.
comparar programas: una desigualdad por dato, despejar T∞' − T∞.
de mediciones: T1 ≤ P·T_P, T∞ ≤ T_P (las menores) y enchufar en
   (T1 − T∞)/P + T∞, que crece en T1 y en T∞.
```
