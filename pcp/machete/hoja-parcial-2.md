# Machete 2do parcial — borrador

Para copiar a mano: 4 columnas de 32 renglones (frente izq/der, dorso izq/der), una por ejercicio del parcial.
No repite nada de la hoja útil (API STM, helpers, sintaxis de canales, enunciado del teorema maestro).
Borrador: se ajusta después del simulacro con los errores que aparezcan.

## Frente, columna izquierda — STM (ej 1)
```text
# RECETA
TVar por cosa compartida (data si son varias), newTVarIO en main
op :: ... -> STM a = leer · check cond · escribir
check = condición para SEGUIR · Maybe: case Nothing -> retry
retry duerme hasta que cambie una TVar LEÍDA (no hay signal)
orElse = preferencia / prioridad (encadenar de mayor a menor)
componer: ops devuelven STM, el que las usa pone atomically
# TRAMPAS
avisar + esperar en el MISMO atomically = deadlock
   (el retry deshace el aviso) -> dos atomically
leer y escribir en atomically distintos = race
nada de IO adentro: return valor, print afuera
(-1) es un número: modifyTVar v (subtract 1)
main no espera: async + mapM_ wait
# PATRONES
buffer 1: TVar (Maybe t), get TOMA (deja Nothing)
no bloqueante -> devuelve Bool/Maybe · bloqueante -> retry
semáforo: TVar Int · acq: check (n > 0); write (n-1)
k permisos juntos: check (n >= k) en UNA transacción
racha (3 urg -> 1 común): TVar Int por agente, if n<3 orElse
tomar varias cosas: todo en 1 atomically, si falta -> retry
esperar a que te atiendan: TVar Bool propia en la cola, el que
   atiende la pone True; llamar hace check en OTRO atomically
# ESQUELETO
main = do e <- newTVarIO x0
          hs <- mapM (\i -> async (th e i)) [1..n]
          mapM_ wait hs
th e i = do r <- atomically (op e); print r; th e i
# JUSTIFICAR
safety: transacción atómica y aislada (PL = commit)
no deadlock: sin locks; chequear que nadie quede en retry
NO garantiza ausencia de inanición (reintentos infinitos)
```

## Frente, columna derecha — Mensajes (ej 2)
```text
# PLANTILLA
cajitas = procesos, flechas = canales (quién crea / pasa)
estado compartido -> vive en UN servidor (= lock gratis)
struct por pedido · si espera algo: resp chan T adentro
canal de resp POR cliente/pedido (compartido = se mezcla)
orden entre tipos de pedido -> UN canal con campo tipo
# GUARDAS CON NIL (canal nil = case apagado)
(channel T) ent = nil; if puedo { ent = pedidos }
select { case p = receive(ent): ...  case ...: ... }
cola interna: out = nil; prim = nil
   if len(cola) > 0 { out = salida; prim = cola[0] }
   select { case x = receive(in): cola = append(cola, x)
            case send(out, prim): cola = cola[1:] }
valor del send calculado ANTES del select
condición depende del pedido -> recibir y encolar pendientes
# TIEMPO
Sleep si no atiende nada más · Ticker+select si atiende otros
After(t): timeout de una sola vez
# PREFETCH: resp con buffer 1, pido el próximo al usar este
# RECURSO CONTADO: chan buffer N precargado (tomar = receive,
   liberar = send; un thread lo recarga con lo liberado)
# N EN VUELO / ORDEN
contador + nil en la entrada cuando llego a N
cola FIFO de canales de resp privados, entrego la cabeza
# PRIORIDAD: select{urg; default: select{urg; normal}}
# TRAMPAS
sends cruzados sincrónicos = deadlock -> buffer / process / select
servidor nunca espera a un cliente (resp con buffer 1)
select elige al azar: ni FIFO ni prioridad
# NO DEADLOCK (justificar)
servidor siempre vuelve a recibir · todo pedido aceptado
se contesta · sin ciclos de espera · las guardas nil se reabren
```

