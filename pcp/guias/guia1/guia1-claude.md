# Práctica 1: Modelo de cómputo y Exclusión Mutua — Resolución

**Programación Concurrente y Paralela — 1er Cuatrimestre 2026**

---

> ### ⚠️ Aviso de autoría
>
> **Esta resolución fue generada por Claude (modelo de lenguaje de Anthropic), no por mí.**
>
> La usé para ponerme al día con la materia porque no llegué a resolver la guía por mi
> cuenta a tiempo. No está corregida por un docente ni verificada contra una solución
> oficial. Puede contener errores, y en varios ejercicios el enunciado admite más de una
> interpretación (sobre todo respecto de qué operaciones se asumen atómicas), así que las
> conclusiones dependen de la convención adoptada — que está explicitada más abajo.
>
> La estoy leyendo críticamente y consultando los puntos que no me cierran. No debería
> tomarse como respuesta autorizada de la cátedra.

---

## Convención sobre atomicidad

Casi todos los ejercicios de esta guía dependen de **qué se considera atómico**, así que
conviene fijarlo antes de arrancar (es el punto de la slide 17 de la clase: si elegís un
grano demasiado grueso, se te escapan trazas y concluís que un programa es correcto cuando
no lo es).

- **Ejercicios 1 y 3:** el enunciado del Ej. 1 aclara que son atómicas "la lectura y
  asignación de variables, operaciones aritméticas y evaluación de expresiones booleanas".
  Lo interpreto como: **cada instrucción completa es atómica** — no hay que desagregar
  `y = x + 1` en load/add/store. La enumeración está para decir que no hace falta partir
  nada.
- **Ejercicios 2, 9, 10, 12, 13, 15:** acá la gracia del ejercicio es justamente que las
  operaciones compuestas **no** son atómicas. Se desagregan explícitamente en lectura de la
  variable compartida hacia una local, y escritura posterior.
- **Variables locales:** siempre atómicas (slide 28). `p.tmp` y `q.tmp` son variables
  independientes.
- **Weak fairness:** se asume siempre (slide 31). El scheduler no ignora a un thread para
  siempre. Cuando algo depende de esta hipótesis, lo aclaro.

**Notación de trazas.** Uso el formato de la clase: una columna por thread, una columna de
estado. La celda de estado indica los cambios producidos y la próxima instrucción (IP).

**Notación de estados en diagramas.** `⟨x=1, y=2 | T1:a1, T2:b1⟩` = valores de las globales,
y etiqueta de la próxima instrucción de cada thread. `—` marca thread terminado.

---

# Ejercicio 1

Para cada programa: semántica de cada hilo, semántica de la ejecución concurrente, y
diagrama de transición completo.

## 1.a

```
global x = 1
global y = 2

thread T1        thread T2
   a1: y = x        b1: x = y
```

### Semántica de los hilos

```
⟦T1⟧ = λσ. σ[y ↦ σx]
⟦T2⟧ = λσ. σ[x ↦ σy]
```

### Semántica concurrente

Cada thread tiene una sola instrucción atómica, así que hay exactamente dos intercalados
posibles: `a1;b1` o `b1;a1`.

- **a1 luego b1:** `y ← σx`, y después `x ← ` (el nuevo `y`) `= σx`. Resultado:
  `σ[x ↦ σx, y ↦ σx]` — o sea, ambas quedan con el valor **inicial de x**.
- **b1 luego a1:** `x ← σy`, y después `y ← ` (el nuevo `x`) `= σy`. Resultado:
  `σ[x ↦ σy, y ↦ σy]` — ambas con el valor **inicial de y**.

```
⟦T1|T2⟧ = λσ. σ[x ↦ σx, y ↦ σx]  ⊕  λσ. σ[x ↦ σy, y ↦ σy]
```

Observación linda: pase lo que pase, `x` e `y` terminan **iguales entre sí**. Lo único no
determinístico es cuál de los dos valores iniciales sobrevive.

### Diagrama de transición (desde x=1, y=2)

```
                    ⟨x=1, y=2 | T1:a1, T2:b1⟩
                       │                  │
                    a1 │                  │ b1
                       ▼                  ▼
      ⟨x=1, y=1 | T1:—, T2:b1⟩    ⟨x=2, y=2 | T1:a1, T2:—⟩
                       │                  │
                    b1 │                  │ a1
                       ▼                  ▼
      ⟨x=1, y=1 | T1:—, T2:—⟩     ⟨x=2, y=2 | T1:—, T2:—⟩
              (FINAL)                    (FINAL)
```

**Estados finales:** `(x=1, y=1)` y `(x=2, y=2)`.

## 1.b

```
global x = 0
global y = 0

thread T1              thread T2
   a1: y = x + 1          b1: x = y + 1
```

### Semántica de los hilos

```
⟦T1⟧ = λσ. σ[y ↦ σx + 1]
⟦T2⟧ = λσ. σ[x ↦ σy + 1]
```

### Semántica concurrente

- **a1 luego b1:** `y ← σx+1`; después `x ← y+1 = σx+2`. Resultado:
  `σ[y ↦ σx+1, x ↦ σx+2]`.
- **b1 luego a1:** `x ← σy+1`; después `y ← x+1 = σy+2`. Resultado:
  `σ[x ↦ σy+1, y ↦ σy+2]`.

```
⟦T1|T2⟧ = λσ. σ[y ↦ σx+1, x ↦ σx+2]  ⊕  λσ. σ[x ↦ σy+1, y ↦ σy+2]
```

### Diagrama de transición (desde x=0, y=0)

```
                    ⟨x=0, y=0 | T1:a1, T2:b1⟩
                       │                  │
                    a1 │                  │ b1
                       ▼                  ▼
      ⟨x=0, y=1 | T1:—, T2:b1⟩    ⟨x=1, y=0 | T1:a1, T2:—⟩
                       │                  │
                    b1 │                  │ a1
                       ▼                  ▼
      ⟨x=2, y=1 | T1:—, T2:—⟩     ⟨x=1, y=2 | T1:—, T2:—⟩
              (FINAL)                    (FINAL)
```

**Estados finales:** `(x=2, y=1)` y `(x=1, y=2)`.

Notar la diferencia con 1.a: acá los dos estados finales son **distintos entre sí y
asimétricos**. Este ejemplo va a servir para el Ejercicio 4.

## 1.c

```
global x = 0
global y = 0

thread T1                thread T2
   a1: while (x<1)          b1: x = 1
   a2:    y = y+1
```

Etiquetas: `a1` es la evaluación de la guarda, `a2` el cuerpo (después de `a2` se vuelve a
`a1`).

### Semántica de los hilos

`T1` aislado: si `x < 1` la guarda nunca cambia y el loop no termina.

```
⟦T1⟧ = λσ. if σx < 1 then ⊥ else σ
⟦T2⟧ = λσ. σ[x ↦ 1]
```

### Semántica concurrente

Acá aparece lo interesante. `T2` eventualmente pone `x = 1` (weak fairness), y con eso `T1`
sale del loop. Pero **cuántas vueltas dio antes es no determinístico y no está acotado**:
depende de cuándo el scheduler le dé el turno a `T2`.

```
⟦T1|T2⟧ = λσ. ⨁ₖ≥₀ σ[x ↦ 1, y ↦ σy + k]
```

es decir, la suma no determinística sobre todos los `k ≥ 0` posibles.

Casos borde que conviene tener claros:

- `k = 0`: `T2` ejecuta `b1` antes de que `T1` evalúe su guarda por primera vez. `T1`
  evalúa `x<1` con `x=1` → falso → termina sin incrementar nada.
- `k` arbitrario: `T1` da `k` vueltas antes de que `T2` corra.
- **Vuelta extra:** si `T2` ejecuta `b1` cuando `T1` ya pasó la guarda y está por ejecutar
  `a2`, `T1` igual hace ese incremento (ya pasó el control) y recién después sale. Esto es
  lo que hace que la cuenta sea "cuántas veces evaluó la guarda como verdadera", no
  "cuántas veces `x` valía 0".

**Sin la hipótesis de weak fairness** habría además una ejecución infinita donde `T2` nunca
corre, y el resultado sería `⊥`. Con weak fairness eso se descarta.

### Diagrama de transición

Este es **infinito**, que es exactamente lo que anticipa la slide 19. La estructura es una
escalera que se repite hacia abajo:

```
  ⟨x=0,y=0 | a1,b1⟩ ──a1──▶ ⟨x=0,y=0 | a2,b1⟩ ──a2──▶ ⟨x=0,y=1 | a1,b1⟩ ──a1──▶ ⟨x=0,y=1 | a2,b1⟩ ─▶ ⋯
         │                          │                          │                          │
      b1 │                       b1 │                       b1 │                       b1 │
         ▼                          ▼                          ▼                          ▼
  ⟨x=1,y=0 | a1,—⟩          ⟨x=1,y=0 | a2,—⟩          ⟨x=1,y=1 | a1,—⟩          ⟨x=1,y=1 | a2,—⟩
         │                          │                          │                          │
      a1 │ (guarda falsa)        a2 │                       a1 │ (guarda falsa)        a2 │
         ▼                          ▼                          ▼                          ▼
  ⟨x=1,y=0 | —,—⟩           ⟨x=1,y=1 | a1,—⟩          ⟨x=1,y=1 | —,—⟩           ⟨x=1,y=2 | a1,—⟩
     (FINAL)                        │                     (FINAL)                        │
                                 a1 │                                                 a1 │
                                    ▼                                                    ▼
                             ⟨x=1,y=1 | —,—⟩                                     ⟨x=1,y=2 | —,—⟩
                                (FINAL)                                             (FINAL)
```

**Fila superior:** `T2` todavía no corrió; `T1` alterna entre evaluar la guarda (`a1`) e
incrementar (`a2`), subiendo `y` de a uno. Es infinita hacia la derecha.

**Estados finales:** `⟨x=1, y=k | —,—⟩` para todo `k ≥ 0`. Infinitos.

---

# Ejercicio 2

```
global n = 0

thread T1              thread T2
   do K times             do K times
      n = n + 1              n = n + 1
```

Acá `n = n + 1` **no** es atómica (si lo fuera, el resultado siempre sería `2K` y los
incisos b y c no tendrían sentido). La desagrego como en la slide 27:

