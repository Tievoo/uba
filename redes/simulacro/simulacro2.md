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

### Solución

**Supuesto.** El hotel obtiene para el proxy un certificado digital firmado por una **CA reconocida**: $Cert_P = \{ \text{proxy.hotel.com}, K_P^+ \}$ firmado con $K_{CA}^-$.

**Diseño.** Los clientes se conectan al proxy con **TLS común**, que autentica solo al servidor. No hace falta autenticar a los clientes, porque el enunciado no lo pide, y darles certificados a huéspedes que van y vienen sería volver al problema de distribuir claves.

1. **Hello:** el cliente y el proxy intercambian nonces $R_C$ y $R_S$ y acuerdan los algoritmos.
2. **Certificate:** el proxy manda $Cert_P$. El cliente lo verifica:
   - que la firma sea válida con $K_{CA}^+$;
   - que el nombre coincida con el del proxy configurado;
   - que esté vigente y no revocado.
3. **Key exchange:** el cliente genera un pre-master secret (PMS) y lo manda cifrado como $E_{K_P^+}(PMS)$. Solo el proxy puede descifrarlo, con $K_P^-$.
4. **Claves de sesión:** los dos derivan $K_{sesión} = PRF(PMS, R_C, R_S)$. Desde ahí, todas las peticiones del cliente viajan cifradas con criptografía simétrica.

**Qué garantiza cada cosa.**
- **Autenticidad del proxy.** El certificado es público, así que cualquiera puede reenviarlo. Lo que no puede hacer un impostor es descifrar el PMS, porque no tiene $K_P^-$. Sin el PMS no puede derivar las claves de sesión, y el handshake falla en el `Finished`.
- **Confidencialidad.** Un hacker que escucha la WiFi ve $E_{K_P^+}(PMS)$ y tráfico cifrado con claves de sesión que no puede calcular.

**Dónde se instala cada cosa.**

| Dónde | Qué |
|---|---|
| Proxy | $Cert_P$ y su clave privada $K_P^-$, que nunca sale del proxy |
| Dispositivos de los huéspedes | El certificado raíz de la CA, con $K_{CA}^+$. **Ya viene preinstalado en el OS o el navegador**, así que no viaja por la red y el atacante no lo puede reemplazar |

*Extra:* si además se quisiera que solo naveguen huéspedes, se agrega autenticación de cliente, por ejemplo TLS mutuo o una clave por habitación. No lo pide el enunciado.

## Ejercicio 4 — Seguridad *(Guía 7, ej 9 de parcial)*

La empresa Security First expone una API usando el protocolo HTTP. Dicha API tiene un método `getPrice` que devuelve el precio de frutas usando la siguiente url: `http://api.securityfirst.com/?method=getPrice&fruit=Pera`.

Es necesario agregar un método nuevo a la API que haga lo mismo que el `getPrice` pero que provea el servicio sólo a usuarios autenticados brindando integridad y no repudio del lado del servidor sobre los pedidos de los usuarios.
1. Explique qué información tiene que tener el cliente y el servidor para que esto sea posible.
2. Muestre una posible url que permita procesar el pedido.
3. Explique qué es lo que tiene que hacer cada parte para garantizar lo solicitado.

*Nota: es requisito para lo anterior no usar encripción sobre la totalidad del mensaje y no manejar sesiones.*

### Solución

**Idea.** Cada pedido viaja **firmado digitalmente por el cliente** con su clave privada.
- **Integridad:** si alguien cambia un parámetro, la firma no cierra.
- **No repudio:** solo el cliente tiene su clave privada, así que no puede negar el pedido.

Se firma un **hash** de los parámetros, no el mensaje entero. Así se cumple la nota: los datos viajan en claro. Como no hay sesiones, **cada pedido se autentica solo**.

**1. Qué información tiene cada parte**

| Parte | Qué tiene |
|---|---|
| Cliente | Su par de claves: $K_C^-$ (privada, solo él) y $K_C^+$. Opcionalmente, un certificado $Cert_C$ firmado por una CA |
| Servidor | La $K_C^+$ de cada usuario, asociada a su identificador. Se registra al dar de alta la cuenta, o se obtiene de $Cert_C$ verificándolo con $K_{CA}^+$. Además, la lista de nonces ya usados en la ventana de tiempo vigente |
| Ambos | La misma función de hash $H$ (por ejemplo SHA-256) y el mismo formato para concatenar los parámetros |

