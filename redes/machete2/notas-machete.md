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
_(en progreso: ej. 1–5 hechos)_

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

## Seguridad (Guía 7)
_pendiente_

## Arquitecturas (Guía 8)
_pendiente_
