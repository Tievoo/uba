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

## Ejercicio 6

### a)
Delay por segmentos es de 25.6 microsegundos
STP ya convergió
El router divide dominios de STP (?)

a. para que la distnacia entre el host A y host b sea minima, deberíamos idealmente tomar un camino tal que
Host A va al hub, vía X al switch 1, switch 2, router1, switch 1(bis), switch3(bis).

En ese caso, hay dos redes, a lo que se le pone id entiendo que es a los switches. no se si a los hubs?
sale a ojo.

### b)
eh
2?

### c)
Feo. significa que R1.S3.2 y .1 deja de estár bloqueado y pasa a ser RP/ DP respectivamente. 

### d)
*(armado con Claude)*

Las "tablas de forwarding" de capa 2 son las del **learning bridge** de cada switch: `MAC → puerto`. El hub (capa 1) no tiene tabla y el router (capa 3) no entra. Como las MACs no son dato, uso nombres simbólicos: `MAC_A` (host A), `MAC_R1` (interfaz del router del lado red 1), `MAC_R2` (interfaz del router del lado red 2), `MAC_B` (host B).

**Supuestos** (topología del a):
- Red 1: S0 = root (el del hub), S1 = el del router, S2 = M, S3 = A. S3 empata entre Z y el hub → desempato por menor puerto: **S3.0 (Z) = RP**, S3.1 (hub) y S3.2 (hacia S2) **bloqueados**.
- Red 2: S0 = root (pegado a B), S1 = pegado al router, S2 = el de arriba con **S2.0 bloqueado**.
- Cachés ARP ya cargadas (sólo viaja el paquete IP). Un switch aprende la MAC **origen** por el puerto de **entrada**; un puerto bloqueado descarta todo (no aprende ni reenvía).

**Idea clave:** B está en otra red, así que A no le manda el frame a B sino a su gateway. En la red 1 viaja `MAC_A → MAC_R1`; el router arma un frame nuevo y en la red 2 viaja `MAC_R2 → MAC_B`. Por eso en la red 1 nunca aparece `MAC_B` y en la red 2 nunca aparece `MAC_A`.

#### Red 1 — frame `MAC_A → MAC_R1`

1. A → hub → el hub repite: llega a **S0** por su puerto 2 (X) y a **S3.1** (bloqueado → descarta).
2. S0 aprende `MAC_A → 2`. No conoce `MAC_R1` → **flood** por 0, 1 y 3.
3. Por el 0 → **S1** aprende `MAC_A → 0`, flood por su puerto 1 → llega al router.
4. Por el 1 → **S2** aprende `MAC_A → 0`, flood por su 1 → llega a S3.2 (bloqueado → descarta).
5. Por el 3 (Z) → **S3** entra por S3.0 (RP), aprende `MAC_A → 0`; sus otros puertos están bloqueados → no reenvía.

| Switch | MAC | Puerto |
|---|---|---|
| S0 (root) | MAC_A | 2 |
| S1 (router) | MAC_A | 0 |
| S2 (M) | MAC_A | 0 |
| S3 (A) | MAC_A | 0 |

#### Red 2 — frame `MAC_R2 → MAC_B`

1. Router → **S1** aprende `MAC_R2 → 0`. No conoce `MAC_B` → flood por 1 y 2.
2. Por el 1 → **S0** aprende `MAC_R2 → 0`, flood por 1 (llega a **B**) y por 2.
3. Por el 2 de S0 → **S2** entra por su 1, aprende `MAC_R2 → 1`; su 0 está bloqueado → no reenvía.
4. Por el 2 de S1 → llega a S2.0 (bloqueado → descarta).

| Switch | MAC | Puerto |
|---|---|---|
| S0 (root, pegado a B) | MAC_R2 | 0 |
| S1 (pegado al router) | MAC_R2 | 0 |
| S2 (arriba) | MAC_R2 | 1 |

En cada tabla hay una sola MAC porque los switches aprenden sólo MACs de **origen**; los destinos (`MAC_R1`, `MAC_B`) no se aprenden.

#### Si "el intercambio" incluye la respuesta (B → A)

