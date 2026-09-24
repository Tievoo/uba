## Ejercicio 1

**¿Qué es un puerto?**

Un puerto es un identificador numérico de 16 bits que el nivel de transporte usa para identificar el extremo (*endpoint*) de un proceso dentro de un host. Funciona como un "canal" en el que un proceso puede escuchar para recibir los mensajes que están destinados a él a nivel aplicativo.

Ejemplo: si tengo Slack y Discord abiertos, cada segmento que llega al host tiene que poder entregarse al proceso correcto —un DM de Discord no lo puede leer Slack, y viceversa. Para eso el header del segmento (TCP o UDP) lleva **puerto origen** y **puerto destino**, y con eso el receptor sabe a qué proceso entregar los datos.

> Nota: una app *cliente* como Slack/Discord en realidad abre conexiones salientes usando un puerto origen efímero; el que "escucha" en un puerto fijo es el *servidor*. En TCP, cada conexión se identifica por la **4-tupla** `IPorig:Porig ↔ IPdest:Pdest`, no solo por el puerto destino.

**¿Qué relación guarda con la multiplexación?**

El puerto es la pieza que hace posible la (de)multiplexación del nivel de transporte:
- **Multiplexación** (emisor): junta los datos de varios sockets/procesos y les agrega el header de transporte con los puertos.
- **Demultiplexación** (receptor): usa el puerto destino (en TCP, la 4-tupla) para entregar cada segmento al socket/proceso correcto.

**¿Qué sucedería si el nivel de transporte no implementara este concepto?**

No se podría saber a qué proceso pertenece cada segmento. El host recibe la trama, sí, pero no habría forma de decidir a quién entregársela: en la práctica solo podría correr una aplicación de red a la vez, o haría falta otro mecanismo que cumpla la misma función.

**¿Qué diferencias hay entre UDP y TCP (con respecto a los servicios que ofrecen)?**

| | TCP | UDP |
|---|---|---|
| Conexión | Orientado a conexión (3-way handshake p/ setup, 4-way p/ release) | Sin conexión |
| Confiabilidad | Confiable: ACKs, checksum y retransmisión por *timeout* | No confiable (*best-effort*) |
| Orden | Entrega en orden; reordena con números de secuencia | Sin garantía de orden |
| Control de flujo | Sí (ventana deslizante; evita inundar al receptor) | No |
| Control de congestión | Sí (evita sobrecargar la red) | No |
| Modelo de datos | Flujo de bytes (*stream*) | Datagramas (mensajes discretos) |

Ambos comparten la **multiplexación por puertos** (16 bits). TCP además identifica cada conexión con la 4-tupla `(IPorig, Porig, IPdest, Pdest)`.

**¿En qué escenarios es preferible cada uno?**

- **TCP**: cuando importa que llegue *todo y en orden* y se justifica el costo de retransmitir / mantener estado. Ejemplos típicos: transferencia de archivos, web, mail.
- **UDP**: cuando importa más la *latencia* y una pérdida ocasional es tolerable, o cuando la confiabilidad se resuelve a nivel aplicación. La teórica da el ejemplo de **UDP + RTP** para tráfico *real-time* (streaming / voz). Otros casos típicos: DNS, juegos online.


## Ejercicio 2

El enunciado marca que tanto en enlace como en transporte se busca comunicación **confiable** (que llegue todo, sin errores y en orden), que se usan estrategias parecidas, pero que en transporte ciertos parámetros cambian dinámicamente y en enlace no.

**a. Estrategias que comparten ambos niveles**

Como el objetivo es el mismo, usan la misma caja de herramientas:
- **Números de secuencia**: para ordenar y detectar pérdidas o duplicados.
- **ACKs (confirmaciones)**: el receptor avisa qué recibió correctamente.
- **Detección de errores**: checksum / CRC sobre los datos.
- **Retransmisión ante pérdida (ARQ)**: si no llega el ACK dentro de un tiempo → se reenvía (*timeout*).
- **Ventana deslizante (*sliding window*)**: permite tener varios paquetes "en vuelo" sin esperar de a uno, y a la vez hacer control de flujo (que el emisor no inunde al receptor).

**b. Diferencias entre ambos niveles (¿a qué se deben?)**

