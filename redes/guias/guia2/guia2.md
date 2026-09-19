# Guía 2 — Medios Compartidos

*Redes de Comunicaciones y Cómputo Distribuido — FCEN, UBA*

hecha por Claude (Opus). Bruno la había hecho mentalmente; acá la dejo escrita. Ojo: los ejercicios que dependen 100% de figuras del PDF que no se leen bien por OCR (4, 5 y el 6 con el router) los resolví dejando explícita la topología que asumí — si no coincide con el dibujo, el método es el mismo, cambiás los datos y listo.

> **Recordatorios que uso todo el tiempo:**
> - **CSMA/CD**: sensás el medio; si está libre transmitís; para detectar colisión tenés que estar transmitiendo. Peor caso de detección = **2τ** (τ = delay de propagación de punta a punta).
> - **Frame Ethernet 802.3**: `Preamble(64) | Dest(48) | Src(48) | Type/Length(16) | Body(≥46B) | CRC(32)`. Mínimo (sin preámbulo) = **512 bits = 64 B**.
> - **Learning bridge**: aprende el puerto de la MAC **origen**; si no conoce el destino → **flood** (a todos menos por donde vino); broadcast → siempre flood.
> - **STP**: BPDU = `(rootID, distancia, switchID)`. **Mejor** = menor rootID → menor distancia → menor switchID. **Root Port (RP)**: el puerto por donde se ve el mejor BPDU al root. **Designated Port (DP)**: el puerto que ofrece el mejor BPDU en ese segmento. **Closed/Blocked**: el resto. El root tiene *todos* sus puertos DP.

---

## Ejercicio 1 — LAN 802.3 (CSMA/CD)

Datos: H2 y H3 comparten un segmento de 500 m; H4 está a 2500 m de H1 pasando por 4 hubs; **delay máximo = 25,6 µs** (es el τ de propagación de punta a punta, peor caso H1↔H4). Ethernet clásica → **Vtx = 10 Mbps**.

### a) Período mínimo para asegurarse de que no hubo colisión

Por CSMA/CD, para **garantizar** que detectás cualquier colisión tenés que seguir transmitiendo durante todo el tiempo de ida y vuelta de peor caso:

$$t_{min} = 2\tau = 2 \cdot 25{,}6\ \mu s = \mathbf{51{,}2\ \mu s}$$

(Peor caso: H1 empieza a transmitir; justo antes de que la señal llegue a H4, H4 sensa libre y transmite → colisión; esa colisión tarda otro τ en volver hasta H1. Total 2τ.)

### b) Tamaño mínimo del frame

Tengo que estar transmitiendo al menos 51,2 µs, así que el frame no puede ser más corto que lo que se transmite en ese tiempo:

$$|Frame|_{min} = V_{tx} \cdot 2\tau = 10 \cdot 10^6 \cdot 51{,}2 \cdot 10^{-6} = \mathbf{512\ bits = 64\ bytes}$$

(Que es justo el mínimo de la norma: 6 dest + 6 src + 2 type + 46 datos + 4 CRC = 64 B.)

### c) ¿Y si quiero mandar menos datos que el mínimo?

Se rellena con **padding** hasta llegar a los 46 B de datos (64 B de frame). En el receptor se descarta el relleno: en 802.3 el campo **Length** dice cuántos bytes de datos reales hay, así que se leen esos y el resto (padding) se tira.

### d) H2 y H3 reciben datos en t₀+5ms y t₀+7ms (H1 transmite desde t₀ por 10 ms)

Ambos sensan el medio y lo encuentran **ocupado** (H1 está transmitiendo hasta ~t₀+10ms). Con CSMA **1-persistente**, esperan a que el medio se libere y transmiten apenas se libera. Como los dos van a encontrar el medio libre casi al mismo tiempo (la diferencia es sólo la propagación entre ellos y H1), **sus tramas colisionan**. Ahí entra CSMA/CD: jam sequence, backoff exponencial y retransmiten.

### e) H4 recibe datos en t₀+2µs

H1 empezó en t₀, pero su señal tarda hasta 25,6 µs en llegar a H4. En t₀+2µs la señal de H1 **todavía no llegó** a H4, así que H4 sensa el medio **libre**, transmite… y su trama **colisiona** con la de H1. Es el caso clásico de CSMA/CD: por el delay de propagación, H4 no puede "ver" la transmisión en curso de H1.

---