```
thread T1                   thread T2
   local t1                    local t2
   do K times                  do K times
      L1: t1 = n                  L2: t2 = n
      W1: n = t1 + 1              W2: n = t2 + 1
```

Notación abreviada: `L(v)` = el thread lee y obtiene `v`; `W(v)` = el thread escribe `v`.

## 2.a — Dos trazas con valor final 2K

**Traza 1 — ejecución secuencial.** `T1` completo, después `T2` completo.

| T1 | T2 | Estado |
|---|---|---|
| `t1 = n` (=0) | | t1=0; n=0 |
| `n = t1+1` | | n=1 |
| ⋯ (K veces en total) ⋯ | | n=K |
| | `t2 = n` (=K) | t2=K |
| | `n = t2+1` | n=K+1 |
| | ⋯ (K veces en total) ⋯ | **n=2K** |

Ningún incremento se pierde porque nunca hay dos lecturas sin una escritura en el medio.

**Traza 2 — alternancia de incrementos completos.** Los threads se turnan, pero cada uno
completa su par lectura/escritura antes de ceder.

| T1 | T2 | Estado |
|---|---|---|
| `t1 = n` (=0) | | t1=0 |
| `n = t1+1` | | n=1 |
| | `t2 = n` (=1) | t2=1 |
| | `n = t2+1` | n=2 |
| `t1 = n` (=2) | | t1=2 |
| `n = t1+1` | | n=3 |
| ⋯ alternando ⋯ | | **n=2K** |

La clave en ambas: **el cambio de contexto nunca cae entre la lectura y la escritura de un
mismo incremento**. Mientras eso se cumpla, cada incremento es efectivo.

## 2.b — Una traza con valor final K

Hay que perder exactamente `K` incrementos. La forma más limpia es hacer que **los dos
threads avancen en lockstep**: ambos leen el mismo valor, ambos escriben el mismo valor, y
cada "ronda" de dos incrementos ejecutados produce un solo incremento efectivo.

| T1 | T2 | Estado |
|---|---|---|
| `t1 = n` (=0) | | t1=0; n=0 |
| | `t2 = n` (=0) | t2=0; n=0 |
| `n = t1+1` | | n=1 |
| | `n = t2+1` | n=1 ← *se perdió uno* |
| `t1 = n` (=1) | | t1=1 |
| | `t2 = n` (=1) | t2=1 |
| `n = t1+1` | | n=2 |
| | `n = t2+1` | n=2 ← *se perdió otro* |
| ⋯ K rondas ⋯ | | **n=K** |

Ejecutaron `2K` incrementos, quedaron efectivos `K`.

**Traza alternativa (más compacta), también con resultado K:**

| T1 | T2 | Estado |
|---|---|---|
| K−1 incrementos completos | | n=K−1 |
| `t1 = n` (=K−1) | | t1=K−1 |
| | K incrementos completos | n=2K−1 |
| `n = t1+1` | | **n=K** ← una sola escritura tira abajo los K de T2 |

## 2.c — ¿Puede el valor final ser menor que K?

**Sí.** Para `K ≥ 3` es posible, y de hecho el mínimo alcanzable es **2**.

La intuición: en la traza de lockstep cada ronda desperdicia un solo incremento. Pero un
thread puede desperdiciar **muchos incrementos del otro de un saque**, si guarda una lectura
vieja mientras el otro avanza y después la usa para pisar todo.

**Traza que deja `n = 2`, para cualquier `K ≥ 2`:**

| T1 | T2 | Estado | Comentario |
|---|---|---|---|
| | `t2 = n` (=0) | t2=0; n=0 | T2 queda "congelado" con una lectura vieja |
| K−1 incrementos completos | | n=K−1 | T1 avanza sola |
| | `n = t2+1` | **n=1** | T2 completa su 1er incremento y tira abajo K−2 de T1 |
| `t1 = n` (=1) | | t1=1 | T1 arranca su último incremento y se congela |
| | K−1 incrementos completos | n=1+(K−1)=K | T2 termina sus K |
| `n = t1+1` | | **n=2** | T1 completa el suyo y tira abajo K−1 de T2 |

Verificación de la contabilidad: `T1` ejecutó `(K−1) + 1 = K` incrementos, `T2` ejecutó
`1 + (K−1) = K`. Total `2K` incrementos ejecutados, valor final `2`.

**Chequeo con K = 3:**

| paso | T1 | T2 | n |
|---|---|---|---|
| 1 | | `L(0)` → t2=0 | 0 |
| 2 | `L(0)`, `W(1)` | | 1 |
| 3 | `L(1)`, `W(2)` | | 2 |
| 4 | | `W(1)` | **1** |
| 5 | `L(1)` → t1=1 | | 1 |
| 6 | | `L(1)`, `W(2)` | 2 |
| 7 | | `L(2)`, `W(3)` | 3 |
| 8 | `W(2)` | | **2** |

`T1`: 3 incrementos ✓. `T2`: 3 incrementos ✓. Final: `n = 2 < 3 = K` ✓

### Cota inferior: el valor final nunca baja de 2 (para K ≥ 2)

Sea `W` la última escritura del programa, hecha por un thread `T`. Como es la última
operación, el valor final es exactamente lo que escribe `W`, o sea `r + 1` donde `r` es lo
que `T` leyó en su última lectura.

Ahora, `n ≥ 1` desde el momento en que ocurre la **primera** escritura del programa
(toda escritura es de la forma `r+1` con `r ≥ 0`, y `n` arranca en 0). Como `K ≥ 2`, la
última lectura de `T` ocurre después de al menos una escritura propia, así que en ese
momento `n ≥ 1`, o sea `r ≥ 1`. Por lo tanto el valor final es `r + 1 ≥ 2`. ∎

**Resumen del rango:** para `K ≥ 2`, el valor final está en `[2, 2K]`, y **todos** los valores
intermedios son alcanzables. (Para `K = 1` el rango es `[1, 2]`.)

> *Verificado por exploración exhaustiva del espacio de estados para `K = 1..6`: el conjunto
> de valores finales alcanzables es exactamente `{2, 3, …, 2K}` en todos los casos.*

---

# Ejercicio 3

```
global x = 1, y = 2, z = 3

thread T1    thread T2    thread T3
   y = x        z = y        x = z
```

Una instrucción atómica por thread ⇒ hay `3! = 6` intercalados posibles. Los recorro todos
sobre el estado inicial `(x,y,z) = (1,2,3)`:

| # | Orden | Paso a paso | Final `(x,y,z)` |
|---|---|---|---|
| 1 | T1,T2,T3 | `y←1` (1,1,3); `z←1` (1,1,1); `x←1` | **(1,1,1)** |
| 2 | T1,T3,T2 | `y←1` (1,1,3); `x←3` (3,1,3); `z←1` | **(3,1,1)** |
| 3 | T2,T1,T3 | `z←2` (1,2,2); `y←1` (1,1,2); `x←2` | **(2,1,2)** |
| 4 | T2,T3,T1 | `z←2` (1,2,2); `x←2` (2,2,2); `y←2` | **(2,2,2)** |
| 5 | T3,T1,T2 | `x←3` (3,2,3); `y←3` (3,3,3); `z←3` | **(3,3,3)** |
| 6 | T3,T2,T1 | `x←3` (3,2,3); `z←2` (3,2,2); `y←3` | **(3,3,2)** |

**Los 6 resultados son distintos:**

```
(1,1,1)   (3,1,1)   (2,1,2)   (2,2,2)   (3,3,3)   (3,3,2)
```

**Observación estructural.** Las tres asignaciones forman un ciclo de copias
`x → y → z → x`. Si los tres corren "en cadena" en el sentido del ciclo, un mismo valor se
propaga a las tres variables (casos 1, 4 y 5: los tres resultados uniformes `(1,1,1)`,
`(2,2,2)`, `(3,3,3)`). Si el orden rompe la cadena, quedan mezclas.

Notar que **ningún estado final pierde los tres valores originales a la vez**: siempre
sobrevive al menos uno de `{1,2,3}` en todas las variables, porque cada instrucción copia,
no calcula.

---

# Ejercicio 4

`P` = `N` threads, cada uno con exactamente `K` instrucciones atómicas, sin bucles ni
estructuras de control.

## 4.a — Cota inferior para la cantidad de nodos

Un nodo del diagrama de transición está determinado por **(estado de las variables, vector
de próximas instrucciones)** (slide 17).

Como ningún thread tiene control de flujo, cada thread pasa por exactamente `K+1`
"posiciones": antes de su instrucción 1, antes de la 2, …, antes de la K, y terminado
(`—`). Y como los threads avanzan de forma independiente, **toda combinación** de posiciones
es alcanzable: para cualquier `(i₁, …, i_N)` con `0 ≤ i_j ≤ K`, existe un intercalado donde
el thread `j` ejecutó exactamente `i_j` instrucciones.

Cada uno de esos vectores necesita al menos un nodo. Por lo tanto:

> **Cota inferior: (K+1)^N nodos.**

### ¿Cuándo la cota no es ajustada?

La cota se alcanza con igualdad sólo si **cada vector de posiciones se corresponde con un
único estado de memoria**. No es ajustada cuando dos caminos distintos llegan al mismo
vector de posiciones dejando estados de memoria diferentes: ahí hace falta más de un nodo
por vector.

- **Ajustada** cuando no hay interferencia real entre los threads: por ejemplo, si cada
  thread escribe únicamente en variables propias, o si las escrituras conmutan. Ahí el
  estado de memoria es función del vector de posiciones y hay exactamente `(K+1)^N` nodos.
- **No ajustada** apenas hay competencia por una variable compartida. El **Ejercicio 1.b**
  es el contraejemplo mínimo. Ahí `N = 2` y `K = 1`, así que la cota da `(1+1)² = 4`
  vectores de posiciones: `(a1,b1)`, `(—,b1)`, `(a1,—)`, `(—,—)`. Pero el diagrama tiene
  **5** nodos, porque el vector final `(—,—)` se alcanza con **dos** estados de memoria
  distintos: `(x=2,y=1)` por un camino y `(x=1,y=2)` por el otro. La cota inferior se
  cumple (`5 ≥ 4`) pero no es ajustada.

  El **Ejercicio 1.a** exhibe el mismo fenómeno: 5 nodos sobre 4 vectores, con `(—,—)`
  duplicado en `(1,1)` y `(2,2)`.

