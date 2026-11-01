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
_pendiente_

## Seguridad (Guía 7)
_pendiente_

## Arquitecturas (Guía 8)
_pendiente_
