# Resumen teórico — Redes de Comunicaciones y Cómputo Distribuido (2C 2026)

Cubre las teóricas 03 → Transporte/TCP. Complementado con Peterson & Davie (*A Systems Approach*, 5ta) y Tanenbaum & Wetherall (5ta), que es la bibliografía que citan las clases (y la que se usó donde las diapos eran sólo figuras). Los agregados de los libros están marcados con 📖.

---

## 0. Marco general: capas

- **Paradigma de capas**: cada capa brinda servicios a la de arriba y usa los de abajo. Cada capa **encapsula**: agrega header (y a veces trailer) al mensaje de la capa superior.
- **OSI** (7): Física, Enlace, Red, Transporte, Sesión, Presentación, Aplicación. **TCP/IP** (Internet): Enlace/Físico, Red (IP), Transporte (TCP/UDP), Aplicación.
- Comunicación **par a par** (peer-layer): la capa N de A "habla" con la capa N de B mediante un protocolo; físicamente todo baja y sube por el stack.
- Los **routers** implementan hasta capa 3; transporte y aplicación son **end-to-end** (sólo en los hosts).

---

## 1. Nivel Físico — Parte 1: Fundamentos (señales)

- **Onda electromagnética**: campo E y B ortogonales. En vacío viaja a c = 3·10⁸ m/s; en otros medios a v < c (cobre UTP ≈ 0,69c; fibra ≈ 2/3 c).
- **Señal senoidal**: s(t) = A·sen(2πft + φ). A = amplitud, f = frecuencia (Hz), T = 1/f período, φ = fase, ω = 2πf.
- **Longitud de onda**: λ = v/f (distancia que ocupa un ciclo).
- **Fourier**: toda señal periódica se descompone en suma de senos/cosenos de frecuencias múltiplos de la fundamental f₀ = 1/T (armónicas). La onda cuadrada = fundamental + 1/3 de la 3ra + 1/5 de la 5ta + ... ⇒ una señal digital "perfecta" necesita **infinito ancho de banda**; al cortarla en frecuencia se deforma.
- **Dominio del tiempo vs. dominio de la frecuencia** (espectro): mismo objeto, otra representación; el filtrado se entiende mejor en frecuencia.
- **Ancho de banda (B)**: rango de frecuencias que el canal deja pasar sin atenuar demasiado. La frecuencia de corte se define a **−3 dB** (la potencia cae a la mitad). dB = 10·log₁₀(P₁/P₂).
- **Delay total** = T_prop + T_trans + T_encol + T_proc
  - T_prop = distancia / v → pesa en enlaces largos.
  - T_trans = tamaño trama / velocidad de TX → pesa en enlaces lentos o tramas grandes.
  - T_encol: depende de la congestión (de 0 a "gigante").
  - T_proc: μs o menos.

## 2. Teoría de la Información (Shannon, 1948)

- Idea central: el **significado** del mensaje es irrelevante para transmitirlo; importa su **estadística**. A más entropía, más esfuerzo para transmitir.
- Dos teoremas fundacionales: **codificación de fuente** (sin ruido: cuánto se puede comprimir) y **codificación de canal** (con ruido: cuánto se puede transmitir confiablemente).
- **Información** de un símbolo: I(sᵢ) = log₂(1/pᵢ) bits. Lo improbable informa más; lo seguro (p=1) informa 0.
- **Fuente de memoria nula**: símbolos independientes entre sí.
- **Entropía**: H(S) = Σ pᵢ·log₂(1/pᵢ). Es la información promedio por símbolo = incertidumbre promedio.
  - H ≥ 0; H = 0 sii un símbolo tiene p=1 (determinista).
  - Máxima cuando son equiprobables: H_max = log₂ n. Así, 0 ≤ H(S) ≤ log₂ K.
  - Fuente binaria: H(p) máxima (1 bit) en p = 0,5.
- **Codificación**: correspondencia símbolos de fuente → palabras de código. Clasificación: bloque, no singular, **unívocamente decodificable**, **instantáneo**.
  - **Condición de prefijo**: un código es instantáneo sii ninguna palabra es prefijo de otra.
  - Longitud media L = Σ pᵢ·Lᵢ. Código eficiente: palabras cortas a símbolos probables.
  - **Teorema de codificación de fuente**: L ≥ H (en binario). El **codificador óptimo** usa log₂(1/pᵢ) bits por símbolo; su longitud media coincide con la entropía.
  - **Huffman**: juntar repetidamente los dos menos probables en un árbol → código prefijo óptimo. (Ej. "MI MAMA ME MIMA": 33 bits vs 120 en ASCII de 8 bits.)