**Contraejemplo de cota ajustada.** Si en 1.a reemplazamos los threads por `T1: a = 1` y
`T2: b = 1` (cada uno escribe su propia variable), los cuatro vectores de posiciones se
corresponden con un único estado cada uno, y el diagrama tiene exactamente `4 = (1+1)²`
nodos.

**En una frase:** la cota es ajustada sii el programa es determinista en memoria — sii todo
intercalado que llega al mismo punto de control deja el mismo estado.

## 4.b — Cantidad total de trazas

Una traza es una secuencia de las `N·K` instrucciones que **respeta el orden interno de cada
thread**. Equivale a elegir, para cada thread, qué posiciones de la secuencia global ocupan
sus `K` instrucciones (el orden entre ellas ya está fijado).

Es el coeficiente multinomial:

> **Cantidad de trazas = (N·K)! / (K!)^N**

**Verificaciones:**

- Ej. 1 (`N=2, K=1`): `2! / (1!)² = 2` ✓ (dos intercalados)
- Ej. 3 (`N=3, K=1`): `3! / (1!)³ = 6` ✓ (los seis que enumeré)
- `N=2, K=2`: `4! / (2!)² = 6`

Notar que esto crece **muchísimo** más rápido que la cantidad de nodos: para `N=3, K=5` ya
son `15!/(5!)³ = 756.756` trazas contra a lo sumo unos pocos miles de nodos. Es exactamente
lo que dice la slide 38: hacer el diagrama completo para programas medianos es impracticable,
y enumerar trazas lo es todavía más. Por eso se argumenta con invariantes.

---

# Ejercicio 5

`f` tiene una raíz entera. `T1` prueba `1, 2, 3, …` y `T2` prueba `0, −1, −2, …`, de modo que
entre los dos cubren todos los enteros. El programa es **correcto si ambos threads terminan
cuando uno encuentra la raíz**.

Para las trazas asumo, sin pérdida de generalidad, que la raíz es un entero **positivo**
`r > 0` (la encuentra `T1`) y que `f(j) ≠ 0` para todo `j ≤ 0`.

## 5.a — Programa A: **INCORRECTO**

```
global found

thread T1 {                     thread T2 {
   local i = 0                     local j = 1
   found = false                   found = false
   while (!found) {                while (!found) {
      i = i + 1                       j = j - 1
      found = (f(i) == 0)             found = (f(j) == 0)
   }                               }
}                                }
```

Tiene **dos** defectos, ambos por escrituras destructivas sobre la global `found`:

**Defecto 1 — la inicialización `found = false` de un thread pisa el hallazgo del otro.**

| T1 | T2 | Estado |
|---|---|---|
| `found = false` | | found=false |
| itera hasta `i = r` | | found=**true** |
| `!found` → sale del while | | T1 **TERMINÓ** |
| | `found = false` | found=**false** ← se borró el hallazgo |
| | itera para siempre | T2 **NO TERMINA** |

**Defecto 2 (más grave, y el que hace que ni siquiera sirva reordenar) — cada iteración
escribe `found = (f(i)==0)`, que es `false` casi siempre.** Aunque un thread encuentre la
raíz, el otro la borra en su próxima vuelta:

| T1 | T2 | Estado |
|---|---|---|
| | evalúa `f(0) ≠ 0`, va a escribir | (aún no escribió) |
| itera hasta `i = r`, `found = true` | | found=true |
| `!found` → sale | | T1 terminó |
| | `found = false` | found=**false** |
| | itera para siempre | T2 **NO TERMINA** |

**Peor aún**, hay una traza donde ni siquiera `T1` termina: si `T2` escribe `found = false`
entre el momento en que `T1` ejecuta `found = true` y el momento en que evalúa `!found`,
`T1` no sale y sigue buscando una raíz que ya encontró (y que no volverá a aparecer).

**Conclusión:** A es incorrecto.

## 5.b — Programa B: **INCORRECTO**

```
global found = false

thread T1 {                     thread T2 {
   local i = 0                     local j = 1
   while (!found) {                while (!found) {
      i = i + 1                       j = j - 1
      found = (f(i) == 0)             found = (f(j) == 0)
   }                               }
}                                }
```

Respecto de A se eliminó la inicialización redundante (ahora `found` se inicializa una sola
vez, globalmente). Eso **elimina el defecto 1, pero no el defecto 2**, que es el estructural:

> `found = (f(i) == 0)` es una **asignación**, no una acumulación. Escribe `false` cada vez
> que el thread no encuentra la raíz, borrando lo que haya escrito el otro.

**Traza que lo rompe:**

| T1 | T2 | Estado |
|---|---|---|
| | `j = 0`; evalúa `f(0) ≠ 0` → obtiene `false` | está por escribir |
| itera hasta `i = r` | | |
| `found = (f(r)==0)` → `true` | | found=**true** |
| `!found` → sale del while | | T1 **TERMINÓ** |
| | `found = false` | found=**false** |
| | `j = −1, −2, …` para siempre | T2 **NO TERMINA** |

`T2` nunca vuelve a ver `true` porque no hay raíces negativas y `T1` ya no está para
volver a marcarla.

**Conclusión:** B es incorrecto. La diferencia con A es sólo que el bug requiere un
intercalado un poco más específico — pero sigue existiendo, y basta una traza para
refutar la corrección (slide 38).

## 5.c — Programa C: **CORRECTO**

```
global found = false

thread T1 {                     thread T2 {
   local i = 0                     local j = 1
   while (!found) {                while (!found) {
      i = i + 1                       j = j - 1
      if (f(i) == 0)                  if (f(j) == 0)
         found = true                    found = true
   }                               }
}                                }
```

El cambio decisivo: **`found` sólo se escribe con `true`**. Nunca se escribe `false`.

### Argumento de corrección

**Invariante (monotonía).** `found` es monótona: una vez que vale `true`, vale `true` para
siempre. Prueba directa: la única escritura del programa sobre `found` es `found = true`, y
la inicialización es previa al arranque de los threads. ∎

Con eso, las tres partes:

1. **Alguien encuentra la raíz.** Sea `r` la raíz. Si `r > 0`, `T1` la alcanza en `r`
   iteraciones; si `r ≤ 0`, `T2` la alcanza en `|r| + 1` iteraciones. Mientras `found` sea
   `false`, ese thread sigue iterando, y por **weak fairness** ejecuta infinitas veces, así
   que llega a `r` en tiempo finito. En ese momento ejecuta `found = true`.
   (Si `found` ya era `true` antes de eso, mejor todavía — ver punto 3.)

2. **Nadie lo desmarca.** Por la invariante de monotonía, `found` queda en `true`.

3. **Ambos threads terminan.** Cada uno evalúa `!found` al comienzo de cada iteración. Por
   weak fairness ambos llegan a evaluarla; como `found` es `true` y ya no cambia, la guarda
   da `false` y salen. ∎

**Detalle fino:** un thread puede dar **una vuelta de más** después de que `found` se puso en
`true` (si ya había pasado la guarda cuando el otro la marcó). Eso es inofensivo: evalúa un
`f` de más y sale en la siguiente evaluación de la guarda.

**Carrera de datos:** las dos escrituras posibles son ambas `true`, así que aunque se
solapen el resultado es `true`. No hay pérdida de información posible.

> ### ⚠ Nota que conecta con la última parte de la clase 1
>
> Este argumento vale **en el modelo de la práctica**, que asume Sequential Consistency. En
> Java real, `found` sin `volatile` podría no volverse visible nunca al otro thread: el
> compilador tiene derecho a cachearla en un registro y sacar la lectura fuera del loop
> (*hoisting*, slide 95). El programa C es correcto bajo SC, pero para que lo sea en una JVM
> hay que declarar `volatile boolean found`, que establece el happens-before necesario
> (slides 102-103).

---

# Ejercicio 6

```
global n = 0

thread T1                thread T2 {
   a1: while (n < 2)        b1: n = n + 1
   a2:    print(n)          b2: n = n + 1
                          }
```

Etiquetas: `a1` = evaluar guarda, `a2` = imprimir. `T2` tiene dos incrementos, `b1` y `b2`.

**Observación previa:** `n` es **monótona creciente** (sólo se incrementa), y va tomando los
valores `0 → 1 → 2`. Por lo tanto la secuencia impresa es siempre **no decreciente**, y
nunca aparece un valor después de otro mayor.

## 6.a — ¿Cuántas veces puede aparecer `2` en la salida?

> **A lo sumo una vez** (puede ser 0 o 1).

**Puede aparecer una vez.** Para imprimir `2`, `T1` tiene que haber pasado la guarda con
`n < 2` y que `n` llegue a `2` antes del `print`:

| T1 | T2 | Estado |
|---|---|---|
| | `n = n+1` | n=1 |
| `while (n<2)` → `1<2` ✓ | | pasa la guarda; IP a2 |
| | `n = n+1` | n=2 |
| `print(n)` | | **imprime 2** |
| `while (n<2)` → `2<2` ✗ | | T1 termina |

**No puede aparecer dos veces.** Después de imprimir `2`, `T1` vuelve a `a1` y evalúa
`n < 2` con `n = 2`; como `n` nunca decrece, la guarda es falsa y `T1` termina. Para volver
a imprimir habría que pasar la guarda otra vez, lo cual es imposible con `n ≥ 2`. ∎

## 6.b — ¿Cuántas veces puede aparecer `1` en la salida?

> **Cualquier cantidad finita `k ≥ 0`, sin cota superior.** Bajo weak fairness no puede ser
> infinita.

**Sin cota:** entre `b1` (que pone `n = 1`) y `b2` (que lo lleva a `2`) hay una ventana
durante la cual `T1` puede dar todas las vueltas que el scheduler le permita, imprimiendo
`1` cada vez:

| T1 | T2 | Estado |
|---|---|---|
| | `n = n+1` | n=1 |
| `while(1<2)` ✓, `print(1)` | | imprime 1 |
| `while(1<2)` ✓, `print(1)` | | imprime 1 |
| ⋯ k veces ⋯ | | imprime 1 (k-ésima) |
| | `n = n+1` | n=2 |
| `while(2<2)` ✗ | | T1 termina |

Para cualquier `k` existe un intercalado que imprime `1` exactamente `k` veces.

