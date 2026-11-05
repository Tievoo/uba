# Simulacro — 2do parcial Redes (RCCD 2C 2026)

**Tiempo:** 2 h. **Con machete, sin mirar las guías.** Justificá todo y escribí los supuestos que tomes.

Los ejercicios son **literales de los 2dos parciales del 19/06/2024 y del 18/06/2025** (Teoría de las Comunicaciones). Solo el de arquitecturas es armado, porque ese tema no estaba en esos parciales.

---

## Ejercicio 1 — Congestión *(19/06/2024, ej 2)*

El control de congestión de TCP usa retroalimentaciones para cambiar el valor de la ventana de congestión (CWND). Explicar alguna de las retroalimentaciones aclarando cómo se actualiza CWND.

## Ejercicio 2 — DNS *(18/06/2025, ej 2)*

Una aplicación tiene que resolver la dirección IP de un servidor Web con nombre `www.dominio.com.ar`. Para esto tiene configurado un DNS Resolver que se encarga de recibir las consultas recursivas y realiza la secuencia de consultas iterativas para obtener la información solicitada. Suponiendo que hay una zona de autoridad por cada subdominio del dominio que se está consultando, muestre una posible secuencia de mensajes DNS hasta que la aplicación obtiene la dirección IP. *Aclarar de qué dispositivo se envía cada mensaje.*

## Ejercicio 3 — Mail / TCP *(18/06/2025, ej 3)*

Desde una casilla de correo en `undominio.org.ar` se envía un correo a una cuenta en el dominio `otrodominio.org.ar`. Más tarde, se accede a la casilla de correo en `otrodominio.org.ar` desde un Navegador Web vía webmail. Describa las conexiones TCP que se establecen, mencionando entre qué dispositivos son y a qué protocolos de capa de aplicación están relacionadas.

## Ejercicio 4 — Seguridad *(18/06/2025, ej 4)*

Una compañía desea utilizar un sistema criptográfico de clave asimétrica para el control de acceso de sus empleados utilizando una aplicación móvil. Suponiendo que la empresa dispone de un certificado digital firmado por una autoridad certificante, diseñe un criptosistema que verifique la autenticidad de los empleados mencionando dónde deben instalarse los certificados digitales.

## Ejercicio 5 — Arquitecturas *(armado)*

Una ciudad implementa un sistema de **bicicletas públicas**:
- **Estaciones**, cada una con N anclajes con sensor y traba.
- Una **app móvil** para buscar estaciones con bicis libres y desbloquear una.
- Un **servidor central** que lleva los viajes, los usuarios y la disponibilidad en tiempo real.
- Requisito: si una estación **pierde la conexión**, los usuarios tienen que poder seguir **devolviendo** bicis.

a. Definí los componentes con su **interfaz**, su **procesamiento** y sus **datos**.
b. Para cada conector, indicá el protocolo y el **acoplamiento referencial y temporal**. Justificá dónde usarías pub/sub y dónde comunicación directa.
c. Ubicá cada componente en **edge / fog / cloud** y justificá con al menos dos de los motivos vistos. ¿Cómo garantizás el requisito de la desconexión, y qué pasa con la consistencia al reconectar?

## Ejercicio 6 (opcional) *(18/06/2025, ej 5)*

Explique la diferencia entre Clave Simétrica y Clave Pública en Seguridad Informática.

---

### Reserva (19/06/2024), literales

- **DNS TTL** *(ej 3)*: Suponiendo que un registro A asignado al nombre de dominio dc.uba.ar tiene un valor de TTL de 3 días, y cambia la dirección IP de 157.92.27.128 a 157.92.27.200, ¿cuál será la respuesta de los *Resolvers* que tengan el registro en caché durante los 2 días posteriores al cambio?
- **HTTP** *(ej 4)*: Explicar las diferencias entre los mensajes GET y POST de HTTP. Mostrar un ejemplo de cada tipo de mensaje.