- **Perturbaciones del canal real** (limitado en potencia y ancho de banda, con ruido):
  - **Atenuación**: la señal cae con la distancia, más a altas frecuencias → ecualización.
  - **Distorsión de retardo** (medios guiados): cada frecuencia viaja a distinta velocidad → desfasajes.
  - **Ruido**: térmico (N₀ = kT, blanco, N = kTB), intermodulación (no linealidades, m·f₁ ± n·f₂), diafonía/crosstalk, impulsivo (picos cortos y grandes; el peor para datos).
- **BER** (Bit Error Rate): tasa de bits errados.
- **Nyquist** (canal **sin ruido**): C = 2B·log₂M bps (M = niveles de la señal). Baudio = símbolos/seg; C = V_baudios·log₂M.
- **Shannon** (canal **con ruido**): **C_max = B·log₂(1 + SNR)**, SNR como cociente de potencias (SNR_dB = 10·log₁₀ SNR).
  - Aumentar B aumenta el ruido (N = N₀B); aumentar S aumenta no linealidades. Hay un límite: con B → ∞ la capacidad satura (límite de Shannon, Eb/N₀ ≥ ln 2 ≈ −1,6 dB, el "0,693").
  - Teorema de canal: si la tasa R < C existe una codificación con probabilidad de error tan chica como se quiera; si R > C no ("zona verde" vs "zona roja"). No dice **cómo** construir el código.
  - En la práctica: Nyquist dice cuántos niveles "harían falta", Shannon pone el techo; la capacidad real es el mínimo.

## 3. Nivel Físico — Parte 2: medios, multiplexación, modulación

**Medios de transmisión**
- **Guiados**: par trenzado (el trenzado reduce diafonía), coaxial (CATV, 75 Ω), power line, **fibra óptica** (núcleo/revestimiento/cubierta; reflexión total interna; monomodo = largas distancias, multimodo = más barata y corta; inmune a interferencia EM).
- **No guiados**: radio, microondas, infrarrojo, láser, satélite, Li-Fi (datos por variaciones de brillo de LEDs, IEEE 802.15).

**Red telefónica (PSTN)** — conmutación de circuitos
- Local loop (par trenzado, analógico) + troncales (fibra/microondas, digitales) + oficinas de conmutación, en jerarquía redundante.
- **Multiplexación**: FDM (cada usuario una banda de frecuencia todo el tiempo), TDM (cada usuario todo el ancho de banda en turnos round-robin; sólo digital, se hace con electrónica digital), **WDM** (FDM en fibra, por longitud de onda). Ej.: radio AM usa FDM entre emisoras y TDM música/avisos.
- **Multiplexación estadística** (conmutación de paquetes): TDM "bajo demanda"; los paquetes compiten y se encolan; overflow del buffer = **congestión**.
- Taxonomía: redes de circuitos virtuales (orientadas a conexión: X.25, ATM) vs. datagramas (Internet, sin conexión). Transporte ofrece ambos sobre IP (TCP/UDP).

**Conversión A/D — PCM**
- **Teorema de muestreo (Nyquist)**: para reconstruir una señal de frecuencia máxima f_m hay que muestrear a **f_s > 2·f_m**. (CD: 44,1 kHz → hasta ~22 kHz; voz 4 kHz → 8000 muestras/s.)
- Dos etapas: **muestreo** (PAM) y **cuantificación** (n bits por muestra → error de cuantificación).
- Canal PCM de voz: 8000 muestras/s × 8 bits = **64 kbps**; período base 125 μs.
- **T1** (EE.UU./Japón): 24 canales × 8 + 1 bit de framing = 193 bits/125 μs = 1,544 Mbps. **E1** (Europa): 32 canales = 2,048 Mbps.
- Módem (digital↔analógico) ≠ Códec (analógico↔digital).