**2. Una posible URL**

```
http://api.securityfirst.com/?method=getPriceSigned&fruit=Pera&user=bruno
    &ts=1730800000&nonce=8f3a91c2&sig=<firma>
```

donde

$$sig = E_{K_C^-}\big(H(\texttt{getPriceSigned} \,\|\, \texttt{Pera} \,\|\, \texttt{bruno} \,\|\, ts \,\|\, nonce)\big)$$

La firma también podría ir en un header, como `Authorization`. Funciona igual, pero el enunciado pide una URL.

**3. Qué hace cada parte**

*Cliente, en cada pedido:*
1. Genera un `nonce` aleatorio y toma el `ts` actual.
2. Calcula $h = H(\text{method} \| \text{fruit} \| \text{user} \| ts \| nonce)$.
3. Firma: $sig = E_{K_C^-}(h)$.
4. Manda la URL con los parámetros en claro y la firma.

*Servidor, al recibirlo:*
1. Busca la $K_C^+$ de `user`. Si no existe, rechaza el pedido: el usuario no está autenticado.
2. Recalcula $h' = H(\text{parámetros recibidos})$ y verifica que $D_{K_C^+}(sig) = h'$. Si coincide, tiene **integridad y autenticación**.
3. **Anti-replay.** Rechaza el pedido si `ts` cae fuera de una ventana, por ejemplo ±5 min, o si el `nonce` ya se usó dentro de esa ventana. Si lo acepta, guarda el nonce.
4. **Guarda el pedido junto con su firma.** Esa es la prueba de **no repudio**: un tercero puede verificar con $K_C^+$ que solo el dueño de $K_C^-$ pudo generarla.
5. Responde el precio.

**Por qué timestamp y nonce juntos.**
- Con **solo nonce**, el servidor tendría que guardar todos los nonces para siempre.
- Con **solo timestamp**, se podría repetir el pedido dentro de la ventana.

Juntos, el `ts` acota la ventana y el servidor solo guarda los nonces de esos minutos.

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

### Solución

**Supuestos**
1. El sensor solo detecta si el lugar está **ocupado o libre** y lo informa con su `idLugar`. No lee patentes.
2. El conductor paga por anticipado desde la app: indica el **lugar**, la **patente** y la cantidad de horas. La nube cruza ocupación y pagos: un lugar ocupado sin pago vigente es una **infracción**.
3. Se agrega un **gateway de zona** (nodo fog) que agrupa los postes de varias cuadras y tiene el broker de los carteles.
4. El poste mantiene el estado de su cuadra aunque no tenga enlace a la nube.

**Diagrama**

```
        [Sensor]...[Sensor]           (radio corto alcance)
              \     /
              [Poste cuadra X] ──pub cuadra/X──► [Gateway zona (broker)] ──► [Cartel esquina]
                    │                                   ▲ sub cuadra/X, X+1, X+2
                    │ cola (store-and-forward)
                    ▼
               [Nube: servidor] ◄──request/response── [App conductor]
                    │
                    └──pub infracciones/zona──► [Terminal inspector]
```

#### a. Componentes

| Componente | Interfaz | Procesamiento | Datos |
|---|---|---|---|
| Sensor | Emite `ocupado(idLugar)` / `libre(idLugar)` | Detecta un cambio en el lugar y lo informa | Estado de su lugar |
| Poste | Recibe los eventos de los sensores. Publica `cuadra/X: libres=n`. Envía `cambioLugar(idLugar, estado, ts)` a la nube | Mantiene el estado de la cuadra, calcula los lugares libres y encola los eventos para la nube si no hay enlace | Ocupación de cada lugar de su cuadra y la cola de eventos pendientes |
| Gateway de zona | Broker pub/sub: `publish(tópico, msg)`, `subscribe(tópico)` | Reenvía las publicaciones de los postes a los carteles suscriptos | Suscripciones y último valor de cada tópico |
| Cartel | Se suscribe a `cuadra/X`, `cuadra/X+1`, ... | Suma los libres de las cuadras próximas y los muestra | Último valor recibido por cuadra |
| App | `verLibres(zona)`, `pagar(lugar, patente, horas)` | Muestra el mapa y hace el pago | Sesión y datos del usuario |
| Servidor (nube) | `cambioLugar(...)`, `verLibres(zona)`, `pagar(...)`. Publica `infracciones/zona` | Cruza ocupación con pagos y detecta infracciones. Registra el **último contacto de cada poste** (heartbeat) | Ocupación por lugar, pagos (patente, lugar, vencimiento), usuarios, infracciones, estado de los postes |
| Terminal del inspector | Se suscribe a `infracciones/zona`. `consultar(lugar)` | Muestra las infracciones de su zona | Últimas infracciones y último contacto de cada poste |

