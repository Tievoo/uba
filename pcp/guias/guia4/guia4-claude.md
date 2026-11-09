# Práctica 4: Estructuras de datos y sincronización Lock-Free — Resolución

**Programación Concurrente y Paralela — 2do Cuatrimestre 2026**

---

> ### ⚠️ Aviso de autoría
>
> **Esta resolución fue generada por Claude (modelo de lenguaje de Anthropic), no por mí.**
>
> No está corregida por un docente ni verificada contra una solución oficial. Puede
> contener errores, y varios ejercicios admiten más de una interpretación; cuando pasa,
> la interpretación elegida está escrita. No debería tomarse como respuesta autorizada
> de la cátedra.

---

## Convenciones

- Todo el código es **pseudocódigo**, con la sintaxis de las teóricas.
- `lock` / `unlock` son locks mutuamente excluyentes. Salvo que se diga otra cosa,
  **no** se asume que son fair.
- `CAS(x, esperado, nuevo)` es atómico y devuelve si lo logró.
- Para linealizabilidad se usa la receta del resumen 04: la función de abstracción, el
  PL de cada operación (éxito y falla por separado) y el chequeo de que el PL es atómico
  y está dentro del intervalo.

---

# Ejercicio 1 — Listas con claves hash no únicas

**Interpretación:** dos items **distintos** pueden tener el mismo `hashCode` (colisión).
El conjunto sigue siendo un conjunto de items: `add(x)` falla solo si ya está **ese**
item, no otro con la misma clave.

Lo que se rompe en todas las versiones es lo mismo: hoy, "encontré un nodo con
`curr.key == key`" se usa como "el item está". Con colisiones eso ya no vale. Puede
haber un **bloque** de nodos con la misma clave, y hay que comparar los items.

### La solución más simple: un orden total sin empates

Si los items se pueden comparar (o se agrega un desempate cualquiera que sea un orden
total y consistente con la igualdad), se ordena la lista por el par
**`(key, item)`** en vez de solo por `key`. El par vuelve a ser único, y **todas** las
implementaciones quedan iguales, cambiando la comparación `curr.key < key` por
`(curr.key, curr.item) < (key, item)` y la igualdad por la igualdad de pares. Los PL no
cambian.

### Sin desempate: qué cambia en cada versión

Los nodos con la misma clave quedan contiguos (el orden por clave se mantiene), en un
orden cualquiera dentro del bloque. Se fija una **posición canónica de inserción: al
final del bloque** (entre el último nodo con `key == k` y el primero con `key > k`).

- **Gruesa:** `add`, `remove` y `contains` recorren hasta el bloque y lo recorren
  entero comparando `curr.item == item`. `add`, si no lo encontró, inserta al final del
  bloque. (El `remove` de la teórica ya hace esto: recorre con `curr.key <= key` y
  compara items.) PL: sin cambios.
- **Fina (hand-over-hand):** igual que la gruesa, pero el recorrido del bloque sigue
  tomando los locks de a pares. Como se sigue tomando en orden de lista, no aparece
  deadlock. PL: `add` y `remove` exitosos en la escritura de `pred.next`; los que fallan
  y `contains`, cuando tienen tomado el lock del nodo que decide (el que tiene el item,
  o el primero con clave mayor).
- **Optimista:** el problema nuevo es que `add` tiene que asegurarse de que el item no
  está en **ningún** nodo del bloque, pero solo bloquea dos nodos. Con la posición
  canónica alcanza:
  1. recorre sin locks todo el bloque buscando el item; si lo encuentra, bloquea ese
     nodo y su `pred`, valida, y responde;
  2. si no lo encuentra, bloquea `(pred, curr)` = (último del bloque, primero con clave
     mayor) y valida.
  Otro `add` con la misma clave tendría que insertar exactamente en esa ventana, así que
  si alguien insertó el mismo item entre el recorrido y el lock, `pred.next != curr` y la
  validación falla (se reintenta). `remove` y `contains` buscan el nodo con el item y
  validan `(pred, ese nodo)`.
- **Lazy:** igual que la optimista para `add` y `remove`. `contains` recorre el bloque y
  devuelve `true` si encuentra un nodo **con ese item y sin marcar**. Sigue siendo
  wait-free. PL de `remove` exitoso: marcar.
