# Simulacro resuelto (ej 1–5)

Armado a partir de lo que respondiste y de las correcciones del chat. El 6 lo hacés vos.

---

## Ejercicio 1 — Retroalimentaciones del control de congestión

TCP no recibe información explícita de la red (es **lazo cerrado implícito**): infiere el estado de la red a partir de lo que le vuelve del receptor. Hay tres retroalimentaciones.

**1. Llega un ACK que reconoce datos nuevos (retroalimentación positiva).** Los datos están llegando, así que la red aguanta y CWND crece. Cuánto crece depende de la fase:
- **Slow start** (CWND < SSTHRESH): `CWND += min(N, SMSS)` por ACK, con N = bytes nuevos reconocidos. Una ventana entera de ACKs por RTT hace que CWND **se duplique por RTT**. Se topea en SSTHRESH y se pasa a CA.
- **Congestion avoidance** (CWND ≥ SSTHRESH): `CWND += SMSS²/CWND` por ACK. Como hay CWND/SMSS ACKs por RTT, el total es **+1 SMSS por RTT** (crecimiento lineal).

**2. Vence el timeout (retroalimentación negativa fuerte).** No volvió ningún ACK: es la señal más grave, porque probablemente se perdió la ráfaga entera.
- `SSTHRESH = max(FlightSize/2, 2·SMSS)`
- `CWND = LW = 1 SMSS`
- Se vuelve a **slow start** desde 1 SMSS.

**3. Llegan 3 ACKs duplicados (4 iguales), una retroalimentación negativa más leve.** Se perdió un segmento, pero los posteriores **siguen llegando**, porque cada dup es un segmento que llegó al receptor. La red todavía entrega, así que no se corta a 1 SMSS:
- **Fast retransmit:** se retransmite el segmento perdido en el momento, sin esperar el timeout.
- **Fast recovery:**
  - `SSTHRESH = max(FlightSize/2, 2·SMSS)` y `CWND = SSTHRESH + 3 SMSS` (los 3 dups son 3 segmentos que salieron de la red).
  - Por cada dup extra, `CWND += 1 SMSS` (se **infla**): salió otro segmento y se puede mandar uno nuevo en su lugar.
  - Cuando llega el ACK nuevo que reconoce la retransmisión, `CWND = SSTHRESH` (se **desinfla**) y se pasa a **CA**.

El corte a la mitad (decremento multiplicativo) junto con el +1 SMSS/RTT (aumento aditivo) es **AIMD**, que converge a eficiencia y equidad entre flujos (Chiu-Jain).

---

## Ejercicio 2 — Secuencia DNS para `www.dominio.com.ar`

**Supuestos:** cachés vacías. Hay una zona por subdominio: raíz, `ar`, `com.ar`, `dominio.com.ar`, y `www` es un host dentro de `dominio.com.ar`. Las IPs son de ejemplo. Todo va por **UDP 53**.

En la PC, la aplicación llama al **stub resolver**, que no resuelve nada: le hace una consulta **recursiva** al **resolver** configurado (el del ISP). El resolver hace las consultas **iterativas** preguntando siempre el **nombre completo**.

| # | De → a | Tipo | Mensaje |
|---|---|---|---|
| 1 | PC (stub) → resolver | recursiva | `www.dominio.com.ar A?` |
| 2 | resolver → servidor raíz | iterativa | `www.dominio.com.ar A?` |
| 3 | raíz → resolver | referral | `ar NS ns.ar` + glue `ns.ar A 1.2.3.4` |
| 4 | resolver → ns.ar | iterativa | `www.dominio.com.ar A?` |
| 5 | ns.ar → resolver | referral | `com.ar NS ns.com.ar` + glue `ns.com.ar A 1.2.3.5` |
| 6 | resolver → ns.com.ar | iterativa | `www.dominio.com.ar A?` |
| 7 | ns.com.ar → resolver | referral | `dominio.com.ar NS ns.dominio.com.ar` + glue `ns.dominio.com.ar A 1.2.3.6` |
| 8 | resolver → ns.dominio.com.ar | iterativa | `www.dominio.com.ar A?` |
| 9 | ns.dominio.com.ar → resolver | **autoritativa (aa)** | `www.dominio.com.ar A 1.2.3.7` |
| 10 | resolver → PC | respuesta (no autoritativa) | `www.dominio.com.ar A 1.2.3.7` |

- **Referral:** el servidor no tiene la respuesta, así que delega con el NS de la zona hija. El **glue** es el A de ese NS, que va en ADDITIONAL porque el NS está dentro de la zona delegada (si no, sería circular).
- El mensaje 9 es **autoritativo** porque ns.dominio.com.ar es el servidor de la zona que contiene `www`: responde con sus propios datos. Los anteriores son autoritativos solo de su zona y lo único que saben es a quién delegaron.
- El mensaje 10 es **no autoritativo**: el resolver no es dueño de la zona, reenvía lo que aprendió (y lo cachea por el TTL).