La diferencia de fondo es **el alcance de la comunicación**:
- En **enlace**, los dos extremos están **directamente conectados** por un único medio físico (un salto, punto a punto), con características fijas.
- En **transporte**, los dos extremos son procesos separados por **toda la red** (muchos saltos, ruteo variable, routers con colas, medio compartido con otros flujos).

De ahí salen las diferencias (la teórica las lista en la p.9, *"Enlace de Datos versus Transporte"*):

| El transporte... | ...por eso necesita |
|---|---|
| conecta muchas máquinas distintas | establecimiento y liberación **explícitos** de conexión (handshakes) + multiplexación por puertos |
| tiene **RTT muy variable** (colas, rutas, congestión) | **timeouts adaptativos** (RTT estimado) ← el "parámetro dinámico" del enunciado |
| sufre retardos largos | prepararse para el arribo de **paquetes muy viejos** (duplicados / desordenados) → espacio de secuencia grande |
| enfrenta receptores de distinta capacidad | **control de flujo** con ventana anunciada dinámica |
| enfrenta distinta capacidad de red | **control de congestión** (ventana que varía dinámicamente) |

En cambio, en enlace el medio es fijo: el RTT es prácticamente constante (un timeout fijo alcanza), los datos llegan en orden (un solo camino) y no hay "congestión de red" que administrar. Por eso los parámetros del enlace pueden ser estáticos y los del transporte no.

## Ejercicio 3

Contexto: un protocolo de **red** orientado a conexión mediante **circuitos virtuales** (todos los paquetes de una conexión siguen el mismo camino preestablecido), que **garantiza la entrega en orden** pero **no hace control de errores** (puede perder o corromper paquetes; los que llegan, llegan en orden).
> El concepto de circuito virtual es de Nivel de Red — ver teórica de IP, slide *"Datagrama vs. Circuito Virtual"*.

**a. ¿Podrían dividirse los paquetes de una conexión de transporte por varios caminos?**

**No.** Por definición de circuito virtual, se establece un único camino al abrir la conexión y todos los paquetes van por ahí. Justamente por eso la red puede garantizar el orden (un solo camino = FIFO). Repartir los paquetes por varios caminos rompería esa garantía y contradiría el modelo de CV.

**b. Si las conexiones de red son simplex, ¿podrían establecerse conexiones de transporte full-duplex?**

**Sí.** Un canal full-duplex se compone con dos canales simplex, uno en cada sentido. El transporte abre dos circuitos virtuales simplex (A→B y B→A) y le presenta a la aplicación una única conexión full-duplex. Es el mismo principio por el que TCP es full-duplex: son "dos flujos de bytes" independientes.

**c. ¿Sería necesario usar números de secuencia en los paquetes de transporte?**

**Sí**, pero no para lo que uno pensaría:
- **Para ordenar: no** hacen falta, porque la red ya garantiza la entrega en orden.
- **Para detectar pérdidas y retransmitir: sí.** Como la red no controla errores, puede perder paquetes. Si el receptor recibe `1, 2, 4, 5`, sin números de secuencia no tiene forma de darse cuenta de que falta el `3`. Los números de secuencia permiten detectar el hueco y saber qué retransmitir / qué confirmar.

*Observación*: como la red entrega en orden y no deja "paquetes viejos" dando vueltas (a diferencia de una red de datagramas), el espacio de números de secuencia puede ser más chico que en TCP sobre IP, pero de todos modos se necesitan.

## Ejercicio 4

Contexto: un monitor de red con **recursos limitados que no mantiene estado** de las conexiones, que ve **un único paquete** del three-way handshake y necesita (1) **confirmar que la conexión se estableció** y (2) **identificar cliente y servidor**.

Repaso de la máquina de estados:
- **Cliente**: `SYN_SENT` → (recibe SYN-ACK, manda ACK) → **ESTABLISHED** (al *mandar* el 3er ACK).
- **Servidor**: `SYN_RCVD` → (recibe el 3er ACK) → **ESTABLISHED** (al *recibir* el 3er ACK).

**Respuesta: el segundo paquete, el SYN-ACK.**

