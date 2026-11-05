# Simulacro 2 — 2do parcial Redes (RCCD 2C 2026)

**Tiempo:** 1 h 30. **Con machete, sin mirar las guías ni el simulacro 1 resuelto.** Justificá todo y escribí los supuestos que tomes.

De dónde sale cada ejercicio:
- Ej 1 y 2: **literales del 2do parcial del 19/06/2024** (eran la reserva del simulacro 1).
- Ej 3 y 4: **"Ejercicios de Parcial" de la Guía 7** (Ej 7 y Ej 9), literales.
- Ej 5: **armado** (arquitecturas, igual que en el simulacro 1).
- Ej 6: preguntas tipo teórica del `resumen-teorico.pdf`. No hay parciales viejos de Lamport/TrueTime/Blockchain porque es plan nuevo.

---

## Ejercicio 1 — DNS TTL *(19/06/2024, ej 3)*

Suponiendo que un registro A asignado al nombre de dominio `dc.uba.ar` tiene un valor de TTL de 3 días, y cambia la dirección IP de 157.92.27.128 a 157.92.27.200, ¿cuál será la respuesta de los *Resolvers* que tengan el registro en caché durante los 2 días posteriores al cambio?

## Ejercicio 2 — HTTP *(19/06/2024, ej 4)*

Explicar las diferencias entre los mensajes GET y POST de HTTP. Mostrar un ejemplo de cada tipo de mensaje.

## Ejercicio 3 — Seguridad *(Guía 7, ej 7 de parcial)*

En el hall de un hotel hay un WiFi donde los huéspedes pueden conectarse y navegar en internet usando sus dispositivos móviles. Se desea que sólo puedan navegar la Web vía un servidor Proxy. Repetidas veces, hackers han espiado las peticiones de los clientes. Diseñe un sistema criptográfico de clave asimétrica, que garantice la autenticidad del proxy y la confidencialidad de los clientes. Aclare dónde deberían instalarse los certificados.

## Ejercicio 4 — Seguridad *(Guía 7, ej 9 de parcial)*

La empresa Security First expone una API usando el protocolo HTTP. Dicha API tiene un método `getPrice` que devuelve el precio de frutas usando la siguiente url: `http://api.securityfirst.com/?method=getPrice&fruit=Pera`.

Es necesario agregar un método nuevo a la API que haga lo mismo que el `getPrice` pero que provea el servicio sólo a usuarios autenticados brindando integridad y no repudio del lado del servidor sobre los pedidos de los usuarios.
1. Explique qué información tiene que tener el cliente y el servidor para que esto sea posible.
2. Muestre una posible url que permita procesar el pedido.
3. Explique qué es lo que tiene que hacer cada parte para garantizar lo solicitado.

*Nota: es requisito para lo anterior no usar encripción sobre la totalidad del mensaje y no manejar sesiones.*

## Ejercicio 5 — Arquitecturas *(armado)*

Un **estacionamiento medido** de una ciudad tiene:
- Un **sensor** por lugar (detecta si hay auto), conectado por radio de corto alcance a un **poste** por cuadra.
- **Carteles** en las esquinas que muestran cuántos lugares libres hay en las próximas cuadras.
- Una **app** donde el conductor ve lugares libres y paga el estacionamiento.
- **Inspectores** con una terminal que les avisa qué autos están estacionados sin pago.
- Requisito: los carteles tienen que actualizarse en **menos de 2 s** aunque se caiga el enlace a la nube.

a. Definí los componentes con su **interfaz**, su **procesamiento** y sus **datos**.
b. Para cada conector, indicá el **acoplamiento referencial y temporal**. Justificá dónde usarías pub/sub y dónde comunicación directa.
c. Ubicá cada componente en **edge / fog / cloud** y justificá con los motivos vistos. ¿Qué pasa si un inspector consulta un auto justo cuando el poste de esa cuadra está desconectado de la nube?

## Ejercicio 6 — Teórica *(del resumen teórico, tapá la sección 9)*

Elegí **dos** y respondelas en ≤ 10 líneas cada una:
- Pregunta 7: relojes de Lamport vs vectoriales (¿qué no te garantiza C(a) < C(b)?).
- Pregunta 8: TrueTime y commit wait.
- Pregunta 2: PoW, ataque Sybil y 51 %.