**No puede ser infinita (con weak fairness):** `T2` está permanentemente listo para ejecutar
`b2`, así que el scheduler no puede postergarlo para siempre. Una vez que ejecuta, `n = 2` y
`T1` sale en su próxima evaluación de la guarda. *(Sin la hipótesis de fairness, sí existiría
una ejecución infinita imprimiendo `1` por siempre.)*

Lo mismo vale, simétricamente, para la cantidad de veces que aparece `0`: cualquier cantidad
finita, antes de que `T2` ejecute `b1`.

## 6.c — Longitud de la secuencia más corta

> **0.** La salida puede ser vacía.

Basta con que `T2` complete sus dos incrementos antes de que `T1` evalúe su guarda por
primera vez:

| T1 | T2 | Estado |
|---|---|---|
| | `n = n+1` | n=1 |
| | `n = n+1` | n=2 |
| `while (n<2)` → `2<2` ✗ | | T1 termina **sin imprimir nada** |

*(Si el enunciado pretendiera una secuencia no vacía, la más corta tiene longitud **1**: la
traza del inciso a imprime únicamente `2`.)*

### Caracterización completa de las salidas posibles

Combinando todo, las secuencias que el programa puede producir son exactamente:

```
0ᵃ 1ᵇ 2ᶜ     con  a, b ≥ 0  y  c ∈ {0, 1}
```

es decir: una tira de ceros, después una tira de unos, y a lo sumo un `2` al final. Todas
finitas bajo weak fairness.

---

# Ejercicio 7

```
global n = 0

thread T1                    thread T2
   a1: while (n < 1)            b1: while (n >= 0)
   a2:    n = n + 1             b2:    n = n - 1
```

## 7.a — ¿Existe un interleaving donde el loop de T1 ejecute exactamente una vez?

> **Sí.**

Basta con que `T1` corra sola hasta salir, antes de que `T2` toque nada:

| T1 | T2 | Estado |
|---|---|---|
| `while (n<1)` → `0<1` ✓ | | n=0; IP a2 |
| `n = n+1` | | **n=1**; IP a1 |
| `while (n<1)` → `1<1` ✗ | | T1 **TERMINA** (cuerpo ejecutado 1 vez) |
| | `while (n≥0)` → `1≥0` ✓ | |
| | `n = n−1` | n=0 |
| | `while (n≥0)` → `0≥0` ✓ | |
| | `n = n−1` | n=−1 |
| | `while (n≥0)` → `−1≥0` ✗ | T2 **TERMINA** |

**Justificación:** el cuerpo de `T1` se ejecutó exactamente una vez, porque `T1` evaluó la
guarda como verdadera una sola vez. Esto es posible porque nada obliga al scheduler a
intercalar: darle el procesador a `T1` hasta que salga del loop es una traza válida (y
además weakly fair, ya que después `T2` corre y ambos terminan).

## 7.b — ¿Existe un interleaving donde el loop de T1 no termine?

> **Sí**, y además es un intercalado **perfectamente weakly fair** — lo cual lo hace más
> interesante que un simple caso de inanición.

La idea: `T2` decrementa `n` a `0` justo antes de cada evaluación de la guarda de `T1`, de
modo que `T1` nunca llega a ver `n ≥ 1`.

| T1 | T2 | Estado |
|---|---|---|
| `while (n<1)` → `0<1` ✓ | | IP a2 |
| `n = n+1` | | n=1 |
| | `while (n≥0)` → `1≥0` ✓ | IP b2 |
| | `n = n−1` | **n=0** |
| `while (n<1)` → `0<1` ✓ | | IP a2 |
| `n = n+1` | | n=1 |
| | `while (n≥0)` → `1≥0` ✓ | |
| | `n = n−1` | **n=0** |
| ⋯ se repite indefinidamente ⋯ | | |

**Justificación:**

- `T1` nunca termina: cada vez que evalúa `n < 1`, el valor es `0`, porque `T2` lo bajó.
- `T2` tampoco termina: cada vez que evalúa `n ≥ 0`, el valor es `1` (o `0`), nunca negativo.
- **Es weakly fair:** ambos threads ejecutan infinitas veces; ninguno está siendo ignorado
  por el scheduler. La hipótesis de fairness de la slide 31 **no descarta** esta ejecución.

Esto es un **livelock**: los dos threads están permanentemente activos ejecutando
instrucciones, y sin embargo ninguno progresa hacia su terminación. Es la distinción que
importa contra el deadlock del slide 33, donde los threads también giran para siempre pero
por una condición que ya no puede cambiar.

---

# Ejercicio 8

```
global n = 0
global flag = false

thread A                     thread B
   a1: while (!flag)            b1: while (!flag)
   a2:    n = 1 - n             b2:    if (n == 0)
                                b3:       flag = true
```

`A` alterna `n` entre `0` y `1`. `B` levanta la bandera cuando **observa** `n == 0`.

Etiquetas: `b2` es la evaluación de la condición del `if`; `b3` la asignación (son dos pasos
distintos, y esa separación importa).

## 8.a — Posibles valores finales de `n`

> **`n` puede terminar valiendo `0` o `1`. Ambos son alcanzables.**

**`n = 0` es alcanzable:**

| A | B | Estado |
|---|---|---|
| | `while(!flag)` ✓ | n=0 |
| | `if (n==0)` → ✓ | IP b3 |
| | `flag = true` | flag=true, n=0 |
| `while(!flag)` → ✗ | | A **TERMINA** |
| | `while(!flag)` → ✗ | B **TERMINA**; **n = 0** |

**`n = 1` es alcanzable:** basta con que `A` esté "en el aire" (ya pasó su guarda) cuando `B`
levanta la bandera. Como `A` ya pasó el control, ejecuta el cuerpo una vez más:

| A | B | Estado |
|---|---|---|
| `while(!flag)` → ✓ | | IP a2 (pasó la guarda) |
| | `while(!flag)` ✓; `if (n==0)` ✓ | IP b3 |
| | `flag = true` | flag=true, n=0 |
| `n = 1 - n` | | **n=1** |
| `while(!flag)` → ✗ | | A **TERMINA** |
| | `while(!flag)` → ✗ | B **TERMINA**; **n = 1** |

**Justificación de que no hay otros valores:** `n` sólo se modifica con `n = 1 − n`,
partiendo de `0`. Por inducción trivial, `n ∈ {0,1}` en todo momento. ∎

**Variante que también da `n = 1`** (muestra que la carrera está entre `b2` y `b3`, no sólo
en la guarda de `A`): `B` evalúa `if (n==0)` cuando `n = 0`, pero antes de ejecutar `b3`,
`A` ejecuta `n = 1 − n` dejando `n = 1`. `B` levanta igual la bandera — la decisión ya
estaba tomada sobre un valor que quedó obsoleto.

## 8.b — ¿Puede una ejecución no terminar?

> **Sí.**

El programa termina sólo si `B` llega a **observar** `n == 0` en su evaluación `b2`. Nada lo
garantiza: `A` puede estar siempre "del otro lado" del toggle cuando `B` mira.

| A | B | Estado |
|---|---|---|
| `while(!flag)` ✓; `n = 1−n` | | n=1 |
| | `while(!flag)` ✓; `if (n==0)` → **✗** | vuelve a b1 |
| `while(!flag)` ✓; `n = 1−n` | | n=0 |
| `while(!flag)` ✓; `n = 1−n` | | n=1 ← A da dos vueltas |
| | `while(!flag)` ✓; `if (n==0)` → **✗** | vuelve a b1 |
| ⋯ se repite indefinidamente ⋯ | | flag nunca se levanta |

**Justificación:**

- `B` sólo escribe `flag = true` si su evaluación `b2` cae en un instante con `n == 0`. En
  esta traza siempre cae con `n == 1`.
- `flag` queda en `false` para siempre, así que ninguno de los dos sale de su `while`.
- **Es weakly fair:** ambos threads ejecutan infinitas veces. Weak fairness garantiza que un
  thread *ejecute*, no que sus lecturas caigan en momentos favorables — que es justo la
  distinción que este ejercicio quiere marcar.

Otra vez un **livelock**, y la moraleja: el programa depende de una coincidencia de timing
que ninguna hipótesis del modelo asegura. Un programa concurrente correcto no puede depender
de "seguro que en algún momento va a mirar en el momento justo".

---
# Ejercicio 9 — Bakery para dos threads

```
global np = 0
global nq = 0

thread p                              thread q
   while(true){                          while(true){
      np = nq + 1                           nq = np + 1
      while (nq != 0 && np > nq){}           while (np != 0 && nq > np){}
      // seccion critica                     // seccion critica
      np = 0                                 nq = 0
   }                                     }
```

**La idea del algoritmo:** cada thread se asigna un número mayor que el del otro. Espera
mientras el otro tenga número (`nq != 0`) y el propio sea mayor (`np > nq`) — es decir,
cede el paso a quien llegó primero. Al salir devuelve su número poniéndolo en `0`.

> ## Respuesta: **NO resuelve el problema de la exclusión mutua.**

## El problema: `np = nq + 1` no es atómica

Esa instrucción **lee una variable compartida y escribe otra**. Desagregándola como en la
slide 27:

```
thread p                          thread q
   local pt                          local qt
   p1: pt = nq                       q1: qt = np
   p2: np = pt + 1                   q2: nq = qt + 1
   p3: while (nq!=0 && np>nq){}      q3: while (np!=0 && nq>np){}
   p4: // SECCION CRITICA            q4: // SECCION CRITICA
   p5: np = 0                        q5: nq = 0
```

## Traza que viola Mutex

Si ambos leen el número del otro **antes** de que ninguno escriba el suyo, los dos calculan
el mismo número — y **el empate no está desempatado por nada**.

| p | q | Estado |
|---|---|---|
| `pt = nq` | | p.pt = 0; p:p2 |
| | `qt = np` | q.qt = 0; q:q2 |
| `np = pt + 1` | | **np = 1**; p:p3 |
| | `nq = qt + 1` | **nq = 1**; q:q3 |
| `while (nq!=0 && np>nq)` | | `(1≠0)` ✓ **&&** `(1>1)` ✗ ⟹ falso; p:p4 |
| `// SECCION CRITICA` | | **p ENTRA** |
| | `while (np!=0 && nq>np)` | `(1≠0)` ✓ **&&** `(1>1)` ✗ ⟹ falso; q:q4 |
| | `// SECCION CRITICA` | **q ENTRA** |

**Los dos threads en la sección crítica simultáneamente. Mutex violado.** ∎

