# Notas para el machete — 2do parcial Redes (RCCD 2C 2026)

Borrador acumulativo: lo que iría al machete de 1 página, guía por guía. Al final se arma con el pipeline de `redes/machete/` (machete.html + fit.py). Las ★ marcan lo que costó / se preguntó durante el estudio → prioridad alta.

---

## Congestión (Guía 5)

### Valores de la guía
SMSS = 2 KB · IW = 2·SMSS = 4 KB · LW = 1 SMSS = 2 KB (post time-out) · RW = min(IW, CWND) (post idle ≥ 1 RTO) · ISSTHRESH = 64 KB

### Ventanas
- Se envía **min(CWND, RWND)** por RTT (★ mínimo, no máximo). CWND no está topeada por RWND: siguen independientes.
- RWND = AdvertisedWindow = espacio libre en el buffer del receptor (control de **flujo**, lo anuncia el receptor en cada ACK). CWND = estimación del emisor de lo que aguanta la **red** (control de **congestión**).
- EffectiveWindow = MaxWindow − (LBS − LBA) · **FlightSize = LBS − LBA** ⇒ ★ LBA = LBS − Flight (clave ej. 12).

### Reglas (por ACK → consecuencia por RTT)
| Situación | SSTHRESH | CWND |
|---|---|---|
| SS (CWND < SSTHRESH) | = | +min(N, SMSS) por ACK ⇒ ×2/RTT, ★ topear en SSTHRESH |
| CA (CWND ≥ SSTHRESH) | = | +SMSS²/CWND por ACK ⇒ +1 SMSS/RTT |
| Time-out | max(**FlightSize**/2, 2 SMSS) | 1 SMSS → SS |
| 3 dup ACKs (4 iguales) | max(FlightSize/2, 2 SMSS) | SSTHRESH + 3 SMSS; +1 SMSS por dup extra |
| ACK nuevo en FR/FR | = | = SSTHRESH → CA |

- ★ SSTHRESH sale de **FlightSize/2** (lo enviado = min(CWND,RWND)), no de CWND/2.
- ★ Ráfaga perdida entera ⇒ no vuelve ningún ACK ⇒ **time-out** (nunca FR/FR).
- ★ Por qué +1/RTT en CA: (CWND/SMSS ACKs) × (SMSS²/CWND) = SMSS. En SS: W ACKs × 1 = +W ⇒ ×2.
- N = bytes **nuevos** que reconoce el ACK (dups suman 0). min(N,SMSS) evita ACK division.
- SSTHRESH solo cambia ante pérdida (puede subir si se pierde con ventana mayor).
- Corte a la mitad (MD): vaciar la cola + equidad AIMD (Chiu-Jain) + ser conservador.

### Método trazas (ej. 6, 9, 10, 11)
Tabla: RTT | CWND | se envía = min(CWND, RWND, falta) | ¿≥ umbral? | SSTHRESH | acumulado.
- Ráfaga perdida + espera RTO (2 RTT, timer desde el envío) = **2 RTTs**.
- Estado estacionario = SSTHRESH deja de cambiar. Ciclo: bytes útiles / RTTs ⇒ total = (datos / bytes por ciclo) × RTTs por ciclo.
- ★ RWND < umbral ⇒ nunca pierde ⇒ puede ser **más rápido** (ej. 11b: 18 KB/RTT vs ≈ 8,4).
- Escribir supuestos: duración time-out, borde CWND = SSTHRESH, 1 KB = 1024, 1 ACK por segmento.

### Leer tablas (ej. 12)
×2 = SS · +1 SMSS = CA · cae a 1 SMSS = time-out · cae a ~mitad (+3) = FR/FR · Flight < CWND ⇒ limita RWND o app · LBS baja ⇒ retransmisión desde LBA · LBA quieto + CWND sube ⇒ dup ACKs (inflado FR/FR).