- **Lock-free:** `find` tiene que devolver, además de la ventana canónica, si el item
  está en el bloque. `add` hace CAS sobre `pred.next` de la ventana canónica. Si otro
  `add` insertó en esa ventana, el CAS falla y reintenta, y en el reintento lo ve.
  `remove` marca el nodo que tiene el item. PL: iguales a los de la teórica.

En todas, `contains` y las operaciones que fallan se linealizan cuando se lee el nodo que
decide el resultado. En el caso "no está", eso incluye haber recorrido el bloque entero.

---

# Ejercicio 2 — Figura con dos grupos de campos

Como `ajustarPosicion` solo toca `x, y` y `ajustarTamano` solo toca `alto, ancho`, y
ninguna lee los campos de la otra, se usa **un lock por grupo**:

```text
class Figura {
    int x = 0, y = 0, alto = 0, ancho = 0
    Lock lockPos, lockTam

    ajustarPosicion() {
        lockPos.lock()
        x = algunX(); y = algunY()
        lockPos.unlock()
    }

    ajustarTamano() {
        lockTam.lock()
        alto = algunAlto(); ancho = algunAncho()
        lockTam.unlock()
    }
}
```

- **Exclusión:** cada grupo de campos se toca solo con su lock, así que no hay races y
  cada método sigue siendo atómico respecto de su grupo.
- **Concurrencia:** un `ajustarPosicion` y un `ajustarTamano` toman locks distintos, así
  que corren a la vez.
- **Linealizable:** cada método se linealiza en cualquier momento con su lock tomado.

**Funciones nuevas que tocan los dos grupos:** tienen que tomar los **dos** locks, y
**siempre en el mismo orden global** (por ejemplo, primero `lockPos` y después
`lockTam`), en todas las funciones. Si una los tomara al revés, dos funciones de ese tipo
podrían tener cada una un lock y esperar el otro: espera circular, deadlock.

```text
moverYEscalar() {
    lockPos.lock(); lockTam.lock()     // siempre Pos antes que Tam
    ...
    lockTam.unlock(); lockPos.unlock()
}
```

---

# Ejercicio 3 — Recursos con `assign` y `swap`

## 3.a — Un lock por posición

```text
class Recursos {
    Object[] recursos
    Lock[] locks          // uno por posición
    int capacidad

    assign(pos, o) {
        if (pos < capacidad) {
            locks[pos].lock()
            recursos[pos] = o
            locks[pos].unlock()
        }
    }

    swap(i, j) {
        if (i < capacidad && j < capacidad) {
            if (i == j) return                 // no hay nada que hacer (y evita tomar dos veces el mismo lock)
            a = min(i, j); b = max(i, j)
            locks[a].lock(); locks[b].lock()   // orden global: menor índice primero
            aux = recursos[i]; recursos[i] = recursos[j]; recursos[j] = aux
            locks[b].unlock(); locks[a].unlock()
        }
    }
}
```

- `capacidad` no cambia, así que se puede leer sin lock.
- Operaciones sobre posiciones distintas toman locks distintos y corren a la vez.
- **Sin deadlock:** todos toman los locks en orden creciente de índice. Si hubiera un
  ciclo de threads, cada uno esperando un lock que tiene el siguiente, los índices
  esperados serían estrictamente crecientes a lo largo del ciclo, lo cual es absurdo.
- **Linealizable:** `assign` en la escritura, `swap` en cualquier momento con los dos
  locks tomados.

## 3.b — ¿Es libre de inanición?

**Depende de los locks.**

- **Con locks fair (FIFO): sí.** No hay deadlock, y cada lock que alguien espera lo tiene
  un thread que, o no espera nada, o espera un lock de índice mayor. Siguiendo esa
  cadena (siempre creciente, así que finita) se llega a alguien que no espera y termina,
  y libera. Entonces todo lock tomado se libera en tiempo finito, y con locks fair el que
  espera tiene una cantidad acotada de threads adelante.
- **Con locks no fair: no.** Un `swap(0, 5)` puede esperar `locks[0]` para siempre si otros
  threads lo toman y lo sueltan una y otra vez (`assign(0, ...)` repetidos) y el lock
  siempre se lo da a otro.

---

# Ejercicio 4 — Lista optimista

## 4.a — Un thread que nunca logra eliminar

Lista: `head → a → c → tail`. A quiere `remove(c)`.