Y por lo tanto tampoco resuelve el problema, que exige las tres propiedades juntas.

## Por qué falla: le falta el desempate

La condición de espera es `np > nq` — **estricta**. Cuando `np == nq`, ninguno de los dos
cede y ambos pasan. El algoritmo asume implícitamente que los números son únicos, pero nada
lo garantiza si la asignación no es atómica.

Comparar con el **bakery real** (Ejercicio 13), cuya condición de espera es:

```
numero[j] < numero[id]  ||  (numero[j] == numero[id] && j < id)
                                                       ^^^^^^^^
```

Ese `j < id` es precisamente el **desempate por identidad de thread**: cuando dos threads
sacan el mismo número, gana el de menor `id`, y exactamente uno pasa. Sin ese término, el
empate es simétrico y rompe el algoritmo — acá dejando pasar a los dos, y en el Ej. 13
(donde la comparación es `≤`) trabando a los dos.

## Observación: ¿y si `np = nq + 1` **fuera** atómica?

Vale la pena verlo, porque cambia la respuesta y es un buen ejercicio de invariantes.

**Invariante:** con la asignación atómica, **nunca se alcanza `np == nq ≠ 0`.**

*Prueba.* Las únicas escrituras son: `np ← nq+1`, `np ← 0` (por `p`), y `nq ← np+1`,
`nq ← 0` (por `q`). Inmediatamente después de `np ← nq+1` vale `np = nq+1 > nq`, o sea
`np ≠ nq`. Simétricamente para `nq ← np+1`. Y después de un `← 0`, si coinciden es porque
ambos valen `0`, caso excluido por la hipótesis. Como entre escrituras nada cambia, el
empate con valores no nulos es inalcanzable. ∎

Con esa invariante, si `p` y `q` estuvieran ambos en la SC, cada uno pasó su guarda con el
otro ya anotado, lo que exige `np ≤ nq` **y** `nq ≤ np` con ambos no nulos, o sea
`np == nq ≠ 0`: imposible. **Mutex se cumple.**

**Tampoco hay deadlock:** los dos esperan simultáneamente sólo si `np > nq` y `nq > np`, que
es contradictorio.

**Garantía de entrada:** también se cumple, y por una razón elegante. Si `p` sale de la SC y
se re-anota, ejecuta `np = nq + 1 > nq`, lo que hace **falsa** la guarda de espera de `q`
(que era `nq > np`). O sea: reanotarse le **cede** el paso al otro, en vez de robárselo. Es
exactamente el mecanismo del bakery.

> **Moraleja del ejercicio:** el algoritmo es conceptualmente correcto, pero su corrección
> depende por completo de una atomicidad que no tiene. Es el mismo fenómeno de las slides
> 35-37: la propiedad se rompe **sólo** al nivel de grano fino.

---

# Ejercicio 10 — Turnos con contador

```
global actual = 0
global turnos = 0

PedirTurno(){                    LiberarTurno(){
   local turno = turnos             actual = actual + 1
   turnos = turnos + 1              turnos = turnos - 1
   return turno                  }
}

// protocolo de cada thread:
//SECCION NO CRITICA
local miturno = PedirTurno()
while (actual != miturno){}
//SECCION CRITICA
LiberarTurno()
//SECCION NO CRITICA
```

## 10.a — La propuesta no resuelve el problema

Hay **dos** defectos independientes. El primero es de atomicidad; el segundo es de diseño y
sobrevive incluso a la atomicidad (por eso el inciso b tiene gracia).

### Defecto 1 — `PedirTurno` no es atómica ⟹ **viola Mutex**

`PedirTurno` lee `turnos` en una local y después lo incrementa: es exactamente la pérdida de
sumas de la slide 29. Dos threads pueden llevarse **el mismo turno**:

| T1 | T2 | Estado |
|---|---|---|
| `turno = turnos` | | T1.turno = 0; turnos = 0 |
| | `turno = turnos` | T2.turno = **0**; turnos = 0 |
| `turnos = turnos + 1` | | turnos = 1 |
| | `turnos = turnos + 1` | turnos = **1** ← se perdió un incremento |
| `while (actual != 0)` | | `actual = 0` ⟹ falso |
| `//SECCION CRITICA` | | **T1 ENTRA** |
| | `while (actual != 0)` | `actual = 0` ⟹ falso |
| | `//SECCION CRITICA` | **T2 ENTRA** |

**Mutex violado.** ∎

### Defecto 2 — `turnos = turnos - 1` recicla números ⟹ **viola Ausencia de Deadlock y Garantía de Entrada**

En un *ticket lock* correcto, el dispensador de números **sólo crece**: es un contador de
"cuántos tickets se entregaron en la historia". Acá `LiberarTurno` lo **decrementa**, de modo
que un número ya usado vuelve a estar disponible mientras `actual` sigue avanzando. El
resultado es que un thread puede sacar un turno **que ya pasó**, y esperarlo para siempre.

| Thread | Acción | `actual` | `turnos` | miturno |
|---|---|---|---|---|
| T1 | `PedirTurno()` | 0 | 1 | 0 |
| T1 | `while(actual != 0)` → entra a la SC | 0 | 1 | 0 |
| T1 | `LiberarTurno()` | **1** | **0** | |
| T2 | `PedirTurno()` | 1 | 1 | **0** |
| T2 | `while (actual != 0)` → `1 ≠ 0` | 1 | 1 | 0 |
| | **T2 espera para siempre**: `actual` sólo crece, nunca vuelve a `0` | | | |

Con `T2` bloqueado indefinidamente y **nadie** en la sección crítica, se viola la **ausencia
de deadlock** (el sistema entero deja de progresar) y, a fortiori, la **garantía de entrada**.

### Resumen del inciso a

| Propiedad | ¿Se cumple? | Por qué |
|---|---|---|
| **Mutex** | ❌ NO | `PedirTurno` no atómica ⟹ dos threads con el mismo turno |
| **Ausencia de deadlock** | ❌ NO | el decremento de `turnos` entrega turnos ya vencidos |
| **Garantía de entrada** | ❌ NO | el deadlock anterior lo prueba (slide 34) |

## 10.b — ¿Y si `PedirTurno` y `LiberarTurno` fueran atómicas?

> **Sigue sin resolver el problema.** La atomicidad tapa el Defecto 1, pero **el Defecto 2 es
> independiente de la atomicidad** y de hecho permite violar *incluso Mutex*.

**Traza con ambas operaciones atómicas que viola Mutex:**

| Thread | Acción | `actual` | `turnos` | miturno |
|---|---|---|---|---|
| T1 | `PedirTurno()` | 0 | 1 | 0 |
| T2 | `PedirTurno()` | 0 | 2 | 1 |
| T1 | entra a la SC (`actual == 0`) | 0 | 2 | 0 |
| T1 | `LiberarTurno()` | **1** | **1** | |
| T3 | `PedirTurno()` | 1 | 2 | **1** ← ¡el mismo que T2! |
| T2 | `while (actual != 1)` → falso | 1 | 2 | 1 |
| T2 | `//SECCION CRITICA` | | | **T2 ENTRA** |
| T3 | `while (actual != 1)` → falso | 1 | 2 | 1 |
| T3 | `//SECCION CRITICA` | | | **T3 ENTRA** |

`T2` y `T3` comparten el turno `1` y entran juntos. **Mutex violado con operaciones
atómicas.** ∎

Y la traza de inanición del Defecto 2 sigue valiendo tal cual. Conclusión: la atomicidad es
**necesaria pero no suficiente**; el algoritmo está mal diseñado.

## Cómo se arregla

Dos cambios:

```
PedirTurno(){              // ATÓMICA (fetch-and-add)
   local turno = turnos
   turnos = turnos + 1     // el dispensador SÓLO crece
   return turno
}

LiberarTurno(){            // ATÓMICA
   actual = actual + 1     // ← se elimina  turnos = turnos - 1
}
```

Con eso queda el *ticket lock* clásico, que es lo que pide el Ejercicio 14. La justificación
de correctitud está desarrollada allá.

---

# Ejercicio 11 — Peterson "en anillo" para n threads

```
global flag[n] = {false, false, ..., false}
global turno = 0

thread(id) {
   //SECCION NO CRITICA
   f1: flag[id] = true
   f2: local otro = (id + 1) % n
   f3: turno = otro
   f4: while (flag[otro] && turno == otro){}
   f5: //SECCION CRITICA
   f6: flag[id] = false
   //SECCION NO CRITICA
}
```

> ## Respuesta: **NO resuelve el problema para n > 2. Falla Mutex.**

## El defecto de fondo

Peterson para 2 threads funciona porque cada thread mira **a su único competidor**. Esta
generalización conserva la forma sintáctica pero cambia el significado: cada thread mira
**sólo a su vecino en el anillo** `(id+1) % n`, e ignora a los otros `n−2`.

Para `n = 2`, `(id+1)%2` es efectivamente "el otro", y el algoritmo coincide con Peterson.
Para `n > 2`, `T0` sólo se cuida de `T1`, `T1` sólo de `T2`, etc. — **nadie vigila a los
threads no adyacentes**, y nada impide que dos threads que no se miran entre sí entren a la
vez.

## Traza que viola Mutex (n = 3)

`T0` mira a `T1`; `T1` mira a `T2`; `T2` mira a `T0`.

| # | Thread | Instrucción | Estado |
|---|---|---|---|
| 1 | T0 | `flag[0] = true` | flag = [**T**, F, F], turno = 0 |
| 2 | T0 | `otro = 1` | T0.otro = 1 |
| 3 | T0 | `turno = 1` | turno = **1** |
| 4 | T0 | `while (flag[1] && turno==1)` | `(F && T)` = **falso** |
| 5 | T0 | `//SECCION CRITICA` | **T0 ENTRA** |
| 6 | T1 | `flag[1] = true` | flag = [T, **T**, F] |
| 7 | T1 | `otro = 2` | T1.otro = 2 |
| 8 | T1 | `turno = 2` | turno = **2** |
| 9 | T1 | `while (flag[2] && turno==2)` | `(F && T)` = **falso** |
| 10 | T1 | `//SECCION CRITICA` | **T1 ENTRA** |

`T0` y `T1` están simultáneamente en la sección crítica. **Mutex violado.** ∎