### RTT / RTO
- RTT = ida + vuelta (segmento → ACK); ≠ Ttx = SMSS/BW (despreciable en ejercicios). En 1 RTT sale una ventana entera.
- RTT_est = α·RTT_est + (1−α)·Sample · RTO = 2·RTT_est. α alto (0,8–0,9) = estable; α bajo ⇒ RTO se desploma tras una muestra chica ⇒ ★ time-out **espurio**. Chequear Sample > RTO vigente **antes** de actualizar.
- Karn/Partridge: no samplear retransmitidos; al retransmitir, RTO ×2 (backoff → por debajo de 1 seg/RTT se frena en el tiempo).
- Jacobson/Karels: Diff = S − Est; Est += δ·Diff; Dev += δ(|Diff| − Dev); RTO = μ·Est + φ·Dev (μ=1, φ=4, δ=1/8).

### Teórica
- Congestión = sobrecarga **sostenida**, demanda ≥ capacidad ⇒ QoS degradada. Síntomas: pérdidas + delay creciente.
- Flujo (receptor, punto a punto) vs congestión (red, global).
- FIFO (scheduling: quién sale) + Drop Tail (buffer: se tira el que llega) ⇒ sincronización global.
- Knee: throughput deja de crecer, delay se dispara. Cliff: colapso, goodput → 0. Potencia = throughput/delay (máx ≈ knee).
- Jain: f = (Σx)² / (n·Σx²) ∈ [1/n, 1].
- M/M/1 (Kendall A/S/c): llegadas Poisson (exp. entre llegadas, sin memoria), servicio exp., 1 servidor. ρ = λ/μ < 1 para estacionario. E[N] = ρ/(1−ρ), E[T] = 1/(μ−λ) → ∞ con ρ → 1.
- Buffers infinitos no sirven (delay → time-outs → duplicados). Ruteo solo reparte, no reduce (métricas no miran carga; si miraran, oscilan). Prealocar con datagramas: no hay circuito.
- Taxonomía: lazo abierto (circuitos) / cerrado: implícito (TCP, pérdidas) vs explícito (ECN, DECbit, ATM ABR).
- RED: AvgLen = (1−w)·Avg + w·Sample; < MinTh encola, entre umbrales descarta con P, ≥ MaxTh descarta. MaxP ≈ 0,02, MaxTh = 2·MinTh. Evita sincronización global.
- Mathis: BW = (MSS/RTT)·√(3/2)/√p.
- Slow Start: "slow" vs TCP pre-1988 (mandaba toda la AdvWin).
- CWND no representativa: errores de bit (WiFi), idle, app-limited.

---

## Aplicación (Guía 6)

### Base
- Orden siempre: nombre → **DNS (UDP 53)** → IP → **TCP** (1 RTT handshake) → protocolo app. Integradores = aplicar esto a **cada host nuevo**.
- Puertos: HTTP 80 · HTTPS 443 · SMTP 25 (587 submission) · POP3 110 · IMAP 143 · DNS 53/UDP.
- ★ 1 servidor/1 IP/1 puerto alcanzan para N clientes: TCP distingue por la **4-upla** (IPc, puertoc, IPs, puertos); el cliente usa puerto efímero. Escalar = capacidad (LB / varios A en DNS), no puertos.
- DNS round robin (varios A) vs balanceador: DNS reparte grueso (TTL/caché, no detecta caídas); LB fino + health checks, pero punto único.