#### b. Conectores y acoplamiento

| Conector | Ref. | Temp. | Tipo | Por qué |
|---|---|---|---|---|
| Sensor → Poste | Acoplado | Acoplado | **Directa** (radio) | Es local a la cuadra y el evento es inmediato. Si el poste no está, no hay a quién guardarle nada |
| Poste → Cartel (vía gateway) | **Desacoplado** | Acoplado | **Pub/sub** | El cartel muestra varias cuadras. Así no necesita conocer a cada poste, y sumar un poste o un cartel no cambia a los demás |
| Poste → Nube | Acoplado | **Desacoplado** | **Mailbox / cola** | Si se cae el enlace, los eventos se encolan en el poste y se envían al reconectar. No se pierde nada |
| App → Nube | Acoplado | Acoplado | **Directa** (request/response, HTTPS) | El pago necesita una confirmación en el momento |
| Nube → Terminal | **Desacoplado** | Acoplado | **Pub/sub** | La nube publica las infracciones por zona y cada inspector se suscribe a la suya, sin que la nube sepa cuántos hay |
| Terminal → Nube | Acoplado | Acoplado | **Directa** | Para consultar un lugar puntual |

#### c. Ubicación y desconexión

| Capa | Componentes | Motivo |
|---|---|---|
| Edge | Sensores, postes, carteles | **Latencia:** un cambio de lugar llega al cartel en ms, sin pasar por la nube, y así se cumplen los 2 s. **Ancho de banda:** el poste agrega las lecturas y solo manda cambios |
| Fog | Gateway de zona | **Autonomía:** los carteles ven las cuadras vecinas aunque se caiga la nube. Sigue cumpliendo la latencia porque está en la zona |
| Cloud | Servidor | Vista **global** de la ciudad: pagos, usuarios, infracciones. No es urgente ni local |
| Dispositivos de usuario | App, terminal | Hablan con la nube por Internet (4G/5G) |

**El inspector consulta un auto con el poste desconectado de la nube.**

- **Cómo se detecta.** El servidor registra el **último contacto** de cada poste por heartbeat. Si pasa un timeout sin noticias, marca el poste como **desconectado**.
- **Qué ve el inspector.** No se le muestra un dato erróneo como si fuera actual. Ve la información marcada como *"Poste X sin conexión. Datos al hh:mm"*, con el último estado conocido. La terminal guarda ese último momento como referencia, y el inspector puede verificar en persona, porque está ahí.
- **Por qué los datos están desactualizados.**
  - **Pagos:** la nube los sigue teniendo al día, porque llegan por la app.
  - **Ocupación de esa cuadra:** está desactualizada desde el corte. Los autos que llegaron o se fueron después están en la cola del poste.
  - **Consecuencias:** puede haber falsos negativos, de autos que llegaron y no se ven, y falsos positivos, de lugares que se liberaron y la nube todavía cree ocupados.
- **Al reconectar.** El poste vacía su cola en orden, con los timestamps de cada evento. La nube actualiza la ocupación y recalcula las infracciones de ese período. Es **consistencia eventual**.
- **El trade-off es CAP.** Ante la partición se elige **disponibilidad**: el sistema sigue respondiendo y avisa que el dato puede estar viejo, en vez de bloquear la consulta.

## Ejercicio 6 — Teórica *(del resumen teórico, tapá la sección 9)*

Elegí **dos** y respondelas en ≤ 10 líneas cada una:
- Pregunta 7: relojes de Lamport vs vectoriales (¿qué no te garantiza C(a) < C(b)?).
- Pregunta 8: TrueTime y commit wait.
- Pregunta 2: PoW, ataque Sybil y 51 %.