**Modulación** (variar amplitud, frecuencia o fase de una **portadora** según la **moduladora**)
- Analógica/analógica: AM, FM.
- **Digital/analógica** (módems): **ASK** (amplitud), **FSK** (frecuencia), **PSK** (fase), multinivel (QPSK = 4 fases, 2 bits/símbolo).
- **QAM**: combina amplitud y fase (dos portadoras I y Q a 90°). 16-QAM = 4 bits/símbolo, 64-QAM = 6, 256-QAM = 8. Se representa en la **constelación**.
- **V_t = V_m·log₂S** (bps = baudios × bits por símbolo).
- **El precio**: más puntos en la constelación ⇒ puntos más cercanos ⇒ el ruido los confunde ⇒ **más BER** para la misma SNR (por eso Shannon limita).
- Analógica/digital: PCM, modulación Delta (codifica diferencias).

**Codificación de línea** (digital/digital)
- **NRZ**: 1 = alto, 0 = bajo. Problema: secuencias largas sin cambios → se pierde el sincronismo (**clock recovery**) y la referencia (baseline wander 📖).
- **NRZI**: transición = 1, sin transición = 0. Arregla muchos 1s, no muchos 0s.
- **Manchester**: transición en el medio del bit (bajo→alto = 1, alto→bajo = 0). Se autosincroniza pero **baud rate = 2 × bit rate** (50% de eficiencia). Usado en Ethernet 10 Mbps.
- **Manchester diferencial**: 0 = transición al inicio del bit, 1 = sin transición al inicio (siempre hay transición en el medio).
- 📖 **4B/5B**: cada 4 bits → 5 bits con a lo sumo un 0 inicial y dos finales, y luego NRZI; eficiencia 80%.

## 4. Nivel de Enlace — Punto a punto

- Se tiene un "caño" serial (no desordena) pero con **errores**. Objetivos: servicio a la capa de red, confiabilidad, control de errores, (control de flujo).
- **Framing**: largo fijo, largo en el header, o **delimitadores** (flags) con **bit/byte stuffing**. Ej. PPP (flag 01111110; 📖 en HDLC tras cinco 1s seguidos se inserta un 0).
- **Tipos de servicio**: sin conexión y sin ACK / sin conexión con ACK / orientado a conexión.
- **Detección y corrección**: m bits de datos + r de redundancia = n (codeword). Con **d = distancia de Hamming mínima** del código:
  - detectar e errores: **d ≥ e + 1**
  - corregir e errores: **d ≥ 2e + 1**
  - 📖 Técnicas: paridad, checksum de Internet (suma en complemento a 1, usado en IP/TCP/UDP), **CRC** (división polinómica módulo 2; detecta todos los errores en ráfaga de longitud ≤ grado del polinomio; usado en Ethernet).
- **Retransmisiones** para confiabilidad (**ARQ**): implícitas (timeout) o explícitas (NACK).
- **Stop & Wait**: enviar 1 frame, esperar ACK. Problema de las **reencarnaciones** (duplicados si se pierde el ACK) → numerar; alcanza con **1 bit de secuencia** (2 números). Muy ineficiente en enlaces largos/rápidos.
- **Eficiencia**: η = T_tx(frame) / RTT(frame) (tiempo transmitiendo / tiempo esperando).
- **Capacidad de volumen**: C_vol = V_tx × Delay (bits "en el caño"). Para aprovecharlo hay que llenar hasta que vuelve el primer ACK → usar RTT (**producto delay × ancho de banda**).
- **Sliding Window**: mandar varios frames sin esperar ACK.
  - **SWS = V_tx·RTT / |Frame|** frames para mantener lleno el canal.
  - Se envía nuevo frame si ÚltimoFrameEnviado ≤ ÚltimoFrameReconocido + SWS.
  - **ACKs acumulativos** (Go-Back-N: el receptor no bufferea, RWS = 1; ante pérdida se reenvía desde ahí) vs. **ACKs selectivos**/NACK (Selective Repeat: RWS = SWS, se bufferea fuera de orden, sólo se reenvía lo perdido).
  - Para distinguir reencarnaciones: **#números de secuencia ≥ SWS + RWS**.

## 5. Nivel de Enlace — Medios compartidos (MAC)