### DNS
- ★ **Stub resolver** en la PC (no resuelve nada) → consulta **recursiva** → **resolver** (servidor: ISP, 8.8.8.8) → consultas **iterativas** raíz → TLD → … → autoritativo. El cliente no "está en una zona".
- ★ El resolver arranca del **ancestro más cercano en su caché** (si no, raíz). Caché solo ayuda si comparten ancestro (.ar no sirve para .com). **Cada resolver tiene su caché** (no se comparten).
- Registros `nombre TTL IN tipo valor`: A/AAAA (IP) · CNAME (alias, seguir cadena; ★ un nombre con CNAME no tiene otros registros; apex no puede ser CNAME) · MX (prioridad, menor = mejor) · NS · SOA · PTR.
- ★ **NS**: (1) en la zona padre = **delegación** (referral "preguntale a…"); (2) en la zona = lista de autoritativos (aa). Varios por redundancia. Dominio con DNS en otro gestor ⇒ cargar sus NS en el registrar (va a la zona padre). "Propagación" = TTL de NS viejos.
- ★ **Glue**: A del NS en la zona padre cuando el NS está **dentro** de la zona delegada (si no, circular). Va en ADDITIONAL.
- **Primario** = primer nombre del SOA; resto de los NS = secundarios (copian si sube el **serial**). SOA: serial, refresh, retry, expire, minimum (= TTL caché negativa).
- Respuesta autoritativa (aa, de primario/secundario) vs no autoritativa (caché). Secciones: ANSWER / AUTHORITY (NS) / ADDITIONAL (A extra).
- TTL + cambio de IP: resolvers con caché siguen dando la IP vieja hasta que vence el TTL.
- DNS centralizado / sin caché / con conexión ⇒ cuello de botella + punto de falla, varios RTT extra por host, +1 RTT handshake. Afecta cada HTTP; SMTP menos (asincrónico, encola).

### Mail
- ★ **Servidor saliente** = SMTP de **tu proveedor** (configurado en el cliente: Gmail → smtp.gmail.com:587). Te autentica, encola y reintenta. ≠ entrante/MX (del **destinatario**) ≠ POP3/IMAP (donde leés).
- ★ El **MX lo busca el saliente** (con **su** resolver), no la PC. La PC solo resuelve el A de su saliente.
- Cadena: UA ─SMTP→ saliente ─(DNS MX+A)─SMTP→ MX destino → buzón ─POP3/IMAP→ UA. Webmail: navegador ─HTTP(S)→ webmail, que hace SMTP por dentro.
- MX hoy sería un SRV/SVCB genérico; existe porque el mail va a otra máquina que la web (dc.uba.ar: web UBA, mail Google).

### HTTP
- ★ Request 1.1: `MÉTODO ruta HTTP/1.1` + **Host obligatorio** (virtual hosting) + línea en blanco. HEAD = headers sin cuerpo. GET condicional `If-Modified-Since` → **304** si no cambió.
- Respuesta: `HTTP/1.1 código texto` + `Content-Type` (tipo MIME) + `Content-Length` + línea en blanco + cuerpo. POST de un upload → **201 Created** + `Location`.
- **RTTs por página** (ej. 6): cada objeto = 1 RTT handshake + 1 RTT GET. 1.0 no persistente: 2·n · 1.1 persistente sin pipelining: 2 + (n−1) · con pipelining: 2 + 1 = **3**. Embebidos recién después de parsear el HTML.
- ★ **Qué se descarga solo**: `<img src>`, `<link rel=stylesheet>`, `<script src>`, `<iframe src>` (otra página HTML ⇒ sus propios recursos), `<input type=image>`. **No**: `<a href>` (clic), `<form action>` (submit).
- ★ **Una conexión TCP por host** distinto (cada uno con su DNS previo). DNS = UDP, no cuenta como conexión TCP.
- Pixel de rastreo: `<img>` a `count.php?Email=...` ⇒ el servidor registra la apertura. `Content-Type` lo decide el servidor, no la extensión.

### MIME (mail vs HTTP)
- Mail: SMTP es ASCII 7 bits ⇒ binario en **base64**. Headers `MIME-Version`, `Content-Type` (qué es), `Content-Transfer-Encoding` (cómo está codificado). SMTP no se entera, decodifica el cliente.
- HTTP reusa los **tipos** MIME en `Content-Type`, pero el cuerpo va binario tal cual (sin base64 ni CTE).