---

## Ejercicio 3 — Conexiones TCP: mail + webmail

**Supuestos:**
- El emisor usa un **cliente de correo (UA)**, por ejemplo Thunderbird, configurado con el servidor saliente de `undominio.org.ar`.
- El webmail de `otrodominio.org.ar` es un servidor aparte que lee el buzón por **IMAP**. POP3 también sería válido.
- El webmail usa HTTP/1.1 persistente (HTTPS) y todos sus recursos están en el mismo host. Si alguno estuviera en otro host, sería otra conexión TCP.
- El mail no tiene recursos externos que se descarguen al abrirlo.

| # | Entre (quién abre → quién atiende) | Protocolo de aplicación | Puerto |
|---|---|---|---|
| 1 | UA del emisor → servidor **saliente** de undominio.org.ar | SMTP (submission, con autenticación) | 587 |
| 2 | Servidor saliente de undominio → **MX** de otrodominio.org.ar | SMTP (servidor a servidor) | 25 |
| 3 | Servidor **webmail** → servidor de correo de otrodominio (buzón) | IMAP | 143 (993 con TLS) |
| 4 | **Navegador** del destinatario → servidor webmail | HTTP(S) | 80 / 443 |

- Entre la 1 y la 2, el saliente encola el mail y **busca el MX** de `otrodominio.org.ar` (y el A del MX) con **su** resolver. Esto es DNS sobre **UDP**, así que no cuenta como conexión TCP.
- La 3 la abre el webmail, que es el cliente IMAP y pide los mails del usuario. Puede ser cuando el usuario entra o periódicamente.
- La 4 usa una sola conexión gracias a HTTP/1.1 persistente: el HTML de la bandeja y sus recursos van por la misma conexión.

**Total: 4 conexiones TCP.**

---

## Ejercicio 4 — Autenticar empleados con certificados (app móvil)

**Idea:** la empresa usa su certificado firmado por una CA para actuar como **CA de sus empleados** (CA intermedia): con su privada firma los certificados de cada empleado. La autenticación es con **TLS mutuo**, sin usuario y contraseña.

**Qué se instala en cada lado:**

| Dónde | Qué |
|---|---|
| **Servidor** de la app | su par de claves + su **Cert_S** (firmado por la empresa/CA) + la pública de la empresa (o la cadena hasta la CA raíz) para validar a los empleados |
| **App de cada empleado** | **su** par de claves (la privada no sale del dispositivo) + su **Cert_E** firmado por la empresa + la **K+CA** para validar al servidor |
| **Empresa** | su certificado firmado por la CA y su privada, con la que emite y revoca los certificados de los empleados |

Nadie guarda públicas ajenas: el certificado del otro llega en el handshake y se valida con la pública de la CA o de la empresa.

**Handshake (TLS mutuo):**
1. **ClientHello** (con R_C) / **ServerHello** (con R_S).
2. El servidor manda **Certificate (Cert_S)** y la app lo valida con K+CA: firma, vigencia, nombre. Así el empleado sabe que habla con el servidor real.
3. El servidor manda **CertificateRequest**.
4. La app manda **Certificate (Cert_E)**, **ClientKeyExchange** (la PMS cifrada con K+S) y **CertificateVerify**, que es la **firma con la privada del empleado** sobre todo el handshake, nonces incluidos.
5. **ChangeCipherSpec + Finished** de los dos lados. `master = PRF(PMS, "master secret", R_C + R_S)` y de ahí salen las **claves de sesión simétricas**: todo lo que sigue viaja cifrado de forma simétrica.

**Qué chequea el servidor sobre el empleado:**
1. Que Cert_E esté firmado por la empresa.
2. Que esté vigente y no revocado (CRL/OCSP).
3. Que el CertificateVerify verifique con la pública de Cert_E. Eso prueba que tiene la privada, y como va sobre los nonces, no es un replay.
4. Que ese empleado esté autorizado.

Si falla cualquiera, se corta el handshake.

**Por qué escala:** cuando entra un empleado, la empresa le emite un certificado; cuando se va, se **revoca**. No hay que tocar el servidor ni distribuir públicas.

---

## Ejercicio 5 — Bicicletas públicas

**Supuestos:**
- El desbloqueo es con un **QR** en el anclaje: la app se lo manda al servidor, el servidor autoriza y le ordena a la estación destrabar, como en Ecobici.
- **Sacar** una bici sin conexión **no** se soporta: la consigna no lo pide y necesita la autorización del servidor. **Devolver** sí.
- "Lleva los viajes" quiere decir origen, destino y horarios, sin GPS.
- Servidor y base de datos se toman como un componente, porque nadie más accede a la base. Lógicamente son dos niveles: procesamiento y datos.
- La app **nunca** crea viajes ni da órdenes a la estación: todo lo autoriza el servidor.