- Compartir un medio: TDM/FDM/WDM/CDMA (estático) o **contención estadística** (los conflictos se aceptan o se manejan). Control **descentralizado** ⇒ hace falta direccionamiento y control de acceso.
- Objetivos de un protocolo MAC: maximizar éxitos en promedio y **fairness** promedio.
- **ALOHA** (Hawaii, 1970): transmitir cuando sea; si no hay ACK, esperar al azar y reintentar. Goodput máx ≈ **18%** (G = 0,5). 📖 Slotted ALOHA: 37% (G = 1).
- **CSMA** (Carrier Sense): escuchar antes de hablar. Si está ocupado: **1-persistente** (espera a que se libere y transmite ya; Ethernet) o **p-persistente** (transmite con probabilidad p).
- **CSMA/CD** (Ethernet, IEEE 802.3): además detecta colisión mientras transmite → corta, manda **jam** y hace backoff.
  - **Largo mínimo de trama**: hay que seguir transmitiendo hasta *saber* que no hubo colisión, es decir **2·T_prop** (peor caso: A y B en los extremos). Ethernet 10 Mbps: 512 bits = 64 bytes (51,2 μs); limita el largo máximo de la red (2500 m, 4 repetidores, 500 m por tramo).
  - **Exponential backoff**: tras la k-ésima colisión, elegir un slot al azar en [0, 2ᵏ − 1] y esperar slot × RTT (📖 k tope 10, abandonar a las 16).
  - Estados: Idle → Sense → Transmit → (Collision → Jam → Wait backoff → Sense).
  - Frame: preámbulo 8 B | dst 6 | src 6 | tipo/largo 2 | datos 46–1500 | CRC 4.
  - CSMA escala mal con la carga G.
- **IEEE 802.2 LLC**: subcapa sobre las MAC (802.3, 802.11...) que ofrece los 3 tipos de servicio y abstrae el medio.
- **Dominios**: **colisión** (lo separa un bridge/switch, no un hub) vs. **broadcast** (lo separa un router o VLAN).
- **Dispositivos por capa**: físico = repetidores/hubs; enlace = bridges/switches; red = routers.
- **LAN extendida / Learning bridges**: el bridge aprende MAC origen → puerto; reenvía sólo donde hace falta (filtra); si no sabe, **inunda**; broadcast siempre se inunda. La tabla es una optimización.
- **Ciclos** (bridges redundantes) ⇒ los frames circulan para siempre ⇒ **Spanning Tree Protocol** (STP, 802.1D, Radia Perlman):
  - Se elige **root** (menor ID). Cada switch calcula su distancia al root; su **root port** = puerto con menor distancia al root. Por cada LAN, un **designated port** (el de menor distancia al root entre los switches de esa LAN). El resto: **bloqueado**.
  - Se intercambian **BPDUs** [mi id, quién creo que es el root, mi distancia] periódicamente; si dejan de llegar, se recalcula.
- **"El broadcast no escala"** → **VLANs**: particionan lógicamente una LAN física en varias (cada una un dominio de broadcast). **Trunking 802.1Q**: tag de 4 bytes en el frame con el VLAN ID (12 bits) y prioridad.
- **Wireless (802.11)**: más ruido y errores, energía, seguridad (eavesdropping → cifrar). Bandas licenciadas (ENACOM/FCC) vs. **no licenciadas ISM/U-NII** (potencia limitada → más interferencia) → **spread spectrum** (FHSS: Hedy Lamarr; 📖 DSSS).
  - **Estación oculta**: A→B, C no oye a A, transmite y colisiona en B.
  - **Estación expuesta**: B→A, C oye a B y no transmite a D aunque podría.
  - No se puede hacer CD (no se escucha mientras se transmite; y la colisión importa en el receptor) → **CSMA/CA**: sensar; si libre esperar **IFS**; si ocupado esperar al fin + **backoff** aleatorio en la ventana de contención (CW, en slots; el contador se congela si el medio se ocupa); se espera **ACK**, sin ACK se asume colisión y se retransmite. 📖 Opcional **RTS/CTS** para atacar la estación oculta (quienes oyen el CTS se callan).

## 6. Nivel de Red — Conmutación, datagramas y circuitos virtuales

