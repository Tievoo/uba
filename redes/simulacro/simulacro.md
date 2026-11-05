# Simulacro — 2do parcial Redes (RCCD 2C 2026)

**Tiempo:** 2 h. **Con machete, sin mirar las guías.** Justificá todo y escribí los supuestos que tomes. En congestión usá los valores de la guía 5 (SMSS = 2 KB, IW = 4 KB, ISSTHRESH = 64 KB, LW = 1 SMSS).

Los ejercicios 1, 2, 3 y 5 son **literales de 2dos parciales viejos** de Teoría de las Comunicaciones (CubaWiki). Solo el 4 (arquitecturas) es armado, porque en los parciales viejos ese tema no estaba.

---

## Ejercicio 1 — Congestión *(2do parcial 16/11/2022, ej 2)*

Una conexión TCP recién establecida tiene un RTT = 100 ms y debe transmitir 70 KB. El receptor siempre anuncia una *Advertised Window* de 64 KB y se sabe que el proveedor de servicio del host emisor limita la velocidad descartando todos los segmentos de una ráfaga si se envían 32 KB o más por RTT.

a. ¿Cuántos datos lleva transmitidos con éxito (i.e.: datos que ya no están "en vuelo") y cuántos están en vuelo a los 450 ms?

b. Si a partir de los 650 ms de iniciada la transferencia, la red desordena todas las ráfagas de segmentos que envía el emisor, de manera que el primer segmento siempre llega al final manteniendo el orden del resto de los segmentos de la ráfaga, ¿en qué instante se activa el algoritmo de *Fast Recovery / Fast Retransmit*?

c. *(Conceptual, 2do parcial 2018, ej 2c)* ¿Cuál es la desventaja de usar Fast Retransmit/Fast Recovery en una conexión que pasa por una red que desordena muchos paquetes?

## Ejercicio 2 — Aplicación *(2do parcial 13/11/2019, ej 4)*

Dado el siguiente fragmento de la base de datos de un servidor DNS autoritativo para el dominio `uba.ar` y la siguiente secuencia de peticiones HTTP realizadas por un mismo navegador en una PC con nombre `gorrion.uba.ar.`:

```
Base de datos DNS                                Peticiones HTTP
...
uba.ar.        IN  NS        ns1.uba.ar          GET /logo.jpg HTTP/1.1
uba.ar.        IN  NS        ns2.uba.ar          Host: secretaria.uba.ar
uba.ar.        IN  MX     5  smtp1.uba.ar        User-agent: Mozilla/4.0
uba.ar.        IN  MX    15  celeste.dc.uba.ar   Accept-Language: es
rectorado      IN  CNAME     secretaria.uba.ar   ...
alumnos        IN  CNAME     secretaria.uba.ar
ns1            IN  A         208.25.19.1         GET /logo.jpg HTTP/1.1
ns2.uba.ar.    IN  A         208.25.19.3         Host: rectorado.uba.ar
secretaria     IN  A         208.25.19.87        User-agent: Mozilla/4.0
gorrion        IN  A         208.25.19.2         Accept-Language: es
smtp1.uba.ar.  IN  A         208.25.19.99        ...
smtp2          IN  A         208.25.19.55
...
```

Se pide:

a. ¿Los encabezados de las respuestas son necesariamente iguales? ¿Las imágenes son necesariamente iguales? Explicar.

b. Muestre las conexiones TCP involucradas en las peticiones HTTP en el siguiente formato: `<ip origen, puerto origen, ip destino, puerto destino>`

c. En el instante t₀ un usuario desde su PC en algún lugar de Internet envía un correo electrónico a la dirección `rector@uba.ar`. En ese mismo instante todos los servidores SMTP receptores del dominio se encuentran apagados por mantenimiento. Indique cuáles son esos servidores y sus direcciones IP si las conoce. ¿Qué ocurre con el mensaje de correo enviado?

## Ejercicio 3 — Seguridad

**a.** *(2do recuperatorio 22/11/2023, ej 5)* Los servidores de un sistema distribuido necesitan comunicarse a través de Internet garantizando su AUTENTICIDAD entre sí (los servidores todos contra todos) y para eso usan SSL/TLS para comunicarse. Suponiendo que la compañía dispone de un certificado digital firmado por una autoridad certificante, explicar dónde deberían instalarse los certificados digitales y por quién deberían estar firmados.