### a) Componentes

| Componente | Interfaz | Procesamiento | Datos |
|---|---|---|---|
| **Anclaje** (sensor + traba) | `estado() → libre / ocupado(idBici)` · `trabar()` · `destrabar()` | ninguno: mide y actúa | — |
| **Controlador de estación** | `destrabar(anclaje, idViaje)` · `sincronizar()` · publica eventos de estado | recibe la orden y destraba. Al detectar una bici, la traba y registra la devolución. Si no hay conexión, la encola y la reenvía al volver | estado de cada anclaje + **cola de eventos pendientes** `(idEvento, bici, anclaje, timestamp)` |
| **Servidor central** | `disponibilidad(zona)` · `pedirDesbloqueo(usuario, estación, anclaje)` · `viajeActual(usuario)` · `registrarEvento(estación, evento)` | autoriza desbloqueos, abre y cierra viajes, mantiene la disponibilidad, cobra | usuarios, viajes, disponibilidad por estación |
| **App móvil** | UI: mapa, escanear QR, viaje actual | pide la disponibilidad, manda el QR escaneado, muestra el viaje | sesión/token del usuario, viaje actual |

**Devolución sin conexión:**
1. El sensor detecta la bici.
2. El controlador traba y guarda el evento en su cola local, con su timestamp.
3. Cuando vuelve la conexión, `sincronizar()` lo manda y el servidor cierra el viaje con ese timestamp.
4. El **idEvento** hace que el reintento sea **idempotente**: si se pierde el OK y el controlador reenvía, el servidor detecta el duplicado y no registra dos devoluciones (como en el ej 6 de la guía 8).

### b) Conectores y acoplamiento

| Conector | Protocolo | Referencial | Temporal | Por qué |
|---|---|---|---|---|
| Anclaje ↔ controlador | bus local / cableado | acoplado | acoplado | **directa**: hardware fijo de la estación, siempre presente |
| App → servidor | REST sobre HTTPS | acoplado | acoplado | **directa**, pedido y respuesta: el usuario espera la respuesta en el momento (disponibilidad, desbloqueo) |
| Servidor → controlador (destrabar) | **pub/sub**: el controlador se suscribe a `estación=X`; el servidor publica `(estación=X, anclaje=3, destrabar)` | **desacoplado** | acoplado | el servidor no necesita la dirección de cada estación, y agregar una estación es solo suscribirla. Es temporal acoplado (si la estación está desconectada no le llega), pero sin conexión no se permite sacar bicis, así que no molesta. El controlador confirma con un evento "anclaje 3 destrabado" antes de que arranque el viaje |
| Controlador → servidor (devoluciones, estado) | **cola / mailbox** (store-and-forward) | acoplado | **desacoplado** | el controlador sabe a quién manda, pero el servidor puede no estar alcanzable. Los eventos se guardan y se reenvían: esto cumple el requisito de la desconexión |

No se usa un mapa en vivo con pub/sub hacia la app: la consigna pide que el **servidor** lleve la disponibilidad en tiempo real, y la app la pide cuando se abre el mapa.

### c) Edge / fog / cloud

| Componente | Capa | Justificación |
|---|---|---|
| Anclajes (sensores, trabas) | dispositivo | hardware sin lógica |
| Controlador de estación | **edge** | **autonomía**: la devolución tiene que funcionar sin red, así que la lógica de trabar y registrar vive en la estación. **Latencia**: trabar en el momento en que el sensor detecta la bici, sin un ida y vuelta a la nube |
| Servidor central | **cloud** | **vista global**: usuarios, viajes, cobros y la disponibilidad de todas las estaciones. Ninguna estación sola lo sabe. No tiene latencia crítica (unos cientos de ms para desbloquear son aceptables) y es accesible desde cualquier lugar |
| App móvil | dispositivo del usuario | UI |

**Fog:** no hace falta. Sería un nivel intermedio, por ejemplo un servidor por barrio que agregue sus estaciones. El volumen de eventos es chico y no hay latencias que lo justifiquen.

**Consistencia al reconectar:**
- Mientras la estación estuvo desconectada, **el servidor tuvo un estado viejo**: creía que el viaje seguía abierto y que en esa estación había menos bicis.
- Al sincronizar, el controlador manda los eventos encolados. El servidor **cierra el viaje con el timestamp del controlador**, no con la hora de llegada del mensaje, para no cobrar de más, y actualiza la disponibilidad.
- Es **consistencia eventual**: mientras dura la partición el sistema elige **disponibilidad** (se puede devolver) en lugar de consistencia (CAP), y cuando cesa la partición las réplicas convergen.
- Un detalle: el timestamp depende del reloj de la estación, que puede derivar. Se sincroniza con NTP cuando hay conexión, y unos segundos de error no importan para cobrar.