## Dorso, columna izquierda — LTS / LTL (ej 3)
```text
# LTS: estado = (pcs, locales, compartidas)
1 paso por acción que lee/escribe algo compartido
lo local se junta con el paso siguiente (aclararlo)
asignación múltiple = 1 paso · await = paso si cond vale
lock: var libre/tomado, lock() solo si libre
sin buffer: send+recv = UN paso; bloqueado en send = sigue antes
canal con buffer = LTS extra (vacío/lleno), in / out
deadlock = estado NO final sin salidas · tryLock en loop: livelock
mismos pcs con otra variable = OTRO estado
# LTL: trazas infinitas (σ^ω)
□◇p: p en el período · ◇□p: p en TODO el período
p U q: q llega, p hasta antes · si q ahora -> true
p W q = p U q ∨ □p (no obliga a que llegue q)
X U ◇ψ ≡ ◇ψ · premisa falsa -> implicación true
¬□¬a ≡ ◇a · ○ se rompe con pasos ajenos -> usar ◇
precedencia: unarios > U, W > ∧, ∨ > →
# PROPIEDADES
mutex:      □¬(cs_0 ∧ cs_1)                safety
inanición:  □(wait_i → ◇cs_i)  (wait_i: pc_i = w)  liveness
q no antes que p: ¬q W p · alternar: W anidados
entre dos p hay q: □(p → p W (¬p W q))  (p dura varios estados)
   □(p → ¬p W q) MAL: falsa apenas vale p
safety: se rompe en prefijo finito · liveness: lazo ω
# VERIFICAR SOBRE EL LTS
safety: ESCRIBIR la traza inicial -> malo (no basta 'alcanzable')
liveness: prefijo (lazo)^ω donde nunca se cumple
ojo: la traza tiene que activar la premisa (wait_i)
# FAIR CHOICE
estado visitado ∞ veces -> toma TODAS sus salidas ∞ veces
lazo injusto: pasa por s, nunca toma salida habilitada de s
terminal = SCC sin flechas afuera; justa -> la recorre entera
fair NO salva safety ni estados sin salidas
```

## Dorso, columna derecha — Paralelismo (ej 4)
```text
# FORK-JOIN
RecursiveTask<T> devuelve · RecursiveAction escribe salida
low = new X(.., lo, mid); low.fork();
r = new X(.., mid+1, hi).compute(); l = low.join(); combinar
fork todas menos 1, compute 1, join al final (no antes)
   max(l.join(), r.compute()) MAL: args en orden = secuencial
join sin resultado = esperar (si no, el padre termina antes)
paralelas: escriben regiones disjuntas, leen lo que nadie toca
pasar índices, no copiar (copiar = Θ(n) de work)
# WORK / SPAN
W = nodos totales (T1) · S = camino más largo (T∞)
secuencial: W+W, S+S · paralelo: W+W, máx(S)
W(n) = a·W(n/b) + f(n) · S(n) = S(n/b) + g(n) (1 copia)
combinar entra al span con SU span (paralelo o no)
work = span -> paralelismo Θ(1) (power: cadena)
paralelismo = W / S · escribir recurrencia + caso base + Θ
# MAESTRO: f vs n^(log_b a) (hojas) · caso 3: regularidad
# SPAN: log n niveles × g(n) · g = n -> Θ(n) (geométrica)
# TABLA
2T(n/2)+1 = n          2T(n/2)+n = n log n
2T(n/2)+log n = n      4T(n/2)+1 = n²      8T(n/2)+n² = n³
T(n/2)+1 = log n       T(n/2)+log n = log² n
T(n/2)+n = n           T(n−1)+1 = n
2T(n/2)+n log n = n log² n (NO entra en el maestro de la hoja)
mergesort: W n log n · S n (merge de la raíz) · par log n
# COTAS
T_P ≥ T1/P · T_P ≥ T∞ (cualquier scheduler)
greedy: T_P ≤ T1/P + T∞ · ajustada: (T1 − T∞)/P + T∞
comparar programas: T_P de cada uno, T∞ incógnitas,
   una desigualdad por frase, despejar T∞' − T∞
medido -> T1 ≤ P·T_P (la menor), T∞ ≤ T_P (la menor)
   enchufar en la ajustada (creciente en T1 y T∞)
```
