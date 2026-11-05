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

### Solución

**Idea clave.** DNS no avisa a las cachés cuando un registro cambia. Un resolver que tiene el registro A de `dc.uba.ar` en caché lo considera válido hasta que se le vence el TTL. Mientras tanto responde desde la caché y **no vuelve a consultar** al servidor autoritativo de `uba.ar`.

**Qué responden.** Los resolvers que tienen el registro en caché responden la **IP vieja, 157.92.27.128**, como respuesta **no autoritativa**, porque sale de su caché y no del servidor de la zona. Lo hacen durante el TTL que les queda.

**Cuánto dura.** Depende de cuándo cacheó el registro cada resolver. El TTL que le queda a cada uno está entre 0 y 3 días:

| TTL restante al momento del cambio | Respuesta durante los 2 días siguientes |
|---|---|
| ≥ 2 días (lo cacheó hace ≤ 1 día) | La IP vieja **los 2 días completos** |
| t < 2 días | La IP vieja hasta que pasa t. Después se le vence el registro y en la próxima consulta resuelve de nuevo en forma iterativa (raíz → `.ar` → `uba.ar`). Desde ahí responde la **nueva, 157.92.27.200** |

En el peor caso, un resolver que lo cacheó justo antes del cambio sigue respondiendo la IP vieja hasta 3 días después del cambio. Un resolver que **no** tenía el registro en caché consulta en ese momento y obtiene la nueva directamente.

**Consecuencia práctica.** Durante ese tiempo los clientes que usan esos resolvers van a la IP vieja, y si el servidor ya no está ahí, no llegan. Por eso, antes de cambiar una IP, conviene **bajar el TTL** con anticipación, por ejemplo a unos minutos, al menos 3 días antes, que es el TTL viejo. Después del cambio se lo vuelve a subir. Otra opción es mantener el servidor viejo andando hasta que vencen las cachés.

## Ejercicio 2 — HTTP *(19/06/2024, ej 4)*

Explicar las diferencias entre los mensajes GET y POST de HTTP. Mostrar un ejemplo de cada tipo de mensaje.

### Solución

| | **GET** | **POST** |
|---|---|---|
| Para qué | **Obtener** un recurso, sin modificar nada | **Enviar datos** al servidor, por ejemplo para crear un recurso, mandar un formulario o subir un archivo |
| Dónde van los datos | En la **URL** (query string `?k=v&...`). **No lleva body** | En el **body**, descrito con `Content-Type` (por ejemplo `application/json` o `multipart/form-data`) y `Content-Length` |
| Visibilidad / límites | Los parámetros quedan en la URL: historial, logs, bookmarks. Largo limitado | No aparecen en la URL. Sin límite práctico de tamaño (archivos) |
| Seguro (no cambia estado) | Sí | No |
| Idempotente | Sí: repetirlo da el mismo resultado | **No**: repetirlo puede crear dos recursos, por eso el navegador pregunta "¿reenviar formulario?" |
| Cacheable | **Sí**. Puede ser **condicional** (`If-Modified-Since` → `304 Not Modified`), y eso lo aprovechan los proxies y cachés | En general no |
| Respuestas típicas | `200 OK` con el recurso, `304 Not Modified`, `404 Not Found` | `201 Created` con el header `Location` del recurso nuevo, o `200 OK` |

**Ejemplo GET.** Una línea de request, los headers y una línea en blanco, sin body:

```
GET /materias?depto=dc&anio=2026 HTTP/1.1
Host: www.uba.ar
Accept: text/html
If-Modified-Since: Mon, 02 Nov 2026 10:00:00 GMT

```

Respuesta posible: `HTTP/1.1 304 Not Modified`. No trae body: el cliente usa su copia en caché.

**Ejemplo POST.** La línea de request y los headers, una línea en blanco y después el body:

```
POST /inscripciones HTTP/1.1
Host: www.uba.ar
Content-Type: application/json
Content-Length: 40

{"alumno": "123/21", "materia": "redes"}
```

Respuesta posible:

```
HTTP/1.1 201 Created
Location: /inscripciones/987
```

**Nota.** Si un POST va sobre HTTP sin TLS, sus datos son tan visibles en la red como los de un GET. "Va en el body" no significa que esté cifrado: para eso hace falta HTTPS.

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