- **Switch** (genérico): dispositivo multi-entrada/multi-salida que hace **forwarding** mirando la dirección/identificador del header. Permite redes escalables (cubrir más área, más nodos; agregar un host no necesariamente carga la red).
- **Conmutación de circuitos** vs. **de paquetes**: temporización de eventos (establecimiento de llamada vs. paquetes de VC vs. datagramas, el más usado).
- **Datagramas** (sin conexión, "sistema postal"): cada paquete lleva la dirección completa y se rutea independientemente. Sin fase de setup (no se espera un RTT), robusto a fallas (se cambia el camino), pero más overhead por paquete y QoS/congestión difíciles.
- **Circuito virtual** (orientado a conexión, "llamada telefónica"): fase de setup (1 RTT) y de fin. Tabla de VC en cada switch: (puerto entrada, **VCI** entrada) → (puerto salida, VCI salida) — *label switching*; el VCI tiene significado local. Poco overhead por paquete (sólo el VCI), permite **reservar recursos** (QoS fácil), pero si cae un switch caen sus VCs. **PVC** (lo arma el administrador) vs. **SVC** (por señalización). Ej.: X.25, Frame Relay, ATM (📖 hoy MPLS).

## 7. Nivel de Red — IP

- **Internetworking**: IP interconecta redes heterogéneas (Ethernet, FDDI, PPP...); los routers corren IP sobre la tecnología de cada enlace.
- **Modelo de servicio best-effort**, sin conexión: los paquetes se pueden perder, desordenar, duplicar y demorar sin cota. Filosofía: red simple, inteligencia en los extremos.
- **Header IPv4** (20 B mínimo, hasta 60 con opciones): Versión, HLen (en palabras de 32 bits, 5–15), TOS → DiffServ/ECN, Longitud total (≤ 65535), Ident/Flags(DF, MF)/Offset (fragmentación), **TTL** (contador de saltos, se descarta en 0; evita loops eternos), **Protocol** (1 ICMP, 6 TCP, 17 UDP, 89 OSPF), Checksum (**sólo del header**), IP origen y destino (32 bits).
- **Fragmentación**: cada enlace tiene un **MTU** (Ethernet 1500, FDDI 4500). Si el datagrama > MTU, el router fragmenta; **se reensambla sólo en el destino**. Fragmentos: mismo Ident, MF = 1 salvo el último, offset en unidades de **8 bytes**. IP no recupera fragmentos perdidos (se pierde todo el datagrama). Todo enlace debe aceptar ≥ 68 bytes. (📖 hoy se prefiere Path MTU Discovery con DF=1.)
- **Direccionamiento**: 32 bits (~4300 M), globalmente único y **jerárquico (red + host)**. Notación dot. Esquema **classful** original A/B/C → problemas de escalabilidad (desperdicio, tablas enormes) → 📖 subnetting y **CIDR** (prefijos /n arbitrarios, agregación de rutas, *longest prefix match*). Ej.: UBA 157.92/16.
- **Direcciones privadas** (RFC 1918): 10/8, 172.16/12, 192.168/16 — no ruteables en Internet (📖 se usan con NAT).
- **Forwarding IP**: si la red destino es una de mis interfaces → entrega directa; si está en la forwarding table → al next hop; si no → **default router**. Un host común sólo tiene "mi red" o "default router". (📖 La entrega directa necesita la MAC del destino → **ARP**; los errores se reportan con **ICMP**, p. ej. TTL expirado → traceroute.)
- **IPv6**: 128 bits (2¹²⁸ direcciones), notación hex con ":". Header fijo de 40 B simplificado (sin checksum, sin fragmentación en routers, opciones como extension headers).

## 8. Nivel de Red — Ruteo

- **Forwarding** (elegir puerto de salida con la tabla; rápido, en el plano de datos) vs. **Routing** (construir/actualizar las tablas; algoritmo distribuido, plano de control). Tabla de ruteo (destino → ruta, lógica) vs. tabla de forwarding (destino → interfaz/MAC).
- Ruteo = problema de grafos: camino de menor costo entre nodos, en tiempos razonables y con pocos recursos. **Estático** (manual) vs. **dinámico** (se adapta a fallas y carga).
- **Sistemas Autónomos (AS)**: dominio bajo una administración. Ruteo **intradominio / IGP** (RIP, OSPF) vs. **interdominio** (EGP, BGP). Idea: autonomía y heterogeneidad; lo interno queda oculto.