| Paso | A (`remove(c)`) | B |
|---|---|---|
| 1 | recorre sin locks: `pred = a`, `curr = c` | |
| 2 | | `add(b)`: inserta `b` entre `a` y `c` |
| 3 | toma los locks de `a` y `c`; `validate`: `a.next == b ≠ c`, **falla**; suelta y reintenta | |
| 4 | | `remove(b)`: la lista vuelve a `a → c` |
| 5 | recorre: `pred = a`, `curr = c` | |
| 6 | | `add(b)` |
| 7 | valida y falla | |
| … | se repite para siempre | |

La traza es fair (todos ejecutan) y los locks pueden ser fair: A siempre consigue los
locks, pero la **validación** falla siempre. Por eso la optimista no es libre de
inanición aunque los locks lo sean.

## 4.b — `add` toma los locks al revés (`curr` antes que `pred`)

`remove` sigue tomando `pred` y después `curr`. Lista: `head → a → c → tail`.

| Paso | T1: `add(b)` (ventana `a`, `c`) | T2: `remove(c)` (ventana `a`, `c`) |
|---|---|---|
| 1 | recorre: `pred = a`, `curr = c` | recorre: `pred = a`, `curr = c` |
| 2 | `c.lock()` (primero `curr`) | |
| 3 | | `a.lock()` (primero `pred`) |
| 4 | `a.lock()`: lo tiene T2, espera | |
| 5 | | `c.lock()`: lo tiene T1, espera |

Los dos esperan un lock que tiene el otro: **deadlock**. El argumento de ausencia de
deadlock de la optimista es que todos toman los locks en orden de lista (de `head` hacia
`tail`). Con `add` al revés ese orden global se pierde, y aparece la espera circular.

---

# Ejercicio 5 — `actualizarEntrada` optimista

## 5.a

Idea: leer con el lock, **computar sin el lock**, y al volver a tomar el lock **validar**
que la entrada no cambió. Para validar se usa un **número de versión por entrada**
(comparar solo el valor puede fallar por ABA: otro thread podría cambiarla y volver a
dejar el mismo objeto).

```text
HashMap<Integer, Object> tabla
HashMap<Integer, int> version     // toda operación que modifique la entrada i hace version[i]++
Lock lock

actualizarEntrada(i) {
    while (true) {
        lock.lock()
        v1 = tabla.get(i)
        ver = version.get(i)
        lock.unlock()

        v2 = ComputacionalmenteCostoso(v1)     // sin lock: la tabla queda libre

        lock.lock()
        if (version.get(i) == ver) {           // nadie tocó la entrada i mientras computaba
            tabla.put(i, v2)
            version.put(i, ver + 1)
            lock.unlock()
            return
        }
        lock.unlock()                          // cambió: se reintenta con el valor nuevo
    }
}
```

- El resto de las operaciones de `Tabla` que modifiquen una entrada tienen que tomar el
  lock e incrementar su versión.
- **Linealizable:** en el intento exitoso, la operación se linealiza en el `put` (con el
  lock tomado). Como la versión no cambió entre la lectura y el `put`, el valor sobre el
  que se computó `v2` es el que tenía la entrada justo antes del `put`, así que el efecto
  es el mismo que si todo se hubiera hecho de golpe.
- `tabla.remove(i); tabla.put(i, v2)` del original se reemplaza por un solo `put`, que
  tiene el mismo efecto.

## 5.b — ¿Es libre de inanición?

**No.** Es libre de deadlock (se toma un solo lock por vez), pero un `actualizarEntrada(i)`
puede reintentar para siempre: si otros threads actualizan la entrada `i` siempre entre
su lectura y su validación, la versión cambió cada vez y la validación falla. Eso pasa
aunque el lock sea fair, porque el problema no es conseguir el lock, sino que la
validación falla.

---

# Ejercicio 6 — Cola con dos pilas

## 6.a — No es correcta si `enq` y `deq` corren a la vez

Cada operación de las pilas es atómica (`synchronized`), pero `deq` hace **varias**
operaciones seguidas sin nada que las agrupe.

**Traza** (pilas escritas de abajo hacia arriba):