Justificación:
1. **Identifica los roles de forma intrínseca**: el SYN+ACK es el único paquete de toda la conexión con ambos flags juntos, y solo lo manda el servidor (respuesta a un *passive open*). Entonces emisor = servidor, destino = cliente, sin necesidad de mantener estado.
2. **Es auto-identificable sin estado**: como la combinación SYN+ACK es única, el monitor lo detecta matcheando los flags, sin recordar nada de la conexión.
3. **Es evidencia fuerte de establecimiento**: un SYN-ACK existe solo si llegó un SYN real *y* el servidor lo aceptó (hubo pedido y aceptación). No es un escaneo a un puerto cerrado, que devolvería RST.

**Por qué no los otros:**
- **SYN**: identifica al cliente, pero no indica que la conexión se haya establecido. Puede ser un port scan, un SYN flood, un puerto cerrado (→ RST) o un host caído. Registraría como "establecidas" conexiones que nunca lo fueron.
- **ACK (el tercero)**: es el paquete que *completa* ESTABLISHED, pero es el peor candidato para un monitor sin estado:
  - Es un ACK "pelado" (solo flag A), indistinguible de todos los ACK de datos posteriores si no se mantiene estado — justo la restricción del ejercicio.
  - No lleva el rol en sí mismo: nada en el paquete dice "soy el cliente"; solo se sabe si ya se asume que es el 3er paquete del handshake.
  - Si ese ACK se pierde, el servidor tampoco llega a ESTABLISHED.

En resumen: el SYN-ACK es el punto justo entre "la conexión es real/aceptada" y "puedo identificarla y ver los roles" sin mantener estado.

## Ejercicio 5

### a. ¿Cuántas conexiones y a cuál pertenece cada segmento?

Cada conexión se identifica por la **4-tupla** `(IPorig, puertoOrig, IPdest, puertoDest)`, es decir el conjunto de ambos extremos sin importar la dirección. Hay **2 conexiones**:

- **CONN1** = `{1.2.3.4:5678 ↔ 20.232.1.1:80}` → segmentos **1, 3, 4, 6, 8, 9, 11, 12, 14**. Cliente: `1.2.3.4` (manda el SYN, *active open*); servidor: `20.232.1.1:80` (puerto 80 = HTTP).
- **CONN2** = `{1.1.1.1:2222 ↔ 3.3.3.3:4444}` → segmentos **2, 5, 7, 10, 13**. Cliente: `1.1.1.1`; servidor: `3.3.3.3:4444`.

Desarrollo de **CONN1**:
- **1, 3, 4**: three-way handshake. `SYN seq=0` → `SYN-ACK seq=10000, ack=1` → `ACK seq=1, ack=10001`. El ISN del server (10000) es arbitrario/aleatorio, es normal.
- **6**: el cliente manda 50 bytes de datos (`seq=1`, bytes 1..50). Nota: **#4** es el ACK que completa el handshake (len=0) y **#6** el primer segmento de datos; podrían haber ido *piggybacked* en un solo segmento. El nº de ACK se repite (10001) porque el server todavía no mandó nada nuevo.
- **8**: el server confirma los 50 bytes (`ack=51 = 1+50`). **9**: el server manda 200 bytes (`seq=10001`, bytes 10001..10200). #8 y #9 podrían combinarse, porque #9 ya lleva `ack=51`.
- **11, 12, 14**: cierre. `FIN` del server (`seq=10201`) → `FIN+ACK` del cliente (`ack=10202`, `seq=51`) → `ACK` del server (`ack=52`). El 4-way se resume en 3 porque el cliente junta *su ACK del FIN ajeno* + *su propio FIN* en el mismo segmento.

### b. Cierre anómalo y posible causa

CONN2 arranca normal (handshake **2, 5, 7**: `SYN seq=42` → `SYN-ACK seq=54321, ack=43` → `ACK seq=43, ack=54322`). La anomalía está en:

**#10**: `1.1.1.1 → 3.3.3.3, flags = SAU (SYN+ACK+URG), seq=43, ack=64334, len=0`
- **SYN sobre una conexión ya establecida**: no tiene sentido, es ilegal.
- **`ack=64334` no coincide**: reconoce bytes que el servidor nunca envió (solo emitió su SYN en `54321`; un ACK válido sería `54322`). Es un ACK fuera de ventana, imposible.
- (El `seq=43` en cambio *sí* es válido: es la posición actual del cliente. Lo roto son el ACK y los flags.)