### DNS: secuencias (ej. 7, 11)
- Tabla: # | de → a | consulta (recursiva/iterativa) | respuesta (referral NS+glue / aa A). PC→resolver recursiva; resolver→raíz→TLD→auth iterativas.
- Lo cacheado se reusa: la 2ª resolución en .com arranca del NS de com (salta la raíz).
- ★ **Zone file**: nombre sin punto final = relativo a la zona (`ads` en jmail.com = `ads.jmail.com`; `cdn.akamai.com` sin punto = `cdn.akamai.com.jmail.com`). Un servidor **no autoritativo** para un dominio no se consulta por él ⇒ esos registros no se usan.
- Mail masivo (ej. 10): **una consulta MX por dominio distinto**, no por destinatario. El A del MX suele venir en ADDITIONAL.

## Seguridad (Guía 7)

### Propiedades
Confidencialidad (solo B lee) · Integridad (no se modificó) · Autenticación (es A) · **No repudio** (A no puede negar; necesita algo que **solo A** pudo generar ⇒ firma con privada). No repudio ⇒ autenticación, no al revés. ★ **MAC no da no repudio** (B también tiene la clave).

### ★ Regla de claves
- **Mi privada** = probar que soy yo (firmar). **Pública del otro** = que solo él lea (cifrar).
- Simétrica (AES): rápida, problema = distribuir la clave (N(N−1)/2 claves). Asimétrica (RSA): lenta, resuelve distribución ⇒ en la práctica: **asimétrica para autenticar + acordar una simétrica de sesión**, después todo simétrico (híbrido).

### ★ Firma + cifrado (ej. 2)
- Firma: `F = E_{K−A}(H(M))`. Envío: `C = E_{K+B}(M + F)` (solo viaja C).
- B: (1) descifra C con K−B → M, F; (2) descifra F con K+A → digest; (3) calcula H(M) y **compara**. ★ El hash **no se invierte**, se recalcula.

### ★ MITM y certificados (ej. 3)
- Sin certificado: el atacante cambia las públicas en el intercambio y descifra/recifra en el medio.
- **Certificado X.509** = (sujeto, **clave pública del sujeto**, emisor, validez, nº de serie, algoritmos) + **firma de la CA**. Verificar: firma con **K+CA** (preinstalada en el SO/navegador = raíz de confianza), validez/fechas, nombre = el que quiero, no revocado (CRL/OCSP).
- Cadena: raíz → intermedia → servidor.

### Challenge-response y replay
- A manda un **nonce** fresco; B lo firma con K−B; A verifica con K+B ⇒ B tiene la privada. ★ Replay: reusar un mensaje viejo válido ⇒ meter nonce/timestamp **dentro** de lo firmado. Reflexión: devolverle el mismo desafío al que lo emitió.