**Vector de distancia (Distance Vector)** — Bellman-Ford distribuido
- Cada nodo guarda (Destino, Costo, NextHop) hacia **todos**; manda **su tabla entera** (Destino, Costo) **sólo a sus vecinos**, periódicamente y ante cambios (*triggered update*).
- Actualiza si recibe un camino más barato: D(x,y) = min_v { c(x,v) + D_v(y) }. Borra rutas por timeout.
- Buenas noticias viajan rápido; malas lento → **conteo a infinito** (A y C se "creen" mutuamente tras caer un enlace).
- Heurísticas: **infinito = 16**; **split horizon** (no anunciar una ruta al vecino por el que se aprendió); **split horizon con poison reverse** (anunciarla con costo ∞). Sólo resuelven ciclos de 2 nodos.
- **RIP**: DV con costo = hops (1–15; 16 = ∞ → redes chicas), sobre **UDP puerto 520**, corre como daemon (routed), updates cada ~30 s.

**Estado de enlace (Link State)** — Dijkstra
- Cada nodo: descubrir vecinos → medir costos → armar un **LSP** (ID, costo a cada vecino, **SEQNO**, **TTL**) → **inundarlo a toda la red** → correr Dijkstra.
- **Inundación confiable**: guardar el LSP más reciente de cada nodo (por SEQNO), reenviar a todos menos a quien lo mandó, con ACKs, TTL que decrece y descarta en 0, LSP nuevo periódico, SEQNO desde 0 al reiniciar.
- **Dijkstra / forward search**: listas *Tentativo* y *Confirmado* con (Dest, Costo, NextHop). Se confirma el tentativo de menor costo y se miran sus LSPs para actualizar.
- Comparación: DV = cada nodo le cuenta a sus vecinos **todo lo que sabe de la red**; puede ser inestable. LS = cada nodo le cuenta a **toda la red** sólo **lo de sus vecinos**; estable, responde rápido, poco tráfico, pero más memoria/CPU (un LSP por nodo) y todos tienen visión consistente.
- **Métricas**: ARPANET original = largo de cola (ignora latencia y ancho de banda); nueva = retardo medido [(DT − AT) + Transmit + Latency] promediado → oscilaciones; revisada = utilización del enlace con rango dinámico acotado.
- **OSPF**: LS abierto, directamente **sobre IP** (protocolo 89). Mensajes **autenticados**, **múltiples caminos de igual costo** (balanceo), varias métricas por **ToS**, multicast (MOSPF). **Jerárquico**: áreas + área **troncal (backbone, área 0)**; los LSAs sólo se inundan dentro del área; los routers de frontera de área resumen distancias. **Se cambia optimalidad por escalabilidad** (ocultar información). Mensajes: Hello, Database Description, LS Request, LS Update, LS Ack (los tres del medio se confirman).

**Interdominio**
- **EGP**: para Internet en árbol; alcanzabilidad sin optimizar; adquisición de vecinos, HELLO/ACK, intercambio tipo DV.
- **BGP**: no requiere árbol. Tipos de AS: **stub** (una conexión, sólo tráfico local), **multihomed** (varias conexiones, no deja pasar tránsito), **transit** (lleva tráfico local y de tránsito). Cada AS tiene routers de borde y un **speaker BGP** que publica redes alcanzables y el **camino de ASs** completo (**path vector**, 📖 que permite detectar loops y aplicar **políticas**, no sólo "el más corto"). Puede retirar rutas. 📖 Corre sobre TCP (puerto 179).
- **NAPs / IXPs**: puntos de intercambio de tráfico entre redes (en Argentina, CABASE con modelo cooperativo): bajan costos y mejoran la calidad (el tráfico local no sale al exterior).

## 9. Nivel de Transporte — TCP y UDP

**Por qué transporte ≠ enlace** (aunque ambos hagan ventana deslizante): conecta muchas máquinas distintas (setup/fin explícito), RTTs distintos y variables (timeouts adaptativos), largos retardos (paquetes muy viejos pueden aparecer), receptores de distinta capacidad (control de flujo), red con capacidad variable (**control de congestión**).
- IP descarta, desordena, duplica, limita el tamaño y demora. Servicios que se desean end-to-end: entrega garantizada, en orden, a lo sumo una copia, mensajes arbitrariamente largos, sincronización, control de flujo, múltiples procesos por host (**puertos**).

