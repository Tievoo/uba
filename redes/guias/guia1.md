# Guía 1 — Transmisión confiable de información

*Redes de Comunicaciones y Cómputo Distribuido — FCEN, UBA*

hecha por mí, formateada por mi brother Sonnet 

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

Todo.
