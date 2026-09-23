# Guía 1 — Transmisión confiable de información

*Redes de Comunicaciones y Cómputo Distribuido — FCEN, UBA*

hecha por mí, formateada por mi brother Sonnet o Luna o quien me re pinte

## Ejercicio 1

### a)

$$H(p_0) = p_0 \log_2\frac{1}{p_0} + (1-p_0)\log_2\frac{1}{1-p_0} = -p_0\log_2 p_0 - (1-p_0)\log_2(1-p_0)$$

### b)

![Gráfico de H(p0): curva simétrica, 0 en los extremos y máximo en p0 = 0.5](image.png)

### c)

Es bastante directo: si ambos símbolos tienen la misma probabilidad (p₀ = 0.5), ahí está el $H_{max}$.

## Ejercicio 2

*Resuelto en clase — mismo enunciado que la Práctica 1, Ejercicio 1.*

## Ejercicio 3

Es fácil ver que, cuando $N$ es potencia de 2, todos los símbolos quedan con la misma longitud y por lo tanto $L(C) = H(S)$. Como los símbolos son equiprobables, $H(S) = \log_2(N)$ siempre, con $N$ = cantidad de símbolos.

Si $N$ no es potencia de 2, armás el Huffman a ojo y contás cuántos símbolos quedan con cada longitud.

- **a)** $H(S) = L(C) = \log_2(2) = 1$ bit

- **b)** $H(S) = L(C) = \log_2(4) = 2$ bits

- **c)** 6 no es potencia de 2 → quedan 2 símbolos con 2 bits y 4 símbolos con 3 bits.

  $H(S) = \log_2(6) = 2.585$ bits, pero $L(C) = \dfrac{2\cdot2 + 4\cdot3}{6} = 2.667$ bits.

- **d)** $H(S) = L(C) = \log_2(8) = 3$ bits

- **e)** 10 no es potencia de 2 → quedan 6 símbolos con 3 bits y 4 símbolos con 4 bits.

  $H(S) = \log_2(10) = 3.322$ bits, pero $L(C) = \dfrac{6\cdot3 + 4\cdot4}{10} = 3.4$ bits.

- **f)** $H(S) = \log_2(N)$, siempre.

  Para $L(C)$: si $N$ es potencia de 2, $L(C) = \log_2(N)$.
  Si no, con $k = \lfloor \log_2 N \rfloor$ y $m = N - 2^k$ (los símbolos "que sobran"), quedan $2m$ símbolos de largo $k+1$ y $2^k - m$ símbolos de largo $k$.

## Ejercicio 4

### 1.

No, a ojo. No es equiprobable porque $b_1, \dots, b_m$ tienen probabilidad $1/32$ de salir, y los $a$ tienen $1/16$.

### 2.

No, tampoco. Tienen la misma cantidad de símbolos en cada lado, pero las probabilidades generales no son equitativas.

### 3.

Tampoco. No me dan las cuentas, pero cada símbolo de $a$ tiene probabilidad $1/32$ y cada símbolo de $b$ tiene $3/64$ (creo).

### 4.

Este, finalmente, sí. La probabilidad para cualquier componente de $A$ es $2/96$, es decir, $1/48$, y la de $b$ también es $1/48$.

## Ejercicio 5, 6

Hecho en clase.

## Ejercicio 7

### a)

La velocidad de transmisión es $V_{tx}=100$ Mbps, por lo que el tiempo de
transmisión de un bit es:

$$T_{tx}(1)=\frac{1}{100\cdot10^6}=10\ \text{ns}$$

El tiempo de propagación es:

$$T_{prop}=\frac{D}{V_{prop}}=\frac{385000\ \text{km}}{300000\ \text{km/s}}
\approx 1.2833\ \text{s}$$

Por lo tanto:

$$Delay(1)=T_{tx}(1)+T_{prop}\approx 1.2833\ \text{s}$$

$$RTT=2\cdot Delay(1)\approx 2.5667\ \text{s}$$

### b)

La capacidad de volumen es:

$$C_{vol}=Delay(1)\cdot V_{tx}$$

$$C_{vol}\approx 1.2833\cdot100\cdot10^6
\approx 128.33\ \text{Mbit}$$

Es decir, entran aproximadamente **128,33 millones de bits** simultáneamente
en el canal.

### c)

El tiempo de transmisión del pedido de 2 kbit es:

$$T_{tx,pedido}=\frac{2000}{100\cdot10^6}=20\ \mu\text{s}$$