| Paso | E (`enq`) | D (`deq`) | `in` | `out` |
|---|---|---|---|---|
| 0 | `enq(x)` termina | | [x] | [] |
| 1 | | `out.isEmpty()` → true | [x] | [] |
| 2 | | `in.pop()` → x | [] | [] |
| 3 | `enq(y)` empieza y termina | | [y] | [] |
| 4 | | `out.push(x)` | [y] | [x] |
| 5 | | `in.isEmpty()` → false; `in.pop()` → y; `out.push(y)` | [] | [x, y] |
| 6 | | `out.pop()` → **y** | [] | [x] |

`enq(x)` termina antes de que empiece `enq(y)`, y el único `deq` devuelve `y` mientras `x`
sigue en la cola. En cualquier linealización `enq(x)` va antes que `enq(y)`, así que el
primer `deq` tendría que devolver `x`. **No es linealizable.**

Otro problema, con dos `deq`: `out = [z]`, `in = [w]`. D1 ve `out` no vacía y no
transfiere; D2 saca `z`; D1 hace `out.pop()` sobre la pila vacía y falla, aunque la cola
tiene `w`.

## 6.b — Solución correcta con concurrencia entre `enq` y `deq`

Un lock para cada pila: `lockIn` para `in` (lo usan `enq` y la transferencia) y `lockOut`
para `out` (lo usa `deq`).

```text
Stack in, out
Lock lockIn, lockOut

enq(o) {
    lockIn.lock()
    in.push(o)                            // PL
    lockIn.unlock()
}

deq() {
    lockOut.lock()
    if (out.isEmpty()) {
        lockIn.lock()                     // la transferencia se hace sin enq en el medio
        while (!in.isEmpty()) out.push(in.pop())
        lockIn.unlock()
    }
    if (out.isEmpty()) { lockOut.unlock(); throw EmptyException }   // PL (vacía): ambas vacías
    r = out.pop()                         // PL (exitoso)
    lockOut.unlock()
    return r
}
```

- **Invariante:** todo elemento de `out` se encoló antes que todo elemento de `in`, y el
  tope de `out` es el más viejo de la cola. La transferencia se hace con **los dos**
  locks tomados, así que ningún `enq` se mete en el medio y el orden queda invertido
  correctamente.
- **Concurrencia:** si `out` no está vacía, `deq` toma solo `lockOut` y corre a la vez que
  cualquier `enq`, que toma solo `lockIn`.
- **Sin deadlock:** el único que toma dos locks es `deq`, y siempre en el orden
  `lockOut` → `lockIn`. `enq` toma uno solo. No hay ciclo posible.
- **Linealizable:** `enq` en el `push`; `deq` exitoso en el `pop` de `out`; `deq` vacío
  cuando, con los dos locks tomados, ve las dos pilas vacías.

---

# Ejercicio 7 — Cola acotada con dos contadores

En la cola de la teórica, `enq` hace `size.getAndIncrement()` y `deq` hace
`size.getAndDecrement()` **siempre**, así que las dos puntas compiten por la misma
variable. La idea es que cada punta lleve su propio contador y solo se sincronicen cuando
de verdad hace falta saber el tamaño.

```text
int enqSize = 0        // lo modifica solo enq, con enqLock: cuántos encoló (menos los ya descontados)
int deqSize = 0        // lo modifica solo deq, con deqLock: cuántos desencoló desde la última sincronización
volatile int deqEsperando = 0, enqEsperando = 0
```

- **Tamaño real:** `enqSize − deqSize`. Como `enq` solo mira `enqSize`, ve un tamaño **igual
  o mayor** al real, o sea, puede creer que está llena cuando no lo está, pero nunca
  al revés. Es seguro.
- **`enq`:** si `enqSize < capacidad`, encola sin tocar nada de `deq`. Solo si
  `enqSize == capacidad` se sincroniza: toma `deqLock`, hace `enqSize -= deqSize;
  deqSize = 0` y lo suelta. Si después de eso sigue llena, espera en `notFull`.
- **`deq`:** decide si hay elementos mirando `head.next` (como en la teórica, sin
  contador) y hace `deqSize++` con `deqLock` tomado.