## Ejercicio 2 — Learning Bridge

Topología: `X —[B1]— [B2]— [B3]`, con Y colgando de B2 (abajo), Z de B3 (arriba) y W de B3 (abajo). Tablas inicialmente vacías. Uso direcciones **izq / der / arr / ab** para los puertos de cada bridge.

### • X transmite a W

Todas las tablas vacías → cada bridge que recibe la trama la **floodea**. La trama de X pasa por B1, B2 y B3.
- **Aprenden dónde está X:** B1, B2 y B3 (todos, X en su puerto izquierdo).
- **¿Y ve la trama?** **Sí** — como B2 floodea, la trama sale también hacia Y.

| | X |
|---|---|
| B1 | izq |
| B2 | izq |
| B3 | izq |

### • Z transmite a X

La trama llega a B3, que **ya sabe** dónde está X (izq) → no floodea, la manda sólo hacia B2. B2 sabe X (izq) → la manda sólo a B1. B1 sabe X (izq) → la entrega a X.
- **Aprenden dónde está Z:** B3 (arr), B2 (der), B1 (der).
- **¿Y ve la trama?** **No** — B2 ya sabía dónde está X, así que no floodea (no manda hacia Y).

| | X | Z |
|---|---|---|
| B1 | izq | der |
| B2 | izq | der |
| B3 | izq | arr |

### • Y transmite a X

La trama llega a B2, que sabe X (izq) → la manda sólo a B1. B1 la entrega a X.
- **Aprenden dónde está Y:** B2 (ab), B1 (der).
- **¿Z ve la trama?** **No** — B2 sabe dónde está X y no floodea (no va hacia B3).

| | X | Y | Z |
|---|---|---|---|
| B1 | izq | der | der |
| B2 | izq | ab | der |
| B3 | izq | — | arr |

### • W transmite a Y

La trama llega a B3, que **no sabe** dónde está Y → aprende W (ab) y **floodea**. Sale hacia B2 y hacia Z. B2 sabe dónde está Y (ab) → la manda sólo a Y, y aprende W (der).
- **Aprenden dónde está W:** B3 (ab), B2 (der).
- **¿Z ve la trama?** **Sí** — B3 no sabía dónde está Y, así que floodeó.

Tabla final:

| | X | W | Y | Z |
|---|---|---|---|---|
| B1 | izq | — | der | der |
| B2 | izq | der | ab | der |
| B3 | izq | ab | — | arr |

---

## Ejercicio 3 — STP

Topología (segmentos LAN L1–L4, switches S1–S3):
- **L1** = {S1, S2}
- **L2** = {S1, S3}
- **L3** = {S2, S3}
- **L4** = {S3} (stub)

Asumo **SwitchIDs = S1 < S2 < S3** (1, 2, 3). Costo 1 por segmento.

### a) Simulación

**Root = S1** (menor ID). BPDU del root: `(1, 0, S1)`.

Segmento por segmento (gana el mejor BPDU = designado):
- **L1 {S1,S2}**: S1 manda (1,0,1) → designado S1. S2 aprende costo 1 por acá.
- **L2 {S1,S3}**: S1 manda (1,0,1) → designado S1. S3 aprende costo 1 por acá.
- **L3 {S2,S3}**: S2 tiene costo 1 (por L1) → manda (1,1,2). S3 tiene costo 1 (por L2) → manda (1,1,3). Gana **S2** (mismo root y distancia, menor ID). Designado en L3 = S2.
- **L4 {S3}**: designado S3 (stub).

Estados de puertos:

| Switch | Puerto | Estado | Motivo |
|---|---|---|---|
| **S1** (root) | →L1 | DP | root: todo DP |
| | →L2 | DP | |
| **S2** | →L1 | **RP** | mejor camino al root (costo 1) |
| | →L3 | DP | ganó el segmento L3 (1,1,2) |
| **S3** | →L2 | **RP** | mejor camino al root (costo 1) |
| | →L3 | **BLOCKED** | no es RP y perdió L3 contra S2 |
| | →L4 | DP | stub |

**Root = S1. Puerto bloqueado = S3 → L3.** (Eso rompe el ciclo S1–L1–S2–L3–S3–L2–S1.)

### b) Se rompe el cable de S2 a L1. Recalcular