El tiempo de transmisión de la imagen de 25 Mbit es:

$$T_{tx,imagen}=\frac{25\cdot10^6}{100\cdot10^6}=0.25\ \text{s}$$

Desde que se inicia el pedido hasta que termina de recibirse la imagen
transcurren:

$$T=T_{tx,pedido}+T_{prop}+T_{tx,imagen}+T_{prop}$$

$$T\approx0.00002+1.2833+0.25+1.2833
\approx 2.8167\ \text{s}$$

El tiempo mínimo es, entonces, aproximadamente **2,817 segundos**.


## Ejercicio 8, 9, 10 
hechos en clase

## Ejercicio 11

*Convención (ver diapo "Recordatorio" de ptoapto.pdf): el "delay" dado en el enunciado (0.25 s) es $T_{prop}$, no $Delay(Frame)$ — salvo que se diga lo contrario. $Delay(Frame) = T_{tx}(Frame) + T_{prop}$ y $RTT(Frame) = 2\cdot Delay(Frame)$.*

Datos reales por frame: es Stop & Wait de largo fijo, con CRC de 16 bits. Para distinguir 2 frames consecutivos ($SWS=RWS=1$, $\#frames \ge 2$) alcanza con **1 bit de SEQ**. Entonces:

$$|Datos| = 2000 - 16 - 1 = 1983\ \text{bits}$$

Para mandar 20 Mbit de datos:

$$\#frames = \left\lceil\frac{20\cdot10^6}{1983}\right\rceil = 10086\ \text{frames}$$

### a)

$$T_{tx}(Frame) = \frac{2000}{1\cdot10^6} = 2\ \text{ms}$$

$$Delay(Frame) = T_{tx}(Frame) + T_{prop} = 0.002 + 0.25 = 0.252\ \text{s}$$

$$RTT(Frame) = 2\cdot Delay(Frame) = 0.504\ \text{s}$$

Como es Stop & Wait, cada frame necesita su ciclo completo de ida y vuelta antes de mandar el siguiente:

$$T_{total} = 10086 \cdot 0.504 \approx 5083.3\ \text{s} \approx \mathbf{84.7\ minutos}$$

### b)

Mismo delay (0.25 s), ahora con $V_{tx}=1$ Gbps:

$$T_{tx}(Frame) = \frac{2000}{1\cdot10^9} = 2\ \mu\text{s}$$

$$Delay(Frame) = 0.000002 + 0.25 = 0.250002\ \text{s} \qquad RTT(Frame) \approx 0.500004\ \text{s}$$

$$T_{total} = 10086 \cdot 0.500004 \approx 5043.0\ \text{s} \approx \mathbf{84.05\ minutos}$$

Casi no cambia respecto de (a): al ser $T_{prop}$ tan dominante frente a $T_{tx}$, aumentar 1000x la velocidad de transmisión apenas mejora el tiempo total.

### c)

Mismo $V_{tx}=1$ Mbps, ahora con delay $=0.1$ s ($T_{prop}=0.1$ s):

$$Delay(Frame) = 0.002 + 0.1 = 0.102\ \text{s} \qquad RTT(Frame) = 0.204\ \text{s}$$

$$T_{total} = 10086 \cdot 0.204 \approx 2057.5\ \text{s} \approx \mathbf{34.3\ minutos}$$

Acá sí baja bastante más, porque ahora $T_{tx}$ representa una fracción mayor de $T_{prop}$ y el $RTT$ se achica en serio (de 0.504s a 0.204s).

## Ejercicio 12

*Misma convención que en el Ejercicio 11: delay dado (0.25 s) $= T_{prop}$.*

### a)

Usamos GoBackN, así que $RWS=1$ siempre. $SWS = V_{tx}\cdot RTT(Frame)/|Frame|$, con $RTT(Frame)=2\cdot Delay(Frame)$ (no alcanza con usar $Delay(Frame)$ solo, hay que duplicarlo).

$$Delay(Frame) = T_{tx}(Frame) + T_{prop} = 0.002 + 0.25 = 0.252\ \text{s}$$

$$RTT(Frame) = 2\cdot 0.252 = 0.504\ \text{s}$$

$$SWS = \frac{1\cdot10^6 \cdot 0.504}{2000} = 252 \qquad RWS = 1$$

### b)

$$\#frames \ge SWS + RWS = 253$$

$$\#SEQ = \lceil \log_2(253) \rceil = \lceil 7.98 \rceil = \mathbf{8\ bits}$$

### c)

Datos reales por frame: $2000 - 8\ (\#SEQ) - 16\ (CRC) = 1976$ bits.

$$\#frames = \left\lceil\frac{20\cdot10^6}{1976}\right\rceil = 10122\ \text{frames}$$

Como $SWS$ está óptimamente dimensionado, el emisor mantiene el canal siempre ocupado sin frenar a esperar ACKs (a diferencia de Stop & Wait). Entonces el tiempo total no es "frames × delay por frame", sino simplemente el tiempo de transmitir todos los bits (con overhead incluido) más un único $T_{prop}$ final:

$$T_{total} = \frac{|Frame|\cdot\#frames}{V_{tx}} + T_{prop} = \frac{2000\cdot10122}{1\cdot10^6} + 0.25 = 20.244 + 0.25 \approx \mathbf{20.5\ segundos}$$

Tiene sentido que sea órdenes de magnitud más rápido que el Stop & Wait del Ejercicio 11 (~85 min): esa es justamente la ventaja de la ventana deslizante, mantener el caño lleno en vez de esperar el RTT completo por cada frame.

## Ejercicio 13

### a)

La eficiencia digamos

$$e(|Frame|) = \frac{|Datos|}{|Frame|}$$
$$|Datos| = |Frame| - CRC/Checksum/Whatever\ (c) - \#SEQ$$

como la función es en base al tamaño del frame, tomo CRC, Checksum y demas como una constante C. 
llamo, por conveniencia, LF al tamaño del frame. entonces

$$e(LF) = \frac{LF - C - \#SEQ}{LF}$$

#SEQ igual tambien se calcula en base a LF, asi que podemos expandir más la ecuación.

#SEQ es ceil del log2 de sws + rws. en este caso es Selective ack asi que RWS y SWS son iguales. SWS sería V_tx * RTT(Frame) / |Frame|

V_tx y Delay son consideradas constantes segun la conigna, entonces no me joden mucho. El T_tx es |Frame|/V_tx que es constante asi q entra bien en la ecuacion. con eso, RTT = 2 * Delay(f) = 2 * (|Frame|/V_tx + D (constante))

Dando toda la vuelta, 
$$ SWS(LF) = \frac{V_{tx} \:\cdot\: 2\cdot(LF/V_{tx} + D )}{LF} $$
Vease
$$  SWS(LF) = \frac{2\cdot(LF + D \: \cdot \: V_{tx})}{LF} $$

Entonces de ahí

$$ \#SEQ = \lceil \log_{2}{(SWS  + RWS)} \rceil $$
$$ \#SEQ = \lceil \log_{2}{(2 \: \cdot \: \frac{2\cdot(LF + D \: \cdot \: V_{tx})}{LF})} \rceil = \lceil \log_{2}{(\frac{4\cdot(LF + D \: \cdot \: V_{tx})}{LF})} \rceil $$

Entonces la función, completa, queda

$$e(LF) = \frac{LF - C - \lceil \log_{2}{(\frac{4\cdot(LF + D \: \cdot \: V_{tx})}{LF})} \rceil}{LF}$$

Creo!

### b)

imaginate que lo grafique. 

## Ejercicio 14

Bajemos variables:

$$|Frame| = 1\ \text{kbit} \qquad T_{prop} = 270\ \text{ms} \qquad V_{tx} = 1\ \text{Mbps}$$

tengo que ver $SWS = 7, 127, y\ 255$.

Ack selectivo significa que $RWS = SWS$.

$$T_{tx} = \frac{1000}{1\cdot10^6} = 0.001\ \text{s} = 1\ \text{ms}$$

Quiero calcular eficiencia de protocolo. Segun las slides eso se da por 

$$ E = \frac{T_{tx}(V)}{RTT(F)} $$

en todos estos casos, sabemos ya el T_tx asi que queda fijo en 0.001s.
Para el RTT, necesitamos $2\cdot(T_{prop} + 0.001\text{s})$.
$T_{prop}$ es 270ms, vease 0.270, asi que el rtt es

$$RTT(F) = 2\cdot 0.271 = 0.542\ \text{s}$$

Y en que carajo nos afecta el SWS aca? que $T_{tx}(V)$ es el tiempo de transmisión de una ventana, es decir de #SWS frames. Para 7 frames, una ventana son 0.007s
lo mismo con cada uno. Las cuentas quedan

$$E_{SWS=7} = \frac{0.007}{0.542} \approx 0.0129 \Rightarrow \mathbf{1.29\%}$$

$$E_{SWS=127} = \frac{0.127}{0.542} \approx 0.2343 \Rightarrow \mathbf{23.43\%}$$

$$E_{SWS=255} = \frac{0.255}{0.542} \approx 0.4705 \Rightarrow \mathbf{47.05\%}$$
respectivamente.

# Ejercicios de Parcial

## Ejercicio 15

### a)

640x480 pixeles = 307200 px. 
cada pixel puede adoptar 256 colores. 256 es 2^8 así que hay 8 bits x pixel
son 2457600 bis por imagen.
20 imagenes x segundo = Rb
Entonces tenemos 49152000 bits por segundo, o 49,15 Mbps
4MHz
La fuente es equiprobable, es decir, cada color tiene 1/256 de aparecer.
SNR min = 2^Rb/B - 1

49,15/4 = 12.29 ish
SNRmin = 2^12.29 - 1 = 5006.93 ISH.

en dB, 10*log_10(5006.93) 37dB ish.

### b)

C = 4Mhz * log_2(1 + 5006)? = 49.15ish mbps, y V_tx = C. en ese caso, si mandamos 20 imagenes en un segundo, mandamos una cada 0.05s

### c)
sabemos que t_tx es 0.05s, entonces para que t_prop sea 0.05s, con 300.000km/s, tenemos que llevar a 15000km.

## Ejercicio 16


### a)
Variables
D = 10km (mínimo)
40dB de SNR a 10km
V_prop a 300000km/s
Sabemos que H(avion) = 50kb como fuente
para que usamos eso? para estar sin perdida, V_tx debe ser menor que C y los paquetes los vamos a tomar de 50kb.

tenemos que manadar 80 paquetes por segundo, o sea 4000kb por segundo (o 4mb). o sea, necesito 4MB/s? eso es todo?
no
C = B *log_2(1+10000)
C = Rb = 4000kbps, entonces B = 4000/13.288 =ish a 301khz.

### b)
Tenemos 4Mbps, entonces mandamos 80 simbolos por segundo, un simbolo son 50kb, son 0.0125s por paquete.
Ttx = 50000/4000000 = 0.0125
Después, eso viaja en el encale a 300000km/s, a 10 putos kilometros de distancia, cosa que es total y completamente despreciable, con exactitud son 0.0000333
entonces son 0.0125333s por paquete. ish.

### c)
70ms = 0.07s. buscamos que nuestro delay por paquete (que definimos recién como 0.0125333s) sea maximo 0.07. pero nos bajaron el ancho de banda, una bocha.

Es decir, pasamos a tener 20kHz! de ancho de banda. Para que un paquete sea a lo sumo 0.07s, significa que los 80 paquetes por segundo

C = 20kHz*(13.288) = 265.75Kbps de ancho de banda. Chan! Seguimos teniendo que mandar 80 paquetes por segundo, o sea que cada paquete debe pesar, a lo mucho, 3.32kb, que tendremos de entropía entonces.

Epa, pero nunca usamos lo 0.07ms! Y bueno, eso pasa porque yo asumí que todavía queremos mandar 80 paquetes por segundo. ahora, no tendría sentido la consigna no? es claro esto: si tenes 80 paquetes por segundo, cada uno dura 0.0125. entonces pedir 0.07 no condice con mantener los 80. descartemoslos!

Hasta calcular el C ibamos bien.
Nuestro delay por paquete, recordemos, es de:

T_tx = |frame|/V_tx(=C=265.75kbps)
Delay = T_tx(frame) + T_prop(frame(despreciable))
cual es el largo de un frame? definimos que usamos la entropía, entonces es nuestra incognita! y T_tx ya lo tenemos, es 0.07s!
0.07s = H/(265.75kbps) + (0.000033... +-= 0)
= 0.07s *265.75kbps = H_max = 18.6 kb!

Capaz este tiene más sentido. con 0.07s, eso nos quedaría 14.28 paquetes por segundo. (Bastantes menos!)

## Ejercicio 17

Usa SACK
|Frame| es de 2kbit
|SEQ| es 4 bits

### a)
10kbps, 1 s de delay,
eficiencia = SWS * T_tx(F)/RTT,
RTT = 2(T_tx + T_prop)
Tenemos 1 segundo de delay, que segun slides, es el T_prop
Calculemos el T_tx. Sabemos que nuestra V_tx es de 10kbps, y que nuestro frame es de 2kbits, entonces claramente el T_tx es de 0.2s (o 200ms).
Entonces sabemos que el RTT es de 2.4s
También podemos calcular el SWS como 

SWS = ceil(V_tx*RTT/|Frame|). esto queda, 10kbps * (2.4/2kb), entonces el SWS = 12.
OPA. eso es el SWS óptimo! pero tenemos el #SEQ limitado a 4. entonces, recordemos, que #SEQ = ceil(log_2(SWS+RWS)). comoe s SACK, rws = sws
entonces, SWS + RWS = 16 => SWS = RWS = 8. woops.

En ese caso, la eficiencia es 8*(0.2/2.4) te queda 2/3, o 66.67% de eficiencia. Obviamente, si tuviesemos el SWS óptimo, (12), para el que necsitamos un #SEQ de 5 bits, tendríamos 100% de eficiencia.

### b)

tengo 8 de sliding window, entonces mando los 4 juntos al hilo. 2 rebotan con ack, los otros dos no llegan. el ack del 5 devuelve que falta el 4, el ack del 7 marca que falta el 6. se manda el 4, devuelve un ack diciendo q leyó hasta el 5, y despues se manda el 6, y un ack diciendo que leyop hasta el 7, y estamos al día. No se si se hace on timeout o antes, depende de si tiene NAK, pero no vimos eso en clase.

## Ejercicio 18

#SEQ de 10 bits
#ACK de 10 bits
#SACK de 10 bits
Checksum de 16 bits.
Largo fijo de 2kbit, eso nos deja con 2000-46 = 1954 bits de datos.

### a)
Estos numeros que nos piden son RWS Y SWS. Son el mismo, dado que estamos en SACK.

El SWS podemos estimarlo masomenos en base aal #seq, que es ceil(log2(SWS+RWS)) = 10, o sea que el SWS es +- 512, es decir,
2^k-1, 2^9. RWS es igual

### b)

La eficiencia de un protocolo se miude como T_tx(Ventana)/RTT(Frame). En primer lugar, si tenemos el doble de distancia, Va a aumentar el RTT, porque el RTT es
2*(T_tx + T_prop). T_prop estaría duplicado en este caso. Teniendo en cuenta que un SWS*T_tx(F) = RTT (SWS frames van en un RTT), podemos deducir que T_prop = 255\*T_tx de F. Entonces la eficiencia bajaría a un 50% aproximadamente.
A la eficiencia del frame le importa un bledo la distancia, es |datos|/|frame|. en este caso, de yapa, es 0.977.

### c)
Tenemos V_tx de 1mbps. Queremos buscar el T_tx de 20 Mbit de datos.
T_total = #Frames * |F|/V_tx + T_prop.

Que cosas tengo, y que cosas no? T_prop no lo tengo, pero lo puedo deducir.

SWS optimo = V_tx * RTT(F)/|F|
512 = 1000000 * x / 2000
1024000 = 1000000*x
1024000/1000000 = x
x= 1.024

RTT(F) = 2*(T_tx(F) + T_prop)
T_tx(F) = 2000/1000000 = 0.002s de un frame
1.024 = 2*(0.002 + x)
1.024 = 0.004 +2x
1.02 = 2x
x = 0.51s

Tenemos T_prop! nota, con eso podemos definir bien la eficiencia arriba en el b, pero me da paja.
me falta cuantos frame son

entonces
#Frames = ceil(20000000/1954) = 10236 frames.
T_total ahora sí
= 10236 * 2000/1000000 +0.51s
= 20.472 + 0.51s = 20.982 ISH.


## Ejercicio 19

*(resuelto por Claude)*

Datos: enlace de 60 Mbps, ventana deslizante. El satélite **sólo envía datos**; la Tierra responde con un frame de reconocimiento de **1024 bits**: `#ACK (16) | #SACK (16) | Padding | Checksum (16)`.

### a)

Hay campo `#SACK` → es **ACK selectivo** → $RWS = SWS$.

El `#ACK` tiene 16 bits, así que hay $2^{16} = 65536$ números de secuencia distintos. Para evitar reencarnaciones:

$$SWS + RWS \le 2^{16} = 65536 \quad\Rightarrow\quad 2\cdot SWS \le 65536$$

$$\mathbf{SWS = RWS = 2^{15} = 32768}$$

### b)

El satélite sólo manda datos (no hay piggybacking), así que su frame no necesita `#ACK`. Tiene que numerar con el mismo espacio de secuencia que usa la Tierra para reconocer (16 bits):

`#SEQ (16bits); Datos (992bits); Checksum (16bits)` → total 1024 bits.

$$|Datos| = 1024 - 16 - 16 = 992\ \text{bits}$$

$$\eta_{frame} = \frac{992}{1024} \approx \mathbf{0.969 = 96.9\%}$$

### c)

El delay dado (6 min) es $T_{prop}$ (convención de la materia): $T_{prop} = 360\ \text{s}$.

$$T_{tx}(F) = \frac{1024}{60\cdot10^6} \approx 1.707\cdot10^{-5}\ \text{s}$$

$$RTT(F) = 2\cdot(T_{tx}(F) + T_{prop}) = 2\cdot(0.00001707 + 360) \approx 720.00003\ \text{s}$$

$$T_{tx}(V) = SWS\cdot T_{tx}(F) = 32768 \cdot 1.707\cdot10^{-5} \approx 0.5592\ \text{s}$$

$$\eta_{proto} = \frac{T_{tx}(V)}{RTT(F)} = \frac{0.5592}{720.00003} \approx 7.77\cdot10^{-4} \approx \mathbf{0.078\%}$$

Tiene sentido que sea bajísima: la ventana se manda en medio segundo y después el satélite se queda ~12 minutos esperando el primer ACK. La ventana óptima sería $V_{tx}\cdot RTT/|F| \approx 42$ millones de frames, pero los 16 bits de secuencia la limitan a 32768.

## Ejercicio 20

*(resuelto por Claude)*

Datos: SNR = 30 dB, $B = 50$ MHz, cámara de 5 Megapíxeles por imagen, 12 bits por píxel.

### a)

**Capacidad del canal** (Shannon):

$$SNR = 10^{30/10} = 1000 \text{ veces}$$

$$C = B\cdot\log_2(1+SNR) = 50\cdot10^6\cdot\log_2(1001) \approx 50\cdot10^6 \cdot 9.967 \approx 498.36\ \text{Mbps}$$

**Bits por imagen**: 12 bits por píxel → $2^{12} = 4096$ valores posibles. Como la fuente es **equiprobable**, $H = \log_2(4096) = 12$ bits/píxel, y el código de largo fijo de 12 bits ya es óptimo ($L = H$).

$$|imagen| = 5\cdot10^6 \cdot 12 = 60\cdot10^6\ \text{bits}$$

**Sin pérdida** → $R_b \le C$:

$$R_b = img/s \cdot 60\cdot10^6 \le 498.36\cdot10^6 \quad\Rightarrow\quad img/s \le 8.306$$

Como son imágenes enteras: **hasta 8 imágenes por segundo**.

### b)

Usando $V_{tx} = C$ (máximo, salvo que se diga lo contrario):

$$T_{tx}(imagen) = \frac{60\cdot10^6}{498.36\cdot10^6} \approx 0.12039\ \text{s}$$

$$T_{prop} = \frac{2\ \text{km}}{300000\ \text{km/s}} \approx 6.67\cdot10^{-6}\ \text{s}$$

$$Delay(imagen) = T_{tx} + T_{prop} \approx 0.12039 + 0.0000067 \approx \mathbf{0.1204\ s \approx 120.4\ ms}$$

$T_{prop}$ es despreciable: a 2 km casi todo el delay es transmisión. (Es "promedio" porque la entropía es un promedio de bits por símbolo; con fuente equiprobable y largo fijo, en realidad todas las imágenes miden lo mismo.)

### c)

Si la fuente **no** es equiprobable, su entropía es **menor** que el máximo: $H < \log_2(4096) = 12$ bits/píxel (la entropía es máxima sólo cuando los símbolos son equiprobables).

Con una codificación óptima (ej. Huffman, dándole códigos más cortos a los colores más probables), el largo promedio $L$ puede acercarse a $H$ ($H \le L < H+1$), así que cada píxel usa **en promedio menos de 12 bits** → cada imagen pesa menos bits → con la misma capacidad $C$ entran más imágenes por segundo:

$$img/s \le \frac{C}{5\cdot10^6 \cdot L} \quad\text{con } L < 12$$

Es "en teoría" porque depende de conocer la distribución real de la fuente y de usar un código que la aproveche; la capacidad del canal no cambia, lo que baja es cuántos bits hace falta mandar.