```text
enq(x) {
    e = new Node(x)
    enqLock.lock()
    while (enqSize == capacidad) {
        deqLock.lock(); enqSize -= deqSize; deqSize = 0; deqLock.unlock()   // único punto de sincronización
        if (enqSize == capacidad) { enqEsperando++; notFull.await(); enqEsperando-- }
    }
    tail.next = e; tail = e                 // PL: tail.next = e
    enqSize++
    enqLock.unlock()
    if (deqEsperando > 0) { deqLock.lock(); notEmpty.signalAll(); deqLock.unlock() }
}

deq() {
    deqLock.lock()
    while (head.next == null) { deqEsperando++; notEmpty.await(); deqEsperando-- }
    r = head.next.value
    head = head.next                        // PL
    deqSize++
    deqLock.unlock()
    if (enqEsperando > 0) { enqLock.lock(); notFull.signalAll(); enqLock.unlock() }
    return r
}
```

**Por qué no se pierde ningún aviso:**
- **Consumidor dormido:** el consumidor hace `deqEsperando++` y chequea `head.next` con
  `deqLock` tomado. El productor engancha `e` y **después** lee `deqEsperando`. Si el
  productor leyó 0, el `++` del consumidor fue posterior a esa lectura, y por lo tanto
  posterior al enganche, así que el consumidor ve `head.next != null` y no se duerme.
  (Hace falta que `deqEsperando` sea `volatile` para que valga este razonamiento de orden.)
- **Productor dormido:** simétrico. El productor incrementa `enqEsperando` antes de la
  sincronización con `deqLock`, y el consumidor incrementa `deqSize` con `deqLock` tomado
  y después lee `enqEsperando`. Si el consumidor desencoló antes de la sincronización, el
  productor lo ve en `deqSize`. Si desencoló después, lee `enqEsperando > 0` y va a
  despertarlo. Para eso toma `enqLock`, que el productor suelta al hacer `await`, así que
  el `signal` no puede caer antes del `await`.

**Resultado:** en el caso común (ni llena ni vacía), `enq` y `deq` no comparten ninguna
variable que escriban los dos. Solo se sincronizan cuando `enq` cree que está llena, o
cuando hay alguien dormido del otro lado.

---

# Ejercicio 8 — Pila acotada

## Versión con monitor (parcial: espera si está llena o vacía)

Como las dos operaciones trabajan sobre el mismo punto (el tope), no se gana nada
separando locks. Un monitor alcanza.

```text
monitor PilaAcotada {
    Object[] datos = new Object[capacidad]
    int tope = 0                 // cantidad de elementos
    Condition noLlena, noVacia

    push(o) {
        while (tope == capacidad) wait(noLlena)
        datos[tope] = o; tope++
        signal(noVacia)          // espera un solo tipo de thread, intercambiables
    }

    pop() {
        while (tope == 0) wait(noVacia)
        tope--; o = datos[tope]; datos[tope] = null
        signal(noLlena)
        return o
    }
}
```

- `while` por Mesa. `signal` alcanza porque en cada condición esperan threads que quieren
  lo mismo.
- Linealizable: cada operación en cualquier momento dentro del monitor.

## Versión lock-free (total: si está llena o vacía, falla)

El tamaño se guarda **en cada nodo**, así que "tope + tamaño" se cambia con un solo CAS:

```text
class Node { Object valor; Node next; int tam }     // inmutable
AtomicReference<Node> top = null

push(o) {                        // devuelve false si está llena
    while (true) {
        old = top.get()
        t = (old == null) ? 0 : old.tam
        if (t == capacidad) return false            // PL (llena): la lectura de top
        n = new Node(o, old, t + 1)
        if (CAS(top, old, n)) return true           // PL (exitoso)
    }
}

pop() {
    while (true) {
        old = top.get()
        if (old == null) throw EmptyException      // PL (vacía): la lectura de top
        if (CAS(top, old, old.next)) return old.valor   // PL (exitoso)
    }
}
```

Es lock-free: un CAS falla solo si otro cambió `top` con éxito.

---

# Ejercicio 9 — ABA en la pila lock-free

## 9.a — Sin garbage collector

Sin GC, los nodos se reciclan a mano (una `freeList`), así que una dirección de memoria
puede volver a aparecer en la pila. Pila: `top → A → B → C`.

| Paso | T1 (`pop`) | T2 | Pila |
|---|---|---|---|
| 1 | lee `oldTop = A`, `newTop = A.next = B`; se duerme antes del CAS | | A → B → C |
| 2 | | `pop()`: saca A y lo devuelve a la `freeList` | B → C |
| 3 | | `pop()`: saca B y lo devuelve a la `freeList` | C |
| 4 | | `push(D)`: reutiliza el nodo **A** para guardar D | A(=D) → C |
| 5 | `CAS(top, A, B)`: `top` vale A, **da true**; `top = B` | | B → ? |