Ahora S2 sólo toca L3. Su único camino al root es L3 → S3 → L2 → S1 (costo 2).
- Root sigue siendo **S1**.
- **L3 {S2,S3}**: S3 manda (1,1,3), S2 manda (1,2,2). Gana **S3** (distancia 1 < 2). Designado L3 = S3 → S3 pasa a **DP** en L3.
- S2: su único puerto (→L3) es **RP** (costo 2).

**¿Qué sucede?** El puerto que estaba bloqueado (**S3→L3**) pasa a **Designated (se activa)**, y el RP de S2 se mueve de L1 (que ya no existe) a L3. Al desaparecer el enlace S2–L1 se rompió el ciclo, así que **ya no queda ningún puerto bloqueado** (la topología quedó como un árbol). S2 ahora llega al root con distancia 2, dando la vuelta por S3.

---

## Ejercicio 4 — STP con switches 1001–1006

> ⚠️ **Bruno, ojo:** la figura de este ejercicio no la pude leer bien del PDF (los puertos y enlaces entre 1001–1006 salen borrosos por OCR). Dejo el **método completo** para que lo apliques sobre el dibujo real. Los pasos son mecánicos.

**Procedimiento STP (para a):**
1. **Elegir root** = switch con menor SwitchID (acá 1001). Sus puertos son todos **DP**.
2. **Root Port de cada switch**: el puerto por el que recibe el mejor BPDU hacia el root (menor costo; empata → menor SwitchID del emisor; empata → menor puerto).
3. **Designated Port por segmento**: en cada segmento, el switch que ofrece el mejor BPDU `(rootID, distancia, switchID)` es el designado; ese puerto es DP.
4. **Blocked**: todo puerto que no sea ni RP ni DP.

**b) Tablas de forwarding aprendidas** (learning bridge): una vez convergido STP, se aprende el puerto de la MAC **origen** de cada trama; si el destino es desconocido, se floodea por los puertos en estado forwarding (RP/DP), nunca por los blocked.

**c) Puerto 2 de 1001 en Disabled**: se recalcula STP sin ese enlace (puede cambiar el árbol / mover RPs / desbloquear algún puerto) y se re-aprenden las tablas desde cero.

**d) Conectar 1001↔1004 (puertos libres 3 y 4) por CSMA/CD**: se agrega un enlace nuevo → puede aparecer un ciclo nuevo → STP recalcula y bloqueará un puerto para volver a dejar un árbol.

*(Si me pasás la topología exacta con los enlaces/puertos, te lleno las tablas concretas en 2 minutos.)*

---

## Ejercicio 5 — Config de SwitchIDs a partir de una tabla

Se sabe que el switch **X** (con puertos 0, 1, 2) aprendió: **H1 → interfaz 0**, **H2 → interfaz 2**.

**Idea clave:** un learning bridge aprende el puerto por el que le **llega** la trama con esa MAC de origen. Que X tenga `H1→0` y `H2→2` significa que, en la topología **ya convergida por STP**, el camino activo desde H1 hasta X **entra por el puerto 0**, y desde H2 **entra por el puerto 2**. Por lo tanto, los puertos **0 y 2 de X quedan en forwarding** (RP o DP) y el enlace redundante (el que STP bloquea para romper el ciclo) queda del lado del **puerto 1** (o bloqueado en el switch del otro extremo de ese enlace).

**a) Una config de SwitchIDs posible:**

Tenés que elegir los IDs de modo que:
- El **Root Port de X** caiga sobre el puerto que va hacia H2 (puerto **2**) → esto se logra haciendo que el **root** (o el mejor camino al root) esté del lado del puerto 2.
- El puerto **0** (hacia H1) quede como **Designated** (X es el designado del segmento que lleva a H1).
- El enlace redundante quede **bloqueado del lado del puerto 1** (X no es designado ahí y no es su RP) → para eso, el switch del otro extremo del puerto 1 debe ofrecer un BPDU mejor que X en ese segmento (menor ID / menor distancia), así **X bloquea el 1**.

> ⚠️ Como no tengo la numeración exacta de todos los switches del cuadrado de la figura, no puedo dar los IDs "definitivos", pero una asignación válida es: **root = el switch vecino de X por el puerto 2** (ID más chico, ej. 1), luego el switch del lado de H1 con ID intermedio, y el switch del otro extremo del **puerto 1 de X con ID menor que X** (para que gane ese segmento y X lo bloquee). Con eso: X → RP=2, DP=0, BLOCKED=1, que reproduce la tabla `H1→0, H2→2`.

---