La traza es tan corta porque ni siquiera hace falta una carrera fina: `T0` mira `flag[1]`
**antes** de que `T1` se anote, y `T1` mira `flag[2]`, que corresponde a un thread que ni
siquiera está compitiendo. Cada uno consulta a la persona equivocada.

## Análisis de las tres propiedades

### Mutex: ❌ **NO se cumple** (traza arriba).

### Ausencia de deadlock: ✅ **SÍ se cumple**

*Argumento.* Supongamos que todos los threads que quieren entrar están esperando en `f4`.
Sea `t` el valor actual de `turno` (estable, porque quien espera no escribe `turno`).

Un thread `T_k` espera sólo si `turno == (k+1)%n`, es decir sólo si `(k+1)%n == t`. Como el
mapa `k ↦ (k+1)%n` es una biyección, **hay a lo sumo un `k` que satisface eso**: sólo
`T_{t−1 mod n}` puede estar esperando por esa condición. Todos los demás threads que quieren
entrar tienen `turno ≠ otro` y por lo tanto **pasan directamente** a la sección crítica.

Y si el único que espera es `T_{t−1}`, su condición exige además `flag[t] == true`, o sea
que `T_t` está compitiendo. Dos casos:

- `T_t` ya pasó su `while`: está en la SC ⟹ hay progreso.
- `T_t` está por ejecutar `f3` (`turno = (t+1)%n`): al hacerlo, `turno` deja de valer `t`,
  con lo cual la guarda de `T_{t−1}` se vuelve falsa y **entra**.

En todos los casos alguien progresa. No hay deadlock. ∎

### Garantía de entrada: ✅ **SÍ se cumple**

*Argumento.* Sea `T_k` esperando en `f4`. Su guarda es `flag[m] && turno == m` con
`m = (k+1)%n`. Para que `T_k` quede bloqueado para siempre, **ambos** conjuntos tienen que
mantenerse verdaderos indefinidamente. Pero:

- Si `T_m` deja de competir, ejecuta `flag[m] = false` (`f6`) y la guarda cae ⟹ `T_k` entra.
- Si `T_m` compite infinitas veces, cada vez que se re-anota ejecuta `turno = (m+1)%n ≠ m`,
  y la guarda cae ⟹ `T_k` entra.

Por weak fairness `T_k` llega a evaluar la guarda después de ese cambio, así que entra en
tiempo finito. ∎

### Resumen

| Propiedad | ¿Se cumple? |
|---|---|
| **Mutex** | ❌ NO — cada thread vigila a un solo vecino |
| **Ausencia de deadlock** | ✅ SÍ |
| **Garantía de entrada** | ✅ SÍ |

Que las dos propiedades de *liveness* se cumplan no salva nada: **un algoritmo de exclusión
mutua que no garantiza mutex no sirve para nada**. Acá el algoritmo es "demasiado
permisivo", que es la falla más peligrosa (falla en silencio, sin colgarse).

---

# Ejercicio 12 — `algunVerdadero`

```
global flag[n] = {false, false, ..., false}

algunVerdadero(id) {
   local aux = false
   for (int i = 0; i < n; i++) {
      if (i != id)
         aux = aux || flag[i]
   }
   return aux
}

thread(id) {
   //SECCION NO CRITICA
   g1: flag[id] = true
   g2: while (algunVerdadero(id)){}
   g3: //SECCION CRITICA
   g4: flag[id] = false
   //SECCION NO CRITICA
}
```

> ## Respuesta: **NO resuelve el problema. Falla Ausencia de Deadlock.**
>
> Y — dato importante — **lo que falla NO es Mutex**: eso sí se cumple, con atomicidad o sin
> ella.

## 12.a — Sin atomicidad de `algunVerdadero`

### Ausencia de deadlock: ❌ **NO se cumple**

Este es el defecto real. Cada thread **levanta su bandera y no la baja hasta salir de la
sección crítica**. Si todos se anuncian antes de que alguno mire, todos ven a alguien más
levantado y todos esperan — para siempre, porque ninguno tiene forma de ceder.

**Traza con n = 3:**

| # | Thread | Instrucción | Estado |
|---|---|---|---|
| 1 | T0 | `flag[0] = true` | flag = [**T**, F, F] |
| 2 | T1 | `flag[1] = true` | flag = [T, **T**, F] |
| 3 | T2 | `flag[2] = true` | flag = [T, T, **T**] |
| 4 | T0 | `algunVerdadero(0)` → lee flag[1]=T, flag[2]=T | devuelve **true** ⟹ T0 espera |
| 5 | T1 | `algunVerdadero(1)` → lee flag[0]=T, flag[2]=T | devuelve **true** ⟹ T1 espera |
| 6 | T2 | `algunVerdadero(2)` → lee flag[0]=T, flag[1]=T | devuelve **true** ⟹ T2 espera |
| 7 | — | los tres reevalúan indefinidamente; **ningún flag baja nunca** | **DEADLOCK** |

Ninguno de los tres puede progresar: para bajar su flag hay que salir de la SC, y para
entrar a la SC hay que ver todos los flags en `false`. **Deadlock.** ∎

### Garantía de entrada: ❌ **NO se cumple**

La existencia del deadlock lo prueba directamente: hay threads que quieren entrar y no entran
nunca. Es el mismo razonamiento del slide 34.

### Mutex: ✅ **SÍ se cumple** (incluso sin atomicidad)

Este es el punto más interesante del ejercicio y hay que argumentarlo bien, porque la
intuición dice lo contrario.

*Argumento (idéntico en forma al análisis de Dekker del slide 66).* Supongamos que `T_i` y
`T_j` (`i ≠ j`) están simultáneamente en la sección crítica. Denotemos, con `≺` el orden en
que ocurren las operaciones en la traza:

- `W_i` = "`T_i` ejecuta `flag[i] = true`"
- `R_ij` = "`T_i` lee `flag[j]` y obtiene `false`" (dentro de su `algunVerdadero` exitoso)

Para que `T_i` haya entrado, su `algunVerdadero(i)` devolvió `false`, así que leyó **todos**
los otros flags en `false`; en particular ocurrió `R_ij`. Y por orden de programa,
`W_i ≺ R_ij`. Simétricamente, `W_j ≺ R_ji`.

Además, `R_ij` obtuvo `false`, de modo que ocurrió **antes** de que `T_j` levantara su
bandera: `R_ij ≺ W_j`. Simétricamente, `R_ji ≺ W_i`.

Encadenando:

```
W_i ≺ R_ij ≺ W_j ≺ R_ji ≺ W_i
```

Es un **ciclo**: contradicción. Por lo tanto no puede haber dos threads en la SC. ∎

Notar que el argumento **no usa** la atomicidad de `algunVerdadero`: sólo usa que cada
lectura de `flag[j]` ocurre después de la escritura de `flag[i]`, lo cual está garantizado
por el orden de programa. Cada bandera se levanta **antes** de mirar las demás, y eso alcanza.

### Resumen del inciso a

| Propiedad | ¿Se cumple? | Por qué |
|---|---|---|
| **Mutex** | ✅ SÍ | ciclo imposible `W_i ≺ R_ij ≺ W_j ≺ R_ji ≺ W_i` |
| **Ausencia de deadlock** | ❌ NO | todos levantan la bandera y ninguno cede |
| **Garantía de entrada** | ❌ NO | el deadlock lo prueba |

## 12.b — ¿Qué sucede si `algunVerdadero` es atómica?

> **No cambia nada relevante: el deadlock persiste.**

La razón es que **el problema no está en `algunVerdadero`**. La escritura `flag[id] = true`
está **fuera** de la función: es una instrucción del thread, previa a la llamada. La
atomicidad de `algunVerdadero` garantiza que el recorrido del array vea una foto consistente
del vector de flags, pero la traza del deadlock nunca necesitó una foto inconsistente — los
tres flags ya estaban en `true` cuando los tres miraron.

La misma traza de arriba funciona palabra por palabra, sólo que ahora los pasos 4, 5 y 6 son
cada uno una única operación atómica que devuelve `true`.

| Propiedad | Sin atomicidad | Con atomicidad |
|---|---|---|
| **Mutex** | ✅ SÍ | ✅ SÍ (el argumento se vuelve más directo) |
| **Ausencia de deadlock** | ❌ NO | ❌ **NO** |
| **Garantía de entrada** | ❌ NO | ❌ **NO** |

## Qué le falta al algoritmo

Este es, esencialmente, el **primer intento fallido de Dekker**: sólo banderas, sin
mecanismo de cesión. Lo que falta es una forma de que un thread **retire temporalmente su
pretensión** para romper la simetría — el `turno` de Peterson, o el número de orden del
bakery. Sin eso, la simetría perfecta produce bloqueo perfecto.

> **Contraste didáctico con el Ejercicio 11:** aquel algoritmo tenía las dos propiedades de
> liveness pero no mutex; éste tiene mutex pero ninguna de las de liveness. Son las dos
> formas complementarias de equivocarse, y ninguna de las dos resuelve el problema.

---

# Ejercicio 13 — Bakery sin la condición `j < id`

```
global entrando[N] = {false, ..., false}
global numero[N]   = {0, ..., 0}

thread(id) {
   //SECCION NO CRITICA
   h1: entrando[id] = true
   h2: numero[id] = 1 + max(numero[0], ..., numero[n-1])
   h3: entrando[id] = false

   h4: for (j = 0; j < n; j++) {
   h5:    while (entrando[j]){}
   h6:    while (numero[j] != 0 && (numero[j] <= numero[id] ||
                                   (numero[j] == numero[id] && j != id))){}
       }
   h7: //SECCION CRITICA
   h8: numero[id] = 0
   //SECCION NO CRITICA
}
```

**Simplificación previa de la guarda.** Como `numero[j] <= numero[id]` ya incluye el caso de
igualdad, el segundo término del `||` es redundante. La condición de espera efectiva es:

```
numero[j] != 0  &&  numero[j] <= numero[id]
```

Comparar con el bakery original, cuya condición es
`numero[j] < numero[id] || (numero[j] == numero[id] && j < id)`. La diferencia es exactamente
el tratamiento del **empate**: el original lo resuelve por `id`, el modificado hace que
**ambos cedan**.

> ## Propiedad violada: **Ausencia de Deadlock** (y con ella, Garantía de Entrada).
> ## Propiedad que sigue valiendo: **Mutex**.

## Traza que produce el deadlock

