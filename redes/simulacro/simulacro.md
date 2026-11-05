# Simulacro — 2do parcial Redes (RCCD 2C 2026)

**Tiempo:** 2 h. **Con machete, sin mirar las guías.** Justificá todo: se corrige el razonamiento, no solo el resultado. Escribí los supuestos que tomes.

---

## Ejercicio 1 — Congestión

Valores de la guía: SMSS = 2 KB, IW = 4 KB, ISSTHRESH = 64 KB, LW = 1 SMSS. El receptor anuncia RWND = 32 KB fija. La red **pierde la ráfaga entera** cada vez que en un RTT se envían **24 KB o más**. El time-out se detecta **2 RTT** después de enviar la ráfaga perdida.

a. Armá la tabla RTT a RTT (CWND, lo que se envía, SSTHRESH, qué pasa) para los primeros **15 RTT**.
b. ¿Llega a un estado estacionario? Si sí, ¿cuántos KB útiles por RTT transmite en promedio en ese ciclo?
c. Si en vez de perder la ráfaga entera se perdiera **un solo segmento** de cada ráfaga ≥ 24 KB, ¿qué mecanismo actuaría y cómo cambiaría la evolución de CWND? (No hace falta la tabla, explicalo.)

## Ejercicio 2 — Aplicación (guía 6 ej 12)

Desde una computadora se conectan a un servicio de **Webmail** usando un **Proxy Web HTTPS**. El servidor de Webmail envía el mail usando un **servidor SMTP**. Finalmente, el mail llega al **servidor de mail del dominio de destino**, y otra computadora lo descarga usando **POP3**.

```
[PC 1] ── [Proxy HTTPS] ── [Webmail] ── [SMTP saliente] ── [Mail destino] ── [PC 2]
```

a. Describí **todas las conexiones TCP** que se establecen durante todo el proceso y qué protocolo de aplicación transporta cada una (incluí puertos).
b. ¿En qué momento se hace la consulta DNS por el registro **MX** del dominio de destino? ¿Quién la hace?
c. ¿Qué tramos van cifrados? ¿El proxy puede leer el contenido del mail?

## Ejercicio 3 — Seguridad

El sistema web de notas de una facultad tiene que cumplir dos requisitos:
1. Solo los **docentes** pueden cargar notas, autenticados **sin usuario y contraseña**.
2. Cualquier alumno tiene que poder **verificar que una nota la cargó un docente en particular**, y el docente no puede negar haberla cargado.

a. Diseñá la solución. Indicá qué claves y certificados se instalan **en cada máquina** (servidor, docentes, alumnos) y quién emite los certificados.
b. Describí el handshake que autentica al docente: qué mensajes intervienen y qué chequea el servidor.
c. ¿Cómo se cumple el requisito 2? ¿Qué se guarda junto a cada nota y cómo verifica el alumno? ¿Por qué no alcanzaría con un MAC?

## Ejercicio 4 — Arquitecturas

Una ciudad implementa un sistema de **bicicletas públicas**:
- **Estaciones**, cada una con N anclajes con sensor y traba.
- Una **app móvil** para buscar estaciones con bicis libres y desbloquear una.
- Un **servidor central** que lleva los viajes, los usuarios y la disponibilidad en tiempo real.
- Requisito: si una estación **pierde la conexión**, los usuarios tienen que poder seguir **devolviendo** bicis.

a. Definí los componentes con su **interfaz**, su **procesamiento** y sus **datos**.
b. Para cada conector, indicá el protocolo y el **acoplamiento referencial y temporal**. Justificá dónde usarías pub/sub y dónde comunicación directa.
c. Ubicá cada componente en **edge / fog / cloud** y justificá con al menos dos de los motivos vistos. ¿Cómo garantizás el requisito de la desconexión, y qué pasa con la consistencia al reconectar?

## Ejercicio 5 (opcional) — Teórica

Tres procesos. **p1:** evento local `a`, después envía `m1` a p3 (evento `b`). **p2:** envía `m2` a p3 (evento `c`), después evento local `d`. **p3:** recibe `m2` (evento `e`), después recibe `m1` (evento `f`), después evento local `g`.

a. Calculá los relojes de Lamport y los vectoriales de todos los eventos.
b. ¿`a` y `d` son concurrentes? ¿Y `c` y `b`? Justificá con los vectores. ¿Lamport alcanza para decidirlo?
c. En una línea: ¿qué puede ordenar TrueTime que Lamport no, y qué paga por eso?