**#13**: `3.3.3.3 → 1.1.1.1, flags = RA (RST+ACK)` → el servidor **resetea**. Al recibir un segmento incoherente con el estado de la conexión, la aborta con un RST (uso del RST según la teórica p.22: *"resetear una conexión que se ha vuelto confusa"*). Por eso CONN2 cierra de forma **anómala (RST)** en lugar del FIN de manual que usó CONN1.

**Causa posible**: un **ataque de inyección** — un atacante *off-path* que intenta hijackear/interrumpir la conexión debe *adivinar* los números de secuencia; una adivinanza errada produce exactamente esto (seq plausible pero ack fuera de ventana y flags ilegales). Alternativas válidas: un segmento viejo/duplicado de otra encarnación de la conexión dando vueltas por la red, corrupción de bits, o un host que se reinició y perdió el estado.

### c. Cambios de estado de CONN1 en cada extremo

| Segmento | Servidor (`20.232.1.1`) | Cliente (`1.2.3.4`) |
|---|---|---|
| inicio | LISTEN | CLOSED |
| **#1** SYN → | LISTEN | → **SYN_SENT** |
| **#3** SYN-ACK → | → **SYN_RCVD** | SYN_SENT |
| **#4** ACK → | → **ESTABLISHED** | → **ESTABLISHED** |
| #6 / #8 / #9 datos | ESTABLISHED | ESTABLISHED |
| **#11** FIN (server) → | → **FIN_WAIT_1** | ESTABLISHED |
| **#12** FIN+ACK (client) → | → **TIME_WAIT** | → **CLOSE_WAIT** → **LAST_ACK** |
| **#14** ACK (server) → | TIME_WAIT | → **CLOSED** |
| +2·MSL | → **CLOSED** | CLOSED |