Con `n = 2` (threads `T0` y `T1`). La clave es que `numero[id] = 1 + max(...)` **no es
atómica**: los dos pueden calcular el `max` antes de que ninguno escriba, y sacar el mismo
número.

| # | T0 | T1 | Estado |
|---|---|---|---|
| 1 | `entrando[0] = true` | | entrando = [T, F] |
| 2 | | `entrando[1] = true` | entrando = [T, T] |
| 3 | calcula `max(0,0) = 0` | | (aún no escribió) |
| 4 | | calcula `max(0,0) = 0` | (aún no escribió) |
| 5 | `numero[0] = 1` | | numero = [**1**, 0] |
| 6 | | `numero[1] = 1` | numero = [1, **1**] ← **EMPATE** |
| 7 | `entrando[0] = false` | | entrando = [F, T] |
| 8 | | `entrando[1] = false` | entrando = [F, F] |
| 9 | `j=1`: `while(entrando[1])` → F | | pasa |
| 10 | `j=1`: `numero[1]≠0` ✓ **&&** `1 <= 1` ✓ | | **T0 ESPERA a T1** |
| 11 | | `j=0`: `while(entrando[0])` → F | pasa |
| 12 | | `j=0`: `numero[0]≠0` ✓ **&&** `1 <= 1` ✓ | **T1 ESPERA a T0** |
| 13 | ambos giran para siempre; ningún `numero[·]` vuelve a `0` | | **DEADLOCK** |

Ninguno entra a la sección crítica, y `numero[id] = 0` sólo se ejecuta **después** de la SC,
así que la condición nunca se puede volver falsa. **Deadlock.** ∎

Con el `j < id` del algoritmo original, en el paso 10 la guarda de `T0` sería
`numero[1] < numero[0]` (falso: `1 < 1`) `|| (numero[1]==numero[0] && 1 < 0)` (falso), o sea
`T0` **pasa**; y en el paso 12 la de `T1` sería `... || (1==1 && 0 < 1)` = **verdadero**, o
sea `T1` **espera**. El empate se rompe por `id` y exactamente uno entra. Eso es lo que hace
necesaria la condición.

## Garantía de entrada: ❌ **NO se cumple**

Directo del deadlock: en la traza de arriba hay threads que quieren entrar y no entran nunca
(slide 34).

## Mutex: ✅ **SÍ sigue valiendo**

*Argumento.* Supongamos `T_i` y `T_j` (`i ≠ j`) simultáneamente en la SC. Ambos tienen
`numero[·] ≠ 0` (se ponen en `0` recién al salir, en `h8`).

Para que `T_i` haya pasado su `for` en la iteración `j`, la guarda tuvo que ser falsa:

```
¬(numero[j] ≠ 0  ∧  numero[j] ≤ numero[i])
```

Como `numero[j] ≠ 0`, necesariamente **`numero[j] > numero[i]`**.

Simétricamente, para que `T_j` haya pasado su iteración `i`: **`numero[i] > numero[j]`**.

Las dos juntas son contradictorias. Por lo tanto no puede haber dos threads en la SC. ∎

Intuitivamente: la modificación hace la guarda **estrictamente más restrictiva** que la
original (espera en todos los casos en que el original esperaba, **y además** en el empate).
Un algoritmo que espera más nunca puede violar mutex si el original no lo hacía — lo que sí
puede es trabarse, que es exactamente lo que pasa.

> ### Observación adicional: el caso `j == id`
>
> Hay un detalle todavía más brutal en la versión modificada. El `for` recorre **todos** los
> `j` de `0` a `n−1`, **incluido `j == id`**. En ese caso la guarda evalúa
> `numero[id] != 0 && numero[id] <= numero[id]`, que es **verdadera** (el thread ya se
> asignó un número no nulo). Es decir: **el thread se espera a sí mismo, siempre**, sin
> necesidad de ningún empate ni de ningún otro thread.
>
> El algoritmo original está protegido de esto porque su guarda con `j == id` da
> `numero[id] < numero[id]` (falso) `|| (numero[id]==numero[id] && id < id)` (falso) ⟹ no
> espera.
>
> Tomé la traza principal asumiendo la lectura caritativa (que la comparación con uno mismo
> se saltea, o que el término `j != id` pretende cubrirlo), porque el punto pedagógico del
> ejercicio es el empate. Pero si se toma el código literalmente, el deadlock es todavía más
> trivial: ocurre siempre, con un solo thread.

### Resumen

| Propiedad | ¿Se cumple? |
|---|---|
| **Mutex** | ✅ SÍ |
| **Ausencia de deadlock** | ❌ NO — el empate es simétrico y ambos ceden |
| **Garantía de entrada** | ❌ NO |

---

# Ejercicio 14 — `fetch-and-add`

```
fetch-and-add(compartida, propia, x) {     // ATÓMICA
   propia = compartida
   compartida = compartida + x
}

// global ticket = 0, turno = 0
//SECCION NO CRITICA
local miturno
k1: fetch-and-add(ticket, miturno, 1)
k2: while (turno != miturno){}
k3: //SECCION CRITICA
k4: fetch-and-add(ticket, miturno, -1)
//SECCION NO CRITICA
```

## Por qué esta implementación no resuelve el problema

> **El bug es que `turno` nunca se modifica.** Ambos `fetch-and-add` operan sobre `ticket`.
> El de la salida debería incrementar **`turno`**, no decrementar `ticket`.

La consecuencia es inmediata: `turno` vale `0` desde el inicio hasta el fin del programa.
Sólo puede entrar a la sección crítica un thread cuyo `miturno` sea `0`, y ningún otro thread
que haya sacado un ticket distinto entrará **jamás**.

**Traza:**

| Thread | Acción | `ticket` | `turno` | `miturno` |
|---|---|---|---|---|
| — | inicio | 0 | 0 | — |
| T1 | `faa(ticket, miturno, 1)` | 1 | 0 | T1: **0** |
| T2 | `faa(ticket, miturno, 1)` | 2 | 0 | T2: **1** |
| T1 | `while (turno != 0)` → falso | 2 | 0 | entra a la SC |
| T2 | `while (turno != 1)` → `0 ≠ 1` ✓ | 2 | 0 | **espera** |
| T1 | `faa(ticket, miturno, -1)` | 1 | **0** | T1.miturno = 2 |
| T2 | sigue esperando | 1 | 0 | **NUNCA ENTRA** |

`turno` sigue en `0` y ya nadie con `miturno = 0` va a aparecer para "pasar el testigo".
`T2` queda bloqueado para siempre con **nadie en la sección crítica**.

### Propiedades

| Propiedad | ¿Se cumple? | Justificación |
|---|---|---|
| **Mutex** | ✅ SÍ (accidentalmente) | ver abajo |
| **Ausencia de deadlock** | ❌ NO | traza anterior: `T2` bloqueado, SC vacía |
| **Garantía de entrada** | ❌ NO | inanición permanente de todo thread con `miturno ≠ 0` |

*Sobre por qué mutex sí se cumple:* `ticket` cuenta cuántos threads pidieron y todavía no
liberaron. Un thread entra sólo si sacó `miturno = 0`, lo cual requiere que `ticket` valiera
`0` inmediatamente antes de su `fetch-and-add` — o sea, que **todos** los que pidieron ya
liberaron, y por lo tanto que nadie esté en la SC. Y mientras ese thread está adentro,
`ticket ≥ 1`, de modo que ningún otro puede sacar `0`. Nunca hay dos a la vez. ∎

Un algoritmo que garantiza mutex bloqueando a casi todo el mundo no es una solución: la
exclusión mutua exige las **tres** propiedades (slide 31).

## Modificación propuesta

```
global ticket = 0
global turno  = 0

//SECCION NO CRITICA
local miturno
local descartable
m1: fetch-and-add(ticket, miturno, 1)        // saco un número, único
m2: while (turno != miturno){}               // espero mi turno
m3: //SECCION CRITICA
m4: fetch-and-add(turno, descartable, 1)     // ← paso el testigo al siguiente
//SECCION NO CRITICA
```

Dos cambios: el `fetch-and-add` de salida opera sobre **`turno`** (no `ticket`) y suma
**`+1`** (no `−1`). La variable `descartable` está sólo porque la firma de `fetch-and-add`
obliga a recibir el valor viejo; no se usa.

Esto es exactamente el **ticket lock** clásico (el de la panadería con dispensador de números
y display de "atendiendo al número"). En x86 se implementa con `lock xadd` (slide 92).

## Argumento de correctitud

**Invariante 1 (unicidad de tickets).** *Todo thread obtiene un `miturno` distinto.*

`ticket` sólo se modifica dentro de `fetch-and-add`, que es atómica: la lectura y el
incremento no se pueden intercalar. Por lo tanto los `fetch-and-add` sobre `ticket` se
serializan en algún orden total, y el k-ésimo en ejecutarse devuelve `k−1`. Los valores
entregados son `0, 1, 2, …` **sin repeticiones y sin huecos**. ∎

*(Notar que ésta es precisamente la propiedad que el Ej. 10 no tenía: allá `PedirTurno` no
era atómica, y además el decremento reciclaba números.)*

**Invariante 2.** *`turno` = cantidad de threads que ya salieron de la sección crítica.*

`turno` arranca en `0` y se incrementa exactamente una vez por cada ejecución de `m4`, o sea
una vez por salida. ∎

### Mutex ✅

`T_a` está en la SC ⟹ pasó `m2` ⟹ `turno == miturno_a`. Si `T_b` también está en la SC,
`turno == miturno_b`. Como `turno` tiene un único valor en cada instante,
`miturno_a == miturno_b`, contradiciendo la Invariante 1. ∎

### Ausencia de deadlock ✅

Supongamos que hay threads esperando en `m2` y nadie en la SC. Sea `t` el valor actual de
`turno`. Por la Invariante 2, `t` threads ya salieron, y por la Invariante 1 usaron
exactamente los tickets `0, 1, …, t−1`.

Si hay un thread esperando, sacó un ticket `≥ t`. Como los tickets se entregan sin huecos, el
ticket `t` **fue entregado** a algún thread `T`. Ese `T` no salió (los que salieron tienen
tickets `< t`), así que o está esperando en `m2` —y su guarda `turno != t` es **falsa**, con
lo cual entra— o ya está en la SC. En ambos casos hay progreso. ∎