- **Red 2**, frame `MAC_B → MAC_R2`: S0 aprende `MAC_B → 1` y ya conoce `MAC_R2` → lo manda sólo por el 0; S1 aprende `MAC_B → 1`. S2 no se entera (no hubo flood).
- **Red 1**, frame `MAC_R1 → MAC_A`: S1 aprende `MAC_R1 → 1` y lo manda por el 0; S0 aprende `MAC_R1 → 0` y lo manda por el 2 (al hub). S2 y S3 no se enteran.

## Ejercicio 7

### a)
Como referencia, digamos que los ids son, desde arriba de todo y en orden horario, del 1 al 5. es decir, la punta de arriba es 1, y el directo a su izquierda es 5.
al puerto de cada bridge x que lleva a un bridge y lo llamo PX-Y
vease, el puerto de 1 que lleva a 4, lo llamo P1-4. en simultaneo, el puerto de 4 que lleva a 1, por el mismo enlace, se llama P4-1.

Tras ejecutar STP, es bastante obvio el resultado.
todos los puertos de 1 son DP
todos los puertos de 2 son DP, menos el RP
todos los puertos de 3 son DP, menos el RP, y el puerto a 2, que bloquea
todos los puertos de 4 son DP, menos el RP, y el puerto a 2 y 3, que bloquea
todos los puertos de 5 son DP, excepto que ninguno es DP, porque es el menor id. solo le queda el rp.
se entiende el patroncito.

### b)

sí, pq si la tabla está vacía hace flooding para llenarla, entonces ni bien Host A de la red 2-3 quiera mandarle algo a Host B, va a hacer flooding la red a ambos switches.


## Ejercicio 8

6 redes lan, con 4 switches
buscamos minimizar delay entre cliente y servidor. uso interno

### a)
Inicialmente, veamos como funciona el stp en esta red. con el switch de ID 4, lo que pasa es que va a tener su puerto 0 (el mismo que conecta con los clientes) blocked, por que el camino al root es mejor por 2, y el id 3 es dueño del segmento, entonces es dueño del puerto. dicho eso, el camino que tiene algguien de la lan D para llegar a la lan F, es vía ID 3-> 1 -> 2 -> 4 -> F. lo cual es HIPER suboptimo.

Entonces, que cambiamos? tenemos dos situaciones

b. Solo se pueden manipular los cables entre LANS y Switches. Lo que haría, calculo, es borrar la conexión entre el switch de ID 4, con el switch de ID 2. De esta manera, el puerto 0 del ID 4 no se bloquea, entonces tiene conexión directa con la LAN D. y con esto mismo, el intercambio entre LAN D y LAN F es directo, a traves del switch 4.

c. Si solo se pueden reconfigurar los switches a nivel lógico, sin cambiar el root, cambiaria el id del switch 2 con el switch 3, (o hacer que el id 4 sea 2, no importa mucho creo). de tal manera de que el pueto 0 del id 4 no se bloquee. si cambiamos el id 2 por el id 3, el peurto bloqueado es el 1. no sabemos que hay en la LAN b, pero no nos importa tampoco que llegue un poco más lento. en el b. directamente les cortamos la conexión y no nos jodió mucho. 


## Ejercicio 9

*(resuelto por Claude)*

Topología (figura): **Switch0** en el centro, con PC0 y PC1 conectadas directo y tres uplinks a **Switch1** (PC2, PC3, PC4), **Switch2** (PC5, PC6, PC7) y **Switch3** (PC9, PC10, PC11). Todos los enlaces son punto a punto switch–switch o switch–host.

### a.1) ¿Puede quedar algún puerto CLOSED (bloqueado) tras correr STP?

**No.** STP sólo bloquea puertos para **romper ciclos**, y esta topología es un **árbol** (Switch0 en el centro y los otros tres colgando, sin enlaces redundantes): no hay ningún ciclo que cortar.

Corriendo STP (el root es el de menor ID, cualquiera sea), cada switch no-root tiene un único camino al root → ese puerto es su **RP**, y todos los demás puertos (hacia hosts o hacia switches "de abajo") son **DP** porque son el único switch en ese segmento o el más cercano al root. Todos los puertos quedan en forwarding.