### ★ SSH (ej. 5) y dónde vive cada clave
| | Cliente | Servidor |
|---|---|---|
| Clientes con claves (a) | su privada | N públicas en `authorized_keys` |
| Servidor (b) | K+S en `known_hosts` (1ª vez: fingerprint/**TOFU**, débil) | su privada |
| Con CA (c) | su par + Cert_C + **K+CA** | su par + Cert_S + **K+CA** |
- Con CA no se guardan públicas ajenas: el cert del otro llega en el handshake y se valida con K+CA ("una sola pública: la de la CA"). Revocar ⇒ CRL.

### ★ TLS 1.2 (ej. 4)
| Fase | Mensajes |
|---|---|
| HELLO | ClientHello (versión, cipher suites, **R_C**) · ServerHello (elige suite, **R_S**) |
| Key exchange | Certificate (Cert_S) · [CertificateRequest] · ServerHelloDone · ClientKeyExchange (**PMS cifrado con K+S**) · ChangeCipherSpec · Finished |
| Data | todo simétrico + MAC |
- `master = PRF(PMS, "master secret", R_C + R_S)`. Los **nonces R** hacen cada sesión distinta ⇒ anti-replay. Finished = MAC de todo el handshake (detecta manipulación).
- **TLS mutuo**: el servidor manda CertificateRequest; el cliente manda Certificate + **CertificateVerify** (firma del handshake con su privada). ★ Autenticar empleados con certs ⇒ TLS mutuo con la CA de la empresa (no user/pass).
- Capas: TLS sobre TCP (app); IPsec en red; WPA en enlace.

### Blockchain (teórica)
- Problema: **doble gasto** sin autoridad central. Ledger replicado de bloques; cada bloque lleva **hash del anterior** (cadena ⇒ cambiar uno rompe todos los siguientes) + raíz de **Merkle** de las transacciones (probar inclusión en O(log n)).
- **PoW**: encontrar nonce con H(bloque) < target (caro de hacer, barato de verificar). Cadena más larga (más trabajo) gana. **Ataque 51%**: con mayoría de cómputo reescribís historia. Confirmación ≈ esperar k bloques.
- PoS: peso por stake. BFT (permisionado): n ≥ 3f+1.
- Transacciones firmadas con la privada del dueño (dirección = hash de la pública).

## Arquitecturas (Guía 8)

### ★ Receta para ejercicios de diseño (ej. 1, 2, 4)
1. Supuestos. 2. Diagrama: cajas (componentes) + flechas (conectores).
3. **Por componente**: interfaz (operaciones) · procesamiento ("recibe X → hace Y → emite Z"; si lo saco, ¿qué decisión deja de pasar?) · datos · nivel (UI / procesamiento / datos).
4. **Por conector**: protocolo (REST, RPC, pub/sub, BD compartida) + acoplamiento. 5. Justificar cada decisión.

### Estilos y acoplamiento
- Estilos: **en capas** (cada capa usa la de abajo) · **objetos/servicios** (REST: recursos + verbos HTTP, stateless) · **pub/sub** (event-based) · **shared data space**.
- ★ Matriz: referencial = ¿el emisor conoce al receptor? · temporal = ¿tienen que estar vivos a la vez?

| | Temporal acoplado | Temporal desacoplado |
|---|---|---|
| **Ref. acoplado** | directa (RPC, HTTP) | mailbox / cola |
| **Ref. desacoplado** | event-based (pub/sub) | shared data space (BD, tuplas) |
- Pub/sub: por **topic** o por **contenido** (atributo-valor / atributo-rango; ★ el publicador manda **valores**, el **suscriptor** pone el rango; el middleware filtra). Notificar con dato vs aviso + ir a buscarlo. Lease en suscripciones.
- ★ Condición que combina dos eventos (A **y** B) ⇒ el middleware no la evalúa: alguien guarda estado ⇒ **controlador** que se suscribe, decide y publica comandos (regla en un solo lugar, actuadores tontos; costo: punto único ⇒ replicar). Suscribirse a **todo** el rango para enterarse también del "apagar" (ej. 4).

### Middleware: wrappers vs broker (ej. 5)
- Wrapper = adaptador de interfaz. Reemplazar C y D por E ⇒ 2 wrappers.
- N apps todos contra todos: **N(N−1)** wrappers. Con **broker**: **2N** (cada app ↔ formato común). Broker mejor desde N ≥ 4; agregar una app = O(1). Costo: punto central de falla / cuello.

### Cliente-servidor / físicas
- ★ **Idempotencia** (ej. 6): se pierde el OK sobre UDP ⇒ el cliente reintenta ⇒ **transferencia doble**. Solución: **ID de transacción** (el servidor detecta duplicado y re-responde). TCP no lo resuelve (la caída puede ser después de procesar y antes de responder: es de aplicación).
- Organizaciones 2-tier (a)→(e): corte entre UI / app / datos, de **thin** client (solo pantalla) a **fat** client (app + parte de datos local).
- ★ Validación (ej. 7): en el **cliente** (UX, menos viajes) **y** en el **servidor** (seguridad: el cliente se puede saltear). Multi-tier: UI / servidor de app / BD.
- Distribución **vertical** (por capas en distintas máquinas) vs **horizontal** (réplicas / particiones del mismo nivel).

### P2P
- **Overlay** = red lógica sobre la física (quién es vecino lógico de quién; un enlace lógico = varios saltos físicos).
- **Estructurado** (DHT, Chord: anillo + finger table, búsqueda **O(log N)**, hay que mantenerlo) vs **no estructurado** (vecinos al azar): **flooding** (a todos, TTL, `R(k)=d(d−1)^(k−1)` msgs en el salto k; rápido, robusto, carísimo) / **random walk** (a un vecino al azar, `S ≈ N/r` pasos con r réplicas; barato, lento, **no garantiza cubrir todo**). **Super peers**: jerarquía, índice central por grupo (punto débil si cae).
- ★ Ej. 8 (sensores 5 pisos): supuestos (BT llega al piso adyacente; un nodo del piso 1 con WiFi+BT = **gateway**) ⇒ overlay jerárquica: super peer por piso encadenados → AP. Recolección: pedido por el árbol **en paralelo** + **timeout** + **agregación** de vuelta. Anillo = N msgs exactos pero O(N) latencia; armarlo siguiendo la física.
- Ej. 9 (1 TB, 10000 piezas, 100 servidores, 10 vecinos): `T_pieza = (2h + 2)·RTT/2 + Ttx` con h = saltos de búsqueda. Clase (100 ms + 1 Gbps): flooding ≈ 3,5 h · RW ≈ 8,3 h · super peer ≈ 3,3 h. Guía: RTT 200 ms (mismo modelo).

### ★ Cloud / Fog / Edge (ej. 10)
- Latencias aprox: dispositivo ~0 · edge (AP / antena) 1–10 ms · fog (DC local) 10–50 ms · cloud 50–200 ms.
- **4 motivos para acercar al borde**: **latencia** (control en tiempo real) · **ancho de banda** (agregar/filtrar antes de subir) · **autonomía** (seguir sin Internet) · **regulación / privacidad** (datos no salen). Cloud = **vista global**, cómputo/almacenamiento masivo, sin latencia crítica.
- Tabla: componente | capa | procesa | datos | interfaces | por qué ahí. Autos/dispositivos entre sí: **directo (V2V broadcast)**, sin esperar al AP.
- Orquestación: decidir dónde corre cada servicio y moverlo (handoff entre celdas).

## Teórica extra (de `resumen-teorico.pdf`, elegir qué entra)
- **Aplicación**: HTTP **sin estado** (estado con cookies: Set-Cookie / Cookie / archivo en el host / BD del sitio; auth en cada pedido, 401 + WWW-Authenticate) · **CDN**: caches en los ISPs, usuario redirigido por **DNS** al más cercano · **DASH**: video por HTTP en segmentos, el cliente elige bitrate · TCP no da temporización ni BW mínimo; tiempo real ⇒ UDP · objeto = 2 RTT + Ttx · POP3 (baja) vs IMAP (queda en el servidor).
- **Seguridad**: 8 propiedades (+ originalidad, temporalidad, control de acceso, disponibilidad) · IPsec **AH** = integridad + autenticación (no cifra), **ESP** = confidencialidad · **Kerckhoffs**: algoritmo público, clave secreta · factor de trabajo exponencial en el largo de la clave · **OTP** inviolable (Shannon) pero impráctico (distribuir clave) · monoalfabética se rompe por frecuencias · DES 64 bits / 16 rondas, 3DES = E·D·E, AES mínimo hoy · **RSA**: n=pq, z=(p−1)(q−1), e coprimo con z, ed mod z = 1; c = m^e mod n, m = c^d mod n (ej. n=33, e=3, d=7) · hash: preimagen / 2ª preimagen / colisiones; MD5 y SHA-1 rotos · **reflexión**: reglas = inicia el que prueba primero, claves distintas por sentido, challenges de conjuntos distintos · **KDC**: A→KDC K_A(B,K_S); KDC→B K_B(A,K_S).
- **Blockchain**: firma no da orden/unicidad/acuerdo ⇒ doble gasto · **Sybil**: identidades gratis ⇒ votar con recurso escaso (PoW) · BFT n ≥ 3f+1 con identidades conocidas · dificultad cada 2016 bloques (~10 min) · gossip + forks transitorios (huérfanos) · PoW (abierta, probabilística, <50 %) / PoS (slashing, <1/3 stake) / PBFT (permisionada, inmediata, f<n/3) · Ethereum = SMR + smart contracts + gas · ★ conviene solo si muchos escriben sin confiar y no hay tercero aceptable; si no, BD replicada.
- **Distribuidos**: 3 rasgos (concurrencia, sin reloj global, fallas independientes; solo mensajes) · modelos: tiempo (sínc / parcialmente sínc / asínc), fallas (crash / crash-recovery / bizantina), canales (confiables / pérdidas equitativas / arbitrarios) · Amdahl p=0,95 ⇒ tope 20× · 10 000 servers MTBF 30 años ⇒ ~1 falla/día · **cola**: 1 − 0,99¹⁰⁰ ≈ 63 % · péndulo C↔D según costo de computar vs comunicar vs latencia · luz en fibra: **1 ms RTT ≈ 100 km** · latencias: nube 50–150, fog 5–20, edge 1–5, dispositivo < 1 ms · fog = jerarquía, edge = borde de acceso, cloudlet = DC en una caja · problemas: placement (NP-difícil), migración, consistencia entre niveles, autonomía (CRDTs) · cristal 20 ppm ≈ 1,7 s/día; NTP ms, PTP µs · TrueTime: deriva 200 µs/s, sincroniza cada 30 s.

## Teórica sin guía (cómputo distribuido)
- **Amdahl**: speedup = 1 / ((1−p) + p/n) ⇒ la parte serial limita.
- **8 falacias**: red confiable, latencia 0, BW infinito, red segura, topología fija, un administrador, costo de transporte 0, red homogénea.
- **Dos generales**: sin acuerdo garantizado sobre canal no confiable. **FLP**: asincrónico + 1 falla ⇒ no hay consenso determinístico garantizado. **CAP**: ante partición (P) elegir C o A. **PACELC**: si P → A o C; si no (Else) → Latencia o Consistencia.
- Replicación SMR (máquina de estados replicada: mismo orden de operaciones ⇒ mismo estado). Tolerar f fallas: crash **n ≥ 2f+1**, bizantinas **n ≥ 3f+1**. Quórums: **R + W > N** (lectura y escritura se solapan), W > N/2.
- Consistencia (fuerte → débil): linealizable > secuencial > causal > eventual.
- **Lamport**: (1) evento local: C++; (2) enviar: C++ y adjuntar C; (3) recibir: C = max(C, C_msg) + 1. a → b ⇒ C(a) < C(b), **no al revés** (concurrentes pueden tener cualquier orden). Orden total: desempatar por id de proceso.
- **Vectoriales**: V[i]++ local; al recibir, máximo componente a componente + V[i]++. a → b ⇔ V(a) < V(b) (todas ≤ y una <); si ninguno ≤ ⇒ **concurrentes**. Sí capturan causalidad.
- **TrueTime** (Spanner): `TT.now()` = intervalo [earliest, latest], ancho 2ε; ε ≈ 1 ms + deriva 0,2 ms/s desde la última sincronización (GPS + relojes atómicos), ~1–7 ms. **Commit wait**: timestamp s = TT.now().latest, esperar hasta TT.after(s) (≈ 2ε) antes de hacer visible ⇒ **consistencia externa** (si T1 termina antes de que empiece T2, s1 < s2).