**b.** *(2do parcial 15/11/2017, ej 3a)* Ernesto es popular por su fanatismo para utilizar conexiones Wi-Fi inseguras donde Marquitos suele *sniffearle* los paquetes y robarle información. Dado que Claudia teme que a Martín le llegue el contenido de estos mensajes, es necesario que no puedan ser descifrados por Marquitos pero sí por Ernesto.
  1. Explique un mecanismo que garantice esta propiedad. ¿Qué información tienen que tener Claudia y Ernesto para que esto sea posible?
  2. Justifique cuáles aspectos de seguridad (confidencialidad, no repudio, integridad, autenticidad, disponibilidad) se cumplen cada vez que Claudia le envía un email a Ernesto.

  **Nota:** No se puede usar ningún protocolo que corra sobre TLS/SSL.

## Ejercicio 4 — Arquitecturas *(armado, no hay parciales viejos del tema)*

Una ciudad implementa un sistema de **bicicletas públicas**:
- **Estaciones**, cada una con N anclajes con sensor y traba.
- Una **app móvil** para buscar estaciones con bicis libres y desbloquear una.
- Un **servidor central** que lleva los viajes, los usuarios y la disponibilidad en tiempo real.
- Requisito: si una estación **pierde la conexión**, los usuarios tienen que poder seguir **devolviendo** bicis.

a. Definí los componentes con su **interfaz**, su **procesamiento** y sus **datos**.
b. Para cada conector, indicá el protocolo y el **acoplamiento referencial y temporal**. Justificá dónde usarías pub/sub y dónde comunicación directa.
c. Ubicá cada componente en **edge / fog / cloud** y justificá con al menos dos de los motivos vistos. ¿Cómo garantizás el requisito de la desconexión, y qué pasa con la consistencia al reconectar?

## Ejercicio 5 (opcional) *(2do parcial 18/06/2025, ej 5)*

Explique la diferencia entre Clave Simétrica y Clave Pública en Seguridad Informática.

---

### Reserva (si sobra tiempo o para mañana), todos literales

- **Congestión** *(2do recu 22/11/2023, ej 2)*: En una conexión recién establecida con RTT = 100 ms el receptor siempre anuncia una *Advertised Window* de 64 KB. A su vez, el proveedor de servicio descarta los paquetes de la misma si una ráfaga fuera de 12 KB o más. ¿Cuáles son los valores finales de CWND y SSTHRESH después de enviar 50 KB de datos?
- **DNS + mail** *(2do recu 22/11/2023, ej 3)*: Peterson y Tanenbaum desean comunicarse por correo electrónico utilizando direcciones de correo personalizadas. Sus direcciones son `claudio@peterson.com` y `ernesto@tanenbaum.com`. Describa los registros DNS necesarios en las zonas de dominio peterson.com y tanenbaum.com para que puedan enviarse y recibir correos. Suponer que la descarga de los correos es por medio del protocolo POP3.
- **Mail / TCP** *(2do recu 22/11/2023, ej 4)*: Un usuario en una PC envía un correo en texto plano, usando un *User Agent*, a un usuario que accede a su correo usando *Webmail*. Suponiendo que el servidor Webmail usa POP3 para descargar los correos desde el servidor entrante, explicar cuántas conexiones TCP se abren y qué protocolos transportan desde que se envía el correo hasta que el usuario lo visualiza en su computadora. *(PC → servidor de correo saliente → servidor de correo entrante ← servidor webmail ← PC)*
- **DNS iterativo** *(2do parcial 15/11/2017, ej 2.2)*: Suponiendo que todas las caches de la red están vacías, detalle los mensajes del protocolo DNS necesarios para que el DNS resolver *Stallings*, de quien ya se conoce la IP, obtenga una respuesta autoritativa cuando consulta por la IP del servidor de correo de peterson.com mediante una consulta iterativa. La consulta DNS a Stallings es recursiva.
- **SSH** *(2do parcial 13/11/2019, ej 3b)*: Los usuarios en la red interna quieren acceder al servidor por SSH pero sin tener que escribir su contraseña; muestre cómo deberían instalarse las claves para que el servicio SSH pueda garantizar la autenticidad de cada usuario.
- **Congestión conceptual** *(2do parcial 19/06/2024, ej 2)*: El control de congestión de TCP usa retroalimentaciones para cambiar el valor de la ventana de congestión (CWND). Explicar alguna de las retroalimentaciones aclarando cómo se actualiza CWND.
- **DNS TTL** *(2do parcial 19/06/2024, ej 3)*: Suponiendo que un registro A asignado al nombre de dominio dc.uba.ar tiene un valor de TTL de 3 días, y cambia la dirección IP de 157.92.27.128 a 157.92.27.200, ¿cuál será la respuesta de los Resolvers que tengan el registro en caché durante los 2 días posteriores al cambio?