### a.2) ARPs de PC0 y PC1 hacia PC5, y después una trama PC9 → PC1

**Lo que aprenden los switches con los ARP** (tablas inicialmente vacías; un switch aprende la MAC **origen** por el puerto de **entrada**):

1. **ARP request de PC0** (broadcast `FF:FF:FF:FF:FF:FF`): se floodea por toda la red. **Todos los switches aprenden PC0**: Switch0 por el puerto de PC0; Switch1, Switch2 y Switch3 por su uplink a Switch0.
2. **ARP reply de PC5 → PC0** (unicast): Switch2 aprende PC5 (puerto de PC5) y ya conoce PC0 → lo manda sólo por el uplink. Switch0 aprende PC5 (puerto hacia Switch2) y lo manda sólo a PC0. Switch1 y Switch3 no lo ven.
3. **ARP request de PC1** (broadcast): igual que el 1 → **todos aprenden PC1**.
4. **ARP reply de PC5 → PC1**: igual que el 2; no aprenden nada nuevo (PC5 ya estaba).

| Switch | Conoce |
|---|---|
| Switch0 | PC0 (su puerto), PC1 (su puerto), PC5 (→ Switch2) |
| Switch1 | PC0, PC1 (→ uplink) |
| Switch2 | PC0, PC1 (→ uplink), PC5 (su puerto) |
| Switch3 | PC0, PC1 (→ uplink) |

**Trama origen PC9, destino PC1** (unicast):

1. **PC9 → Switch3**: Switch3 aprende PC9. **Ya conoce PC1** (lo aprendió del broadcast ARP de PC1) → la reenvía **sólo por el uplink**.
2. **Switch3 → Switch0**: Switch0 aprende PC9 (puerto hacia Switch3). Conoce PC1 → la manda **sólo por el puerto de PC1**.
3. **Switch0 → PC1**.

➡️ La trama pasa **sólo por 3 enlaces**: `PC9–Switch3`, `Switch3–Switch0`, `Switch0–PC1`. **No hay flooding**, porque gracias al broadcast del ARP de PC1 todos los switches ya sabían dónde está PC1. Ningún otro host ni switch ve la trama.

(Si PC1 no hubiese mandado su ARP, Switch3 no conocería PC1 y floodearía; ese es el punto del ejercicio: el ARP broadcast "enseña" la MAC del que pregunta a toda la red.)

### b) Un sniffer ve 5 RTTs seguidos el comienzo de la misma trama y una colisión. ¿Posible? ¿Esperable?

**En esta red, no es esperable.** Todos los enlaces son punto a punto con switches (un solo equipo por puerto): cada puerto es su propio dominio de colisión. **Suponiendo full-duplex** (el enunciado no lo dice, pero es lo habitual en switches con un equipo por puerto, que lo autonegocian), no hay CSMA/CD ni colisiones. Si algún enlace fuera half-duplex, una colisión sólo podría darse entre las dos puntas de ese cable y quedaría confinada ahí. Además, un sniffer en una red switcheada sólo ve el tráfico de su propio puerto.

**Aun en un medio compartido (half-duplex / hub) sería muy improbable**, por el **backoff exponencial**: tras la k-ésima colisión cada estación espera un número aleatorio de slots en $[0, 2^k - 1]$ (slot = RTT = 2τ). Para ver la misma trama arrancar **en cada RTT seguido**, las estaciones tendrían que elegir **siempre el slot 0** y volver a chocar:

$$P = \frac{1}{2}\cdot\frac{1}{4}\cdot\frac{1}{8}\cdot\frac{1}{16}\cdot\frac{1}{32} = \frac{1}{2^{15}} \approx 3\cdot10^{-5}$$

Es **posible** (probabilidad no nula) pero **no esperable**: el backoff está diseñado justamente para que las retransmisiones se vayan espaciando cada vez más. Si se ve algo así, lo más probable es una falla: una placa que no respeta el backoff, un enlace en half-duplex con *duplex mismatch*, o un equipo que genera ruido/jam constantemente.