### Garantía de entrada ✅ (de hecho, **FIFO**)

Sea `T` con ticket `k`. `T` entra cuando `turno == k`, o sea después de exactamente `k`
salidas de la SC. Por el argumento de ausencia de deadlock, mientras `turno < k` siempre hay
un thread habilitado a entrar; por la hipótesis de que **la sección crítica siempre termina**
(slide 31) y por weak fairness, ese thread entra, sale y ejecuta `m4`, incrementando `turno`.
Como esto ocurre para cada valor `turno = 0, 1, …, k−1`, en un número finito de pasos
`turno` alcanza `k` y `T` entra. ∎

Esta es una propiedad **más fuerte** que la garantía de entrada pedida: el ticket lock atiende
en orden estricto de llegada, así que ni siquiera hay inanición relativa (nadie es "pasado"
por alguien que llegó después).

---

# Ejercicio 15 — `tomarFlag`

```
tomarFlag(mia, otro) {
   flag[mia] = !flag[otro]
}

global flag[0..1] = {false, false}

thread T0 {                        thread T1 {
   while (!flag[0])                   while (!flag[1])
      tomarFlag(0,1)                     tomarFlag(1,0)
   //SECCION CRITICA                  //SECCION CRITICA
   flag[0] = false                    flag[1] = false
}                                  }
```

**Lectura del algoritmo.** `T_i` intenta tomar el flag: se lo asigna **si el otro no lo
tiene**. Entra a la sección crítica cuando `flag[i]` quedó en `true`. Con esta estructura,
los cuatro estados posibles de `(flag[0], flag[1])` son:

| Estado | Significado |
|---|---|
| `(F,F)` | libre |
| `(T,F)` | T0 tiene el flag ⟹ T0 en la SC |
| `(F,T)` | T1 tiene el flag ⟹ T1 en la SC |
| `(T,T)` | **ambos en la SC ⟹ Mutex violado** |

O sea: **el algoritmo resuelve Mutex si y sólo si `(T,T)` es inalcanzable.**

## 15.a — Con `tomarFlag` NO atómica: **NO resuelve el problema**

`flag[mia] = !flag[otro]` es una operación compuesta: **lee** `flag[otro]`, niega, y
**escribe** `flag[mia]`. Desagregándola:

```
tomarFlag(mia, otro) {
   r1: local t = flag[otro]
   r2: flag[mia] = !t
}
```

Si ambos leen antes de que cualquiera escriba, los dos concluyen "el otro no lo tiene" y los
dos se lo quedan:

| T0 | T1 | Estado |
|---|---|---|
| `while (!flag[0])` → `!F` ✓ | | flag = (F, F); entra al loop |
| `t = flag[1]` | | T0.t = **false** |
| | `while (!flag[1])` → `!F` ✓ | entra al loop |
| | `t = flag[0]` | T1.t = **false** |
| `flag[0] = !t` | | flag = (**T**, F) |
| | `flag[1] = !t` | flag = (**T**, **T**) ← ambos |
| `while (!flag[0])` → `!T` = falso | | **T0 sale del loop** |
| `//SECCION CRITICA` | | **T0 ENTRA** |
| | `while (!flag[1])` → `!T` = falso | **T1 sale del loop** |
| | `//SECCION CRITICA` | **T1 ENTRA** |

**Mutex violado.** ∎

Es, otra vez, la misma pérdida de información de siempre: la decisión de cada thread se toma
sobre una lectura que quedó obsoleta antes de ser usada.

## 15.b — Con `tomarFlag` ATÓMICA: **sí resuelve Mutex y Ausencia de Deadlock**

### Mutex ✅

**Invariante: el estado `(T,T)` es inalcanzable.**

*Prueba por inducción sobre las transiciones.* El estado inicial es `(F,F)`. Las únicas
operaciones que modifican el array son cuatro:

| Op | Efecto |
|---|---|
| `tomarFlag(0,1)` | `flag[0] ← ¬flag[1]` (atómica) |
| `tomarFlag(1,0)` | `flag[1] ← ¬flag[0]` (atómica) |
| `flag[0] = false` | salida de T0 de la SC |
| `flag[1] = false` | salida de T1 de la SC |

Analizo las transiciones desde cada estado alcanzable:

**Desde `(F,F)`:**
- `tomarFlag(0,1)`: `flag[0] ← ¬F = T` ⟹ `(T,F)` ✓
- `tomarFlag(1,0)`: `flag[1] ← ¬F = T` ⟹ `(F,T)` ✓

**Desde `(T,F)`:**
- `tomarFlag(0,1)`: `flag[0] ← ¬F = T` ⟹ `(T,F)` (sin cambio)
- `tomarFlag(1,0)`: `flag[1] ← ¬T = **F**` ⟹ `(T,F)` — **T1 no logra tomar el flag** ✓
- `flag[0] = false` ⟹ `(F,F)`

**Desde `(F,T)`:** simétrico al anterior.

Ninguna transición conduce a `(T,T)`. ∎

**El corazón del argumento:** cuando el otro tiene el flag, `¬flag[otro]` vale `false`, así
que el thread se **auto-asigna `false`** y sigue girando en su `while`. La atomicidad es lo
que garantiza que la lectura de `flag[otro]` y la escritura de `flag[mia]` no se puedan
intercalar — exactamente la propiedad que faltaba en el inciso a.

Notar que la operación es esencialmente un **test-and-set condicional** hecho con un solo
read-modify-write, que es la primitiva de hardware de la slide 90.

### Ausencia de deadlock ✅

*Argumento.* Supongamos que ambos threads están girando en su `while` sin entrar. `T0` gira
sólo si `flag[0] == false`, y `T1` sólo si `flag[1] == false`; por lo tanto el estado es
`(F,F)`.

Por weak fairness, alguno de los dos ejecuta su `tomarFlag`. Desde `(F,F)`, quien lo ejecute
obtiene `¬false = true` y **se queda con el flag**, con lo cual sale del loop y entra a la
sección crítica. Hay progreso. ∎

No hay livelock tampoco: desde `(F,F)`, **cualquier** operación que se ejecute le da el flag
a alguien. No existe el "los dos ceden a la vez" del Ejercicio 13, porque `tomarFlag` no es
simétrica en su efecto: el primero en ejecutarla gana.

### Garantía de entrada ⚠️ — depende de la definición

Acá conviene ser preciso, porque el enunciado afirma que el algoritmo **es** una solución:

- **Si "garantía de entrada" se entiende como progreso** (si nadie está en la SC y hay
  threads queriendo entrar, alguno entra): ✅ **se cumple**, es el argumento de arriba.

- **Si se entiende como ausencia de inanición individual** (todo thread que quiere entrar,
  eventualmente entra): ❌ **no se cumple**. Nada impide que `T0` monopolice el recurso:
  entra, sale (`(F,F)`), y vuelve a tomar el flag antes de que `T1` alcance a ejecutar su
  `tomarFlag`. Cada vez que `T1` lo intenta, encuentra `flag[0] == true` y se auto-asigna
  `false`.

  Esa ejecución es **weakly fair**: `T1` ejecuta infinitas veces, sólo que siempre falla.
  Weak fairness garantiza que un thread *ejecute*, no que *tenga éxito*.

  El algoritmo no tiene ningún mecanismo de turno o antigüedad (a diferencia del bakery o
  del ticket lock del Ej. 14), así que no puede garantizar equidad.

### Resumen

| Propiedad | Sin atomicidad | Con atomicidad |
|---|---|---|
| **Mutex** | ❌ NO (traza del inciso a) | ✅ SÍ (`(T,T)` inalcanzable) |
| **Ausencia de deadlock** | — | ✅ SÍ |
| **Garantía de entrada** (progreso) | — | ✅ SÍ |
| **Ausencia de inanición** (individual) | — | ❌ NO |

---

# Apéndice: patrones que se repiten en toda la guía

Después de resolver los 15, hay tres esquemas que aparecen una y otra vez y conviene tenerlos
como reflejo:

### 1. Casi todas las fallas de Mutex son la misma falla

`np = nq + 1` (Ej. 9), `PedirTurno` (Ej. 10), `numero[id] = 1 + max(...)` (Ej. 13),
`tomarFlag` (Ej. 15), `n = n + 1` (Ej. 2): **leer una variable compartida, calcular, y
escribir**. Si el cambio de contexto cae entre la lectura y la escritura, la decisión se toma
sobre información obsoleta. Es la pérdida de sumas de la slide 26, disfrazada de distintas
maneras.

**Reflejo para el parcial:** si te piden refutar Mutex y no encontrás la traza, preguntate
*"¿qué estoy asumiendo atómico que en realidad no lo es?"* y desagregá esa operación.

### 2. Refutar cuesta una traza; afirmar cuesta un invariante

Slide 38. En esta guía:

- **Refutaciones** (Ej. 9, 10, 11, 12, 13, 15a): siempre una tabla de traza concreta.
- **Afirmaciones** (Ej. 5c, 12a-mutex, 13-mutex, 14, 15b): siempre un invariante más un
  argumento de que ninguna transición lo rompe.

Las afirmaciones más limpias de la guía tienen todas la misma forma: *"supongamos que ambos
están en la SC; entonces valen A y B; pero A ∧ B es contradictorio"*.

### 3. El argumento de ciclo de Dekker aparece dos veces

El razonamiento del slide 66 —encadenar precedencias hasta cerrar un ciclo imposible— se usa
tal cual en el **Ej. 12** (mutex de `algunVerdadero`) y está implícito en el **Ej. 13**. Vale
la pena tenerlo memorizado como plantilla:

```
W_i ≺ R_ij        (orden de programa: primero levanto mi bandera, después miro)
R_ij ≺ W_j        (leí false, así que fue antes de que él la levantara)
W_j ≺ R_ji        (orden de programa del otro)
R_ji ≺ W_i        (él leyó false)
────────────────────────────────
W_i ≺ W_i         contradicción
```

Y — el punto de las últimas 40 slides de la clase 1 — **este argumento asume Sequential
Consistency**. En hardware real (x86-TSO), el store buffer permite exactamente el
reordenamiento `store → load` que rompe la cadena, y por eso `DekkerLitmus.java` detecta
violaciones. En el modelo de la Práctica 1 el argumento vale; en Java de verdad hace falta
`volatile`.

---

*Documento generado por Claude (Anthropic) — ver aviso de autoría al inicio.*