`top` quedó apuntando a B, un nodo que ya no está en la pila (está en la `freeList`), y
D y C se perdieron. El CAS solo comparó direcciones: A "volvió", y el CAS no puede
distinguir que en el medio pasaron cosas.

## 9.b — Solución: sello de versión

Se cambia `top` por una referencia con **sello** (`AtomicStampedReference`): cada
modificación exitosa incrementa el sello. Aunque la dirección vuelva a ser A, el sello ya
no es el mismo y el CAS falla.

```text
AtomicStampedReference<Node> top = (null, 0)

push(v) {
    n = reciclarONuevo(v)
    while (true) {
        (old, s) = top.get()
        n.next = old
        if (top.CAS(old, n, s, s + 1)) return
    }
}

pop() {
    while (true) {
        (old, s) = top.get()
        if (old == null) throw EmptyException
        next = old.next
        if (top.CAS(old, next, s, s + 1)) { liberar(old); return old.valor }
    }
}
```

En la traza, T1 leyó el sello `s` en el paso 1. Los pasos 2, 3 y 4 lo llevan a `s + 3`, así
que el CAS del paso 5 falla y T1 reintenta con la pila real.

---

# Ejercicio 10 — Contador lock-free con `inc`, `get` y `reset`

```text
AtomicInteger c = 0

inc() {
    while (true) {
        v = c.get()
        if (CAS(c, v, v + 1)) return        // PL
    }
}

get()   { return c.get() }                  // PL: la lectura
reset() { c.set(0) }                        // PL: la escritura
```

- **Linealizable:** cada operación tiene un PL que es un solo paso atómico sobre `c`, y en
  ese paso el valor cambia (o se lee) exactamente como dice la especificación secuencial.
- **`inc`: lock-free, no wait-free.** Si su CAS falla es porque otro cambió `c` con éxito
  (un `inc` o un `reset`), así que alguien progresó. Pero un mismo `inc` puede perder la
  carrera infinitas veces.
- **`get`: wait-free.** Es una sola lectura.
- **`reset`: wait-free.** Es una sola escritura atómica. No necesita CAS, porque el valor
  nuevo (0) no depende del viejo.

---

# Ejercicio 11 — Figura lock-free

Cada grupo de campos pasa a ser un **objeto inmutable**, apuntado por una referencia
atómica. Cambiar el grupo es armar un objeto nuevo y hacer CAS de la referencia, así que
los dos campos cambian juntos, de golpe.

```text
class Pos { final int x, y }          // inmutables
class Tam { final int alto, ancho }

AtomicReference<Pos> pos = new Pos(0, 0)
AtomicReference<Tam> tam = new Tam(0, 0)

ajustarPosicion() {
    while (true) {
        old = pos.get()
        nuevo = new Pos(algunX(), algunY())     // si dependen del valor viejo, se calculan a partir de old
        if (CAS(pos, old, nuevo)) return        // PL
    }
}

ajustarTamano() {
    while (true) {
        old = tam.get()
        nuevo = new Tam(algunAlto(), algunAncho())
        if (CAS(tam, old, nuevo)) return        // PL
    }
}

leerPosicion() { return pos.get() }             // wait-free; nunca ve un (x, y) mezclado
```

- **Posición y tamaño siguen siendo independientes:** son dos referencias distintas, así
  que un ajuste de cada una no compite con el otro, igual que con los dos locks del
  ejercicio 2.
- **Progreso:** los ajustes son lock-free (un CAS falla solo si otro ajuste del mismo grupo
  tuvo éxito). Si el valor nuevo no depende del viejo, alcanza con `pos.set(nuevo)`, que es
  wait-free.
- **Funciones que tocan los dos grupos a la vez:** dos CAS separados no son atómicos entre
  sí (alguien podría ver la posición nueva con el tamaño viejo). Para eso hay que juntar
  todo en **un solo** objeto inmutable `Estado(x, y, alto, ancho)` con una sola referencia
  atómica. El costo es que ahí los ajustes de posición y de tamaño vuelven a competir por
  la misma referencia.