- El servidor es el *active closer* (inicia el cierre en #11) → termina en **TIME_WAIT** (va a TIME_WAIT quien manda el último ACK del cierre) y pasa a CLOSED tras `2·MSL`.
- El cliente es el *passive closer*: `ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED`. El `#12` hace dos transiciones de una porque junta el ACK del FIN del server + su propio FIN.
- La transición `FIN_WAIT_1 → TIME_WAIT` del server es directa porque `#12` le acka su FIN y le trae el FIN del cliente en el mismo segmento (si vinieran separados pasaría por FIN_WAIT_2 o CLOSING).

## Ejercicio 7

Cliente = `3.14.15.92:654` (*active open*, manda el primer SYN en #1); servidor = `2.71.82.81:823`.

Contexto previo para ubicarse:
- **1, 2, 3**: three-way handshake.
- **4**: cliente manda 300 bytes (`seq=2`); **5**: server los acka (`ack=302`).
- **6 y 7**: es **el mismo segmento retransmitido** (`seq=302, len=1000` las dos veces); **8**: server acka hasta `1302`.

### a. Transiciones de estado a partir del segmento 9

El que inicia el cierre (*active close*) es el **servidor** (#9), no el cliente. Cuidado: quién abre la conexión (cliente = active open) es independiente de quién la cierra primero. Es un **4-way sin comprimir**: el cliente manda el ACK (#10) y su propio FIN (#11) en segmentos **separados**.

```
09  2.71.82.81 → 3.14.15.92   F   seq=2     ack=–      (servidor inicia el cierre)
10  3.14.15.92 → 2.71.82.81   A   seq=1302  ack=3      (cliente acka ese FIN)
11  3.14.15.92 → 2.71.82.81   F   seq=1302  ack=–      (cliente manda su FIN)
12  2.71.82.81 → 3.14.15.92   A   seq=3     ack=1303   (servidor acka el FIN del cliente)
```

| Segmento | Servidor `2.71.82.81` (*active close*) | Cliente `3.14.15.92` (*passive close*) |
|---|---|---|
| antes de #9 | ESTABLISHED | ESTABLISHED |
| **#9** FIN (server) → | → **FIN_WAIT_1** | (recibe FIN) → **CLOSE_WAIT** |
| **#10** ACK (client) → | (recibe ACK) → **FIN_WAIT_2** | CLOSE_WAIT (manda ACK, no cambia) |
| **#11** FIN (client) → | (recibe FIN) → **TIME_WAIT** | → **LAST_ACK** (manda su FIN) |
| **#12** ACK (server) → | TIME_WAIT (manda ACK) | (recibe ACK) → **CLOSED** |
| +2·MSL | → **CLOSED** | CLOSED |

Caminos canónicos:
- **Active closer** (server): `ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED`.
- **Passive closer** (client): `ESTABLISHED → CLOSE_WAIT → LAST_ACK → CLOSED`.

`CLOSING` no aparece: es el caso de **cierre simultáneo** (ambos mandan FIN antes de recibir el del otro). Estando en `FIN_WAIT_1`, lo que te llega decide: ACK de tu FIN → `FIN_WAIT_2` (este caso); FIN → `CLOSING`; FIN+ACK juntos → directo a `TIME_WAIT`.

### b. Segmentos para estimar el RTT

Una muestra de RTT se toma entre que se manda algo que **consume número de secuencia** (datos, SYN o FIN) y llega **el ACK que lo confirma**. La excepción clave es la de **Karn/Partridge** (teórica p.49): **no se usan segmentos retransmitidos**, por la *ambigüedad del ACK* (no se sabe si el ACK confirma la transmisión original o la retransmisión).

**Sirven:**

| Par | Qué mide |
|---|---|
| **#1 ↔ #2** | SYN / SYN-ACK (RTT inicial, lo mide el cliente) |
| **#2 ↔ #3** | SYN-ACK / ACK (lo mide el servidor) |
| **#4 ↔ #5** | 300 bytes de datos / ACK |
| **#9 ↔ #10** | FIN del server / ACK |
| **#11 ↔ #12** | FIN del cliente / ACK |

**No sirve:**

| Par | Por qué |
|---|---|
| **#6 / #7 ↔ #8** | El segmento se retransmitió (mismo `seq=302, len=1000`) → ambigüedad del ACK → Karn/Partridge lo excluye |

## Ejercicio 9

Nuestro host es `192.168.1.104`. Estado inicial según netstat:
- `0.0.0.0:7777` en **LISTEN** (tenemos un server escuchando en el 7777).
- `:48600 ↔ 200.42.33.121:80` **ESTABLISHED** (somos cliente HTTP).
- `:34688 ↔ 69.163.203.254:80` **TIME_WAIT** (somos cliente y cerramos primero → *active closer*).
- `:45911 ↔ 173.194.42.245:443` **ESTABLISHED** (somos cliente HTTPS).

### a. netstat al final de los 5 minutos

Conexión por conexión:

- **`0.0.0.0:7777` LISTEN → sigue en LISTEN.** Aceptar una conexión no consume el socket que escucha: la conexión nueva es *otro* socket, con su 4-tupla completa.
- **Nueva: `:7777 ↔ 192.168.1.247:27351` → ESTABLISHED.** Three-way handshake completo (#1 SYN, #4 SYN-ACK, #5 ACK) y después nada más. Nosotros somos el servidor: `LISTEN → SYN_RCVD → ESTABLISHED`.
- **`:48600 ↔ 200.42.33.121:80` → sigue ESTABLISHED.** Hay tráfico (#2 GET, #6 ACK, #7 200 OK), pero ningún FIN ni RST.
- **`:34688 ↔ 69.163.203.254:80` → desaparece (CLOSED).** TIME_WAIT dura `2·MSL` (con MSL = 2 min según RFC 793, 4 min; en Linux 60 s), menos que los 5 minutos de la captura. Al vencer el timer pasa a CLOSED y deja de listarse.
  > Que estemos en TIME_WAIT siendo cliente no es raro: TIME_WAIT le toca al **que cerró primero** (*active close*), sea cliente o servidor. Cliente/servidor solo importa en la apertura (quién hace LISTEN y quién CONNECT); una vez en ESTABLISHED, cualquiera de los dos puede cerrar primero.
- **`:45911 ↔ 173.194.42.245:443` → CLOSE_WAIT.** En #8 el server manda su FIN (es su propio FIN y no la respuesta a uno nuestro: `Ack=2347` es nuestro `Seq` actual; si hubiéramos mandado FIN, el ack sería 2348). En #9 lo ackeamos (`Ack=4563 = 4562+1`). Somos el *passive closer*: `ESTABLISHED → CLOSE_WAIT`. Para seguir a LAST_ACK nuestra aplicación tendría que hacer `close()` y mandar su FIN, y como la traza es la porción final del tráfico, eso no ocurrió.

```
Proto  Local Address          Foreign Address        State
tcp    0.0.0.0:7777           0.0.0.0:*              LISTEN
tcp    192.168.1.104:7777     192.168.1.247:27351    ESTABLISHED
tcp    192.168.1.104:48600    200.42.33.121:80       ESTABLISHED
tcp    192.168.1.104:45911    173.194.42.245:443     CLOSE_WAIT
```

### b. Instante más temprano en que el receptor puede enviar datos

El receptor es **nuestro host** (`192.168.1.104:7777`), que en esta conexión hace de servidor.
- Al recibir el SYN (#1) y mandar el SYN-ACK (#4) queda en **SYN_RCVD**. En ese estado todavía no puede mandar datos (según RFC 793, un SEND se encola hasta llegar a ESTABLISHED).
- Pasa a **ESTABLISHED al recibir el #5** (el ACK del cliente). **Ese es el instante más temprano en que puede enviar datos.**

En cambio, el que inició la conexión (`192.168.1.247`) ya está ESTABLISHED al recibir el #4, así que podría mandar datos junto con el propio #5 (*piggybacked*).

## Ejercicio 10

La captura se hace desde `192.168.0.1`, el **default gateway** de `192.168.0.100`: todo el tráfico de `.100` hacia otras redes pasa por él, por eso ve toda la conexión (y en el b puede alterarla, como *man-in-the-middle*).

Roles: **cliente** = `192.168.0.100:60205` (manda el SYN, *active open*); **servidor** = `157.92.27.21:80` (HTTP, *passive open*, en LISTEN de antemano).

### a. Cambios de estado de ambos extremos

| Segmento | Cliente `192.168.0.100` | Servidor `157.92.27.21` |
|---|---|---|
| inicio | CLOSED | LISTEN |
| **#1** SYN → | → **SYN_SENT** | → **SYN_RCVD** (al recibirlo y mandar #2) |
| **#2** SYN-ACK ← | → **ESTABLISHED** (al recibirlo y mandar #3) | SYN_RCVD |
| **#3** ACK → | ESTABLISHED | → **ESTABLISHED** |
| #4 – #9 datos | ESTABLISHED | ESTABLISHED |

- **#4**: el cliente manda el GET (567 bytes, por eso el server ackea `568`).
- **#6, #8**: el server manda la respuesta HTTP partida en segmentos de 1448 bytes (`Ack=1449`, `Ack=2897`); #7 y #9 son los ACKs del cliente.
- No hay FIN ni RST → ambos extremos quedan en **ESTABLISHED**.

### b. El gateway reemplaza el #9 por un RST+ACK

`192.168.0.100 → 157.92.27.21  60205 > http [RST, ACK] Seq=568 Ack=2897`

- **El servidor lo acepta como legítimo**: IPs y puertos coinciden con la 4-tupla, y lo decisivo es que un RST solo se acepta si su **número de secuencia cae dentro de la ventana** esperada. `Seq=568` es justo el próximo byte que espera del cliente → válido. No tiene forma de distinguirlo de uno que haya mandado `.100` de verdad.
- **Servidor: ESTABLISHED → CLOSED** de inmediato. Aborta la conexión sin pasar por los estados de cierre ni por TIME_WAIT, descarta sus buffers, y a la aplicación le llega un *connection reset*.
- **Cliente: sigue en ESTABLISHED**. Su ACK original nunca le llegó al server y no recibió nada que le avise. Queda una conexión **half-open** (semiabierta): el cliente cree que está conectado y sigue esperando el resto de la respuesta HTTP.

**Qué pasa después**: el servidor no manda nada más (para él la conexión no existe). Si el cliente envía algo, el servidor no tiene estado para esa 4-tupla y responde con **RST** → recién ahí el cliente pasa a **CLOSED**. Si el cliente no envía nada, queda colgado en ESTABLISHED hasta que la aplicación corte por timeout (o salte un keepalive, si está activo).


## Ejercicio 11

Host `10.80.1.10`. Comparando netstat en t0 y t1, conexión por conexión:

| Conexión | t0 | t1 | Qué pasó |
|---|---|---|---|
| `0.0.0.0:8080` | LISTEN | LISTEN | nada (el socket que escucha no se consume al aceptar) |
| `:35336 ↔ 157.92.27.21:80` | SYN_SENT | CLOSE_WAIT | se estableció y el server cerró primero |
| `:51247 ↔ 200.42.93.137:80` | TIME_WAIT | — | venció el timer de 2·MSL → CLOSED |
| `:8080 ↔ 200.11.54.101:32154` | — | ESTABLISHED | conexión entrante nueva (somos servidor) |
| `:24592 ↔ 98.139.183.24:80` | ESTABLISHED | ESTABLISHED | sin FIN ni RST (puede haber habido datos o no) |

### a. Intercambio de paquetes propuesto

**Conexión `:35336 ↔ 157.92.27.21:80` (somos cliente).** Nuestro SYN ya se había mandado antes de t0 (por eso estábamos en SYN_SENT).

```
1. 157.92.27.21  → 10.80.1.10     SYN+ACK   nosotros: SYN_SENT → ESTABLISHED (y mandamos 2)
2. 10.80.1.10    → 157.92.27.21   ACK       server:   SYN_RCVD → ESTABLISHED
3. 157.92.27.21  → 10.80.1.10     FIN       nosotros: ESTABLISHED → CLOSE_WAIT (y mandamos 4)
4. 10.80.1.10    → 157.92.27.21   ACK       server:   FIN_WAIT_1 → FIN_WAIT_2
```

El server es el *active closer* y nosotros el *passive closer*. Nos quedamos en CLOSE_WAIT porque nuestra aplicación todavía no hizo `close()` (si lo hiciera, mandaríamos FIN y pasaríamos a LAST_ACK).

**Conexión `:8080 ↔ 200.11.54.101:32154` (somos servidor).** El puerto local 8080 es el que estaba en LISTEN, y el remoto (32154) es efímero → la abrió el otro host.

```
5. 200.11.54.101 → 10.80.1.10     SYN       nosotros: LISTEN → SYN_RCVD (y mandamos 6)
6. 10.80.1.10    → 200.11.54.101  SYN+ACK   cliente:  SYN_SENT → ESTABLISHED (y manda 7)
7. 200.11.54.101 → 10.80.1.10     ACK       nosotros: SYN_RCVD → ESTABLISHED
```

Ojo: mandar el SYN+ACK **no** nos lleva a ESTABLISHED; el servidor pasa a ESTABLISHED recién al **recibir** el ACK (7).

**Conexión `:51247 ↔ 200.42.93.137:80`**: no hacen falta paquetes; solo que venza el timer de TIME_WAIT (2·MSL) → CLOSED, y deja de listarse.

**Conexión `:24592 ↔ 98.139.183.24:80`**: no hace falta proponer paquetes. Puede haber intercambio de datos en ESTABLISHED, pero ni FIN ni RST.

### b. Cota inferior para t1

$$t_1 \geq t_0 + 2 \cdot MSL$$

(≈ 4 minutos si se toma MSL = 2 min, como define el RFC 793.)

Justificación:
- Según la máquina de estados, de **TIME_WAIT** se sale únicamente por **timeout de 2·MSL** (la teórica lo describe como la *"expiración de temporizador del doble del tiempo de vida máximo del paquete"*).
- Lo último que manda el que está en TIME_WAIT es el ACK del FIN remoto. Si el otro extremo retransmite su FIN (porque perdió nuestro ACK), se vuelve a ackear y **se reinicia** el timer de 2·MSL (RFC 793, sección 3.9: *"Acknowledge it, and restart the 2 MSL timeout"*).
- Si el último paquete enviado a `200.42.93.137` fue en t0, el timer arrancó (a más tardar) en t0 → la conexión recién puede pasar a CLOSED en `t0 + 2·MSL`. Como en t1 ya no aparece, `t1 ≥ t0 + 2·MSL`.

El resto de las conexiones no aporta una cota útil: sus intercambios pueden ocurrir en unos pocos RTT.