**UDP**: sin conexión, no confiable. Sólo agrega **demultiplexación por puertos** y checksum opcional (📖 header de 8 B: src port, dst port, length, checksum). Se usa cuando importa la latencia más que la confiabilidad (RTP, DNS, RIP...).

**TCP** — características
- Orientado a conexión, **full duplex**, **flujo de bytes** (la app escribe bytes, TCP arma segmentos, la app lee bytes; no se preservan los límites de los mensajes).
- Confiable: ACKs, checksums, números de secuencia, retransmisión por timeout, reordenamiento.
- **Control de flujo** (no inundar al receptor) y **control de congestión** (no inundar la red).
- Conexión identificada por la **4-tupla** (IP origen, puerto origen, IP destino, puerto destino).
- **MSS**: tamaño máximo de datos por segmento (default 536; con Ethernet 1500 − 20 IP − 20 TCP = 1460).
- Un segmento se envía cuando: se junta un MSS, vence un timer, o la aplicación hace **push**.
- **Header** (20 B + opciones): SrcPort, DstPort, **SequenceNum** (32 bits, número del **primer byte** del segmento), **Acknowledgment** (32 bits, **próximo byte esperado**, acumulativo), HdrLen, flags **URG, ACK, PSH, RST, SYN, FIN**, **AdvertisedWindow** (16 bits), Checksum (**pseudo-header IP** + header + datos), UrgPtr, opciones.
- Números de secuencia desde un **ISN** (📖 aleatorio, para no confundir con conexiones viejas).

**Conexión**
- Establecimiento: **3-way handshake** SYN → SYN+ACK → ACK (cliente activo, servidor pasivo). 📖 Cada lado anuncia su ISN; el SYN "consume" un número de secuencia.
- Liberación: **4-way** (FIN, ACK, FIN, ACK) — cada dirección se cierra por separado (half-close).
- **Máquina de estados**: CLOSED, LISTEN, SYN_RCVD, SYN_SENT, ESTABLISHED, FIN_WAIT_1, FIN_WAIT_2, **TIME_WAIT**, CLOSING, CLOSE_WAIT, LAST_ACK. Eventos: llamadas de la app (LISTEN, CONNECT, SEND, CLOSE) o segmentos (SYN, ACK, FIN, RST). **TIME_WAIT** espera **2·MSL** (doble del tiempo de vida máximo de un paquete) para que mueran los segmentos viejos y poder reenviar el último ACK si se pierde.
- Primitivas de sockets Berkeley: socket, bind, listen, accept, connect, send, recv, close.

**Ventana deslizante y control de flujo**
- Variante del sliding window de enlace; retransmisión estilo **Go-Back-N** con ACK acumulativo (📖 extensión SACK, RFC 2018).
- Emisor: LastByteAcked ≤ LastByteSent ≤ LastByteWritten. Receptor: LastByteRead < NextByteExpected ≤ LastByteRcvd + 1 (si hay huecos, NextByteExpected apunta al hueco).
- **AdvertisedWindow = MaxRcvBuffer − (LastByteRcvd − LastByteRead)**
- **EffectiveWindow = AdvertisedWindow − (LastByteSent − LastByteAcked)**
- El emisor bloquea a la app si el buffer de envío se llena. Si AdvertisedWindow = 0, el emisor **persiste**: manda **window probes** de 1 byte periódicamente (**persist timer**), porque el ACK que reabre la ventana podría perderse y quedarían los dos esperando (deadlock).

**Retransmisión adaptativa (RTO)**
- El RTT en TCP es muy variable (congestión, cambios de ruta), a diferencia del enlace → timeout adaptativo (lazo cerrado).
- **Original (RFC 793)**: EstRTT = α·EstRTT + (1−α)·SampleRTT (α 0,8–0,9); TimeOut = 2·EstRTT.
- **Karn/Partridge**: **no medir el RTT de segmentos retransmitidos** (ambigüedad: ¿el ACK es del original o de la retransmisión?) y **duplicar el timeout** en cada retransmisión (exponential backoff).
- **Jacobson/Karels**: considerar la **varianza**. Diff = Sample − EstRTT; EstRTT += δ·Diff; Dev += δ·(|Diff| − Dev); **TimeOut = μ·EstRTT + φ·Dev** con μ = 1, φ = 4.
- **RFC 6298**: SRTT y RTTVAR. Primera medición R: SRTT = R, RTTVAR = R/2. Luego: RTTVAR = (1−β)·RTTVAR + β·|SRTT − R'| (**primero**, con el SRTT viejo), SRTT = (1−α)·SRTT + α·R' (α = 1/8, β = 1/4). **RTO = SRTT + max(G, 4·RTTVAR)**, redondeado a ≥ 1 s; antes de medir, RTO = 1 s.
- Los algoritmos dependen de la granularidad del reloj; un buen timeout es clave para la congestión y para no retransmitir de más.

**Ineficiencias con segmentos chicos**
- Ej. telnet: 1 carácter tipeado → 162 bytes y 4 segmentos (dato, ACK, actualización de ventana, eco).
- Receptor: **delayed ACK**.
- **Algoritmo de Nagle** (emisor): si hay ≥ MSS para enviar y la ventana lo permite, mandar un segmento lleno; si no, y hay datos en vuelo sin ACK, bufferear hasta que llegue el ACK; si no hay nada en vuelo, mandar ya. (Autoajustable: a lo sumo un segmento chico en vuelo por RTT.) 📖 Se desactiva con TCP_NODELAY en apps interactivas.
- **Silly Window Syndrome** (receptor que lee de a 1 byte → anuncia ventanas de 1 byte → segmentos de 1 byte). **Solución de Clark**: no anunciar ventanas chicas; esperar a tener libre min(MSS, buffer/2).

**Uso del ancho de banda — "mantener el caño lleno"**
- Para usar todo el enlace, la ventana tiene que ser ≥ **delay × bandwidth** (RTT × ancho de banda). Si la ventana < RTT·BW, el emisor queda ocioso esperando ACKs.
- AdvertisedWindow de 16 bits ⇒ máximo **64 KB**: alcanza para T1 (18 KB con RTT 100 ms) pero no para Ethernet de 10 Mbps (122 KB) en adelante. 📖 Solución: opción **window scale** (RFC 1323), que además agrega **timestamps** (mejor medición de RTT y PAWS contra el *wraparound* de los números de secuencia de 32 bits en enlaces rápidos).
- (El **control de congestión** — slow start, AIMD, etc. — se anuncia para una clase aparte.)

---

## Preguntas teóricas "clásicas" para repasar

1. ¿Qué diferencia hay entre el límite de Nyquist y el de Shannon? ¿Por qué no se puede aumentar indefinidamente la cantidad de niveles de una modulación?
2. ¿Qué es la entropía y qué relación tiene con la longitud media de un código óptimo (Huffman)?
3. ¿Por qué Manchester duplica el baud rate? ¿Qué problema resuelve respecto de NRZ?
4. ¿Por qué Stop & Wait es ineficiente? ¿Cómo se dimensiona la ventana? ¿Cuántos números de secuencia hacen falta?
5. ¿Por qué Ethernet tiene un tamaño mínimo de trama? ¿Qué pasa con ese mínimo si aumento la velocidad?
6. ¿Por qué en wireless se usa CSMA/CA y no CSMA/CD? Estación oculta vs. expuesta.
7. ¿Para qué sirve STP? ¿Cómo elige root, root ports y designated ports?
8. Dominio de colisión vs. de broadcast; ¿qué los separa? ¿Para qué sirven las VLANs?
9. Datagramas vs. circuitos virtuales: ventajas y desventajas.
10. Fragmentación IP: dónde se fragmenta, dónde se reensambla, qué campos intervienen.
11. Distance Vector vs. Link State; conteo a infinito y sus heurísticas.
12. ¿Por qué OSPF es jerárquico? ¿Qué se pierde?
13. ¿Por qué hace falta BGP además de un IGP? Tipos de AS.
14. ¿En qué se diferencia la ventana deslizante de TCP de la de enlace? Control de flujo vs. congestión.
15. ¿Por qué el RTO es adaptativo? Karn/Partridge y Jacobson/Karels.
16. Nagle vs. Silly Window: ¿de qué lado actúa cada uno y qué resuelven?
17. ¿Por qué el AdvertisedWindow de 16 bits es un problema en redes rápidas?
18. ¿Para qué sirve TIME_WAIT? ¿Y el persist timer?
