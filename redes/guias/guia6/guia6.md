## Ejercicio 1

### a)
corte 1

### b)
6? 7? algo de eso

### c)
con uno estoy creo, 443 para https

### d)
y bueno fijate

## Ejercicio 2

Consultas hechas el 01/11/2026 (con `Resolve-DnsName`, equivalente a `dig nombre TIPO`). Formato de un registro: `nombre TTL IN TIPO valor`.

### a) Registros A, CNAME y MX

| Dominio | A | CNAME | MX |
|---|---|---|---|
| www.dc.uba.ar | 157.92.27.128 (siguiendo la cadena) | www.dc.uba.ar → www-1.dc.uba.ar → dc.uba.ar | — (es un alias; el MX es el de dc.uba.ar) |
| dc.uba.ar | 157.92.27.128 | — | ASPMX.L.GOOGLE.COM y ALT1–4 (Google) |
| uba.ar | 45.60.86.78, 45.60.113.78 | — | uba-ar.mail.protection.outlook.com (Microsoft) |
| ar | — | — | — |
| . (raíz) | — | — | — |

- **CNAME**: `www.dc.uba.ar` es un **alias**; hay que seguir la cadena (`www` → `www-1` → `dc.uba.ar`) hasta llegar a un registro A.
- "—" = el nombre existe pero no tiene registros de ese tipo (la respuesta trae el SOA de la zona en AUTHORITY: respuesta vacía / NODATA).
- `ar` y la raíz no tienen IP ni mail: **solo delegan** (tienen NS). `uba.ar` tiene 2 registros A: varias IPs para el mismo nombre (round robin).

### b) Con `+trace`
`dig +trace` no usa el resolver: hace la resolución **iterativa** a mano desde la raíz, mostrando cada referral:

1. Raíz `.` (a–m.root-servers.net) → "preguntale a `ar`": NS a.lactld.org, c/d/e/f.dns.ar
2. `ar` → "preguntale a `uba.ar`": NS ns1.uba.ar, ns2.uba.ar (+ dns31–34.cloudns.net)
3. `uba.ar` → "preguntale a `dc.uba.ar`": NS ns-1/ns-2.dc.uba.ar, ns1/ns2(.fcen).uba.ar
4. `dc.uba.ar` (autoritativo) → la respuesta final: CNAMEs + A 157.92.27.128

Ningún servidor conoce todo, pero cada uno sabe a quién preguntarle: así se descentraliza la información.

### c) ¿Cómo se reconocen los autoritativos de una zona?
Son los que figuran en los **registros NS** de la zona. Para `dc.uba.ar`: ns-1.dc.uba.ar, ns-2.dc.uba.ar, ns1.uba.ar, ns2.uba.ar, ns1.fcen.uba.ar, ns2.fcen.uba.ar. Sus respuestas tienen el flag **aa** (authoritative answer); un resolver que responde desde caché no.

### d) ¿Cómo se distingue el primario de los secundarios?
Por el **registro SOA**: el primer nombre (MNAME) es el **primario**.

```
dc.uba.ar.  SOA  ns-2.dc.uba.ar.  admin.dc.uba.ar.  2026102300 ...
                 └─ primario      └─ mail admin (admin@dc.uba.ar)  └─ serial
```

El resto de los NS son **secundarios**: tienen una copia de la zona que traen del primario (transferencia de zona) cada *refresh*, y solo si el **serial** aumentó.

Dato real que apareció: distintas consultas devolvieron seriales distintos (2026102300 y 2026070703) → algún secundario (o una caché) todavía tenía una versión vieja de la zona. Eso es justamente lo que regulan refresh / retry / expire.

## Ejercicio 3

En HTTP/1.1 cada request es: línea de pedido (`MÉTODO ruta HTTP/1.1`), headers (**`Host` obligatorio**: permite virtual hosting, varios sitios en la misma IP) y una **línea en blanco** que marca el fin de los headers.

**El recurso `/`**
```
GET / HTTP/1.1
Host: www.dc.uba.ar
User-Agent: Mozilla/5.0
(línea en blanco)
```
→ `200 OK` con el HTML en el cuerpo.

**Encabezado del recurso `/tdc`**
```
HEAD /tdc HTTP/1.1
Host: www.dc.uba.ar
(línea en blanco)
```
→ mismos headers que un GET (`Content-Type`, `Content-Length`, `Last-Modified`…) pero **sin cuerpo**. Sirve para ver si existe, su tipo o tamaño sin bajarlo.

**`/logo.jpg` si no fue modificado desde una fecha** (GET condicional)
```
GET /logo.jpg HTTP/1.1
Host: www.dc.uba.ar
If-Modified-Since: Mon, 05 Oct 2026 12:00:00 GMT
(línea en blanco)
```
→ si **no** cambió: `304 Not Modified` sin cuerpo (se usa la copia en caché). Si cambió: `200 OK` con la imagen nueva. La fecha va en formato HTTP (GMT).

## Ejercicio 4

**Supuestos:**
- La cuenta del usuario es `usuario@gmail.com`, así que su Thunderbird tiene configurado como **servidor saliente** `smtp.gmail.com` (puerto 587, con autenticación).
- La PC usa como resolver el del ISP (`resolver-isp`). El servidor saliente usa el resolver interno de Google (`resolver-google`).
- Cachés vacías (lo dice el enunciado), HTTP/1.1 persistente, y todos los objetos de la página están en `www.smn.gov.ar`.
- Cada referral trae el **glue** (el A de los NS), así no hace falta resolver los nombres de los NS aparte.
- El MX de dc.uba.ar es `mx.dc.uba.ar`, dentro de la zona (en la realidad es Google, y eso sumaría consultas a la zona de google.com).

**Actores:** la PC solo tiene un *stub resolver*: le manda una consulta **recursiva** a `resolver-isp` y espera la respuesta final. Los resolvers hacen consultas **iterativas** desde el ancestro más cercano que tengan en caché (si no hay nada, desde la raíz).

### Conexiones TCP

| # | Entre | Protocolo de aplicación |
|---|---|---|
| 1 | PC ↔ www.smn.gov.ar (puerto 80) | HTTP (con 1.0 sería una conexión **por objeto** de la página) |
| 2 | PC (Thunderbird) ↔ smtp.gmail.com (587) | SMTP (autenticado) |
| 3 | smtp.gmail.com ↔ mx.dc.uba.ar (25) | SMTP |

**Mínimo 3.** La 3 no la abre la PC, pero la desencadena el envío del usuario.

### ¿Quiénes se comunican por UDP?
Solo los mensajes **DNS** (puerto 53):
- PC ↔ resolver-isp
- resolver-isp ↔ servidores raíz, `ar`, `gov.ar`, `smn.gov.ar`, `com`, `gmail.com`
- smtp.gmail.com ↔ resolver-google
- resolver-google ↔ servidores raíz, `ar`, `uba.ar`, `dc.uba.ar`

### Secuencia DNS

**Web:**

| # | De → A | Consulta | Tipo | Respuesta |
|---|---|---|---|---|
| 1 | PC → resolver-isp | `www.smn.gov.ar A?` | recursiva | |
| 2 | resolver-isp → raíz | `www.smn.gov.ar A?` | iterativa | referral: NS de `ar` + glue |
| 3 | resolver-isp → NS de `ar` | ídem | iterativa | referral: NS de `gov.ar` + glue |
| 4 | resolver-isp → NS de `gov.ar` | ídem | iterativa | referral: NS de `smn.gov.ar` + glue |
| 5 | resolver-isp → NS de `smn.gov.ar` | ídem | iterativa | **aa**: A de www.smn.gov.ar |
| 6 | resolver-isp → PC | | | A (no autoritativa) |

→ TCP + HTTP GET con la PC.

**Mail, tramo 1 (la PC encuentra a su servidor saliente):**

| # | De → A | Consulta | Tipo | Respuesta |
|---|---|---|---|---|
| 7 | PC → resolver-isp | `smtp.gmail.com A?` | recursiva | |
| 8 | resolver-isp → raíz | ídem | iterativa | referral: NS de `com` + glue |
| 9 | resolver-isp → NS de `com` | ídem | iterativa | referral: NS de `gmail.com` (ns1–4.google.com) + sus A |
| 10 | resolver-isp → NS de `gmail.com` | ídem | iterativa | **aa**: A de smtp.gmail.com |
| 11 | resolver-isp → PC | | | A |

Acá el resolver **vuelve a la raíz**: lo que tiene cacheado de la consulta web (`ar`, `gov.ar`, `smn.gov.ar`) no sirve para un nombre bajo `.com`. La caché solo ahorra pasos cuando los nombres comparten un ancestro (ej.: si después se pidiera `www.uba.ar`, arrancaría directo en los NS de `ar`).

→ TCP + SMTP entre la PC y el saliente (HELO, MAIL FROM, RCPT TO: …@dc.uba.ar, DATA…). El mail queda en la cola del saliente.

**Mail, tramo 2 (el saliente busca el MX del destino):**

| # | De → A | Consulta | Tipo | Respuesta |
|---|---|---|---|---|
| 12 | smtp.gmail.com → resolver-google | `dc.uba.ar MX?` | recursiva | |
| 13 | resolver-google → raíz | ídem | iterativa | referral: NS de `ar` |
| 14 | resolver-google → NS de `ar` | ídem | iterativa | referral: NS de `uba.ar` |
| 15 | resolver-google → NS de `uba.ar` | ídem | iterativa | referral: NS de `dc.uba.ar` + glue |
| 16 | resolver-google → NS de `dc.uba.ar` | ídem | iterativa | **aa**: MX `mx.dc.uba.ar` (+ su A en ADDITIONAL) |
| 17 | resolver-google → smtp.gmail.com | | | MX + A |

Si el A del servidor de mail no viniera en ADDITIONAL, haría falta una consulta más: `mx.dc.uba.ar A?`.

→ TCP + SMTP entre el saliente y `mx.dc.uba.ar`, que guarda el mail en el buzón del destinatario.

**Clave:** la consulta **MX** no la hace la PC sino el **servidor saliente**, cuando va a reenviar el mail. La PC solo necesita el A de su propio servidor saliente.

## Ejercicio 5

Casi todo request HTTP a un host nuevo arranca con una consulta DNS (nombre → IP), así que **la latencia de DNS se suma a la de HTTP**: el diseño de DNS afecta la performance web.

**Si DNS fuera centralizado** (un único servidor con toda la base):
- **Cuello de botella**: todas las consultas del mundo a un mismo lugar → colas y delay en *cada* resolución → cada carga de página tarda más.
- **Punto único de falla**: si se cae, no se resuelve ningún nombre → la web deja de andar (los servidores HTTP están vivos, pero nadie puede llegar a ellos por nombre).
- **Distancia**: para la mayoría estaría lejos → RTT alto en cada consulta.
- **Mantenimiento**: una sola base gigante, actualizada por un solo administrador (el problema del viejo `hosts.txt`).

**Si DNS no tuviera caché:**
- Cada resolución recorrería la jerarquía entera (raíz → TLD → … → autoritativo): **varios RTTs extra por cada host**, y otra vez para cada página aunque sea el mismo sitio.
- La raíz y los TLD recibirían todo el tráfico de Internet → se saturarían.
- Una página con objetos en varios hosts (CDN, ads, etc.) pagaría esa resolución completa para cada uno.

**Si DNS fuera orientado a conexión** (por ejemplo sobre TCP):
- Cada consulta sumaría un **handshake** (+1 RTT) antes de preguntar, y en una resolución iterativa eso se multiplica por cada servidor consultado.
- Además, los servidores tendrían que mantener estado por cada conexión (más carga). Para un intercambio de 1 pregunta y 1 respuesta corta, UDP alcanza: si se pierde, el resolver simplemente reintenta.

**¿Y con SMTP?** El razonamiento es el mismo: el servidor saliente necesita DNS (MX + A del destino) antes de cada envío, así que un DNS lento, caído o sin caché también demora o impide el envío. La diferencia es que el mail es **asincrónico**: el saliente encola y reintenta, y a nadie le importa si el mail tarda unos segundos (o minutos) más. El impacto **percibido** es mucho menor que en la web, donde el usuario espera la página en tiempo real. Lo único crítico sería la caída total: sin DNS no se puede encontrar el MX y el mail queda en cola hasta que vuelva.

## Ejercicio 6

**Supuestos:** el DNS de www.fcen.uba.ar ya está resuelto, todos los objetos están en el mismo host, cada archivo entra en 1 RTT (lo dice el enunciado), conexiones secuenciales (no paralelas). Para HTTP/1.1 se calculan los dos casos: con y sin pipelining.

**Objetos que se descargan automáticamente** (al parsear el HTML):

| # | Objeto | Origen en el HTML |
|---|---|---|
| 1 | el HTML base | el GET inicial |
| 2 | `style.css` | `<link rel="stylesheet" href="style.css">` |
| 3 | `searchline.png` | `<img src="searchline.png">` |
| 4 | `home.png` | `<img src="home.png">` (aunque esté dentro de un `<a>`, la imagen se dibuja igual) |
| 5 | `search_icon.gif` | `<input type="image" src="search_icon.gif">` (la imagen del botón de buscar) |

**No se descargan**: `avsearch.php` (`<a href>`, requiere clic) y `search` (`<form action>`, requiere submit).

Cada objeto cuesta: **1 RTT** de handshake TCP (SYN → SYN+ACK) + **1 RTT** de GET → respuesta. Los objetos embebidos recién se pueden pedir después de recibir y parsear el HTML.

| Modo | Cálculo | Total |
|---|---|---|
| **HTTP/1.0** (no persistente: 1 conexión TCP por objeto) | 5 objetos × 2 RTT | **10 RTT** |
| **HTTP/1.1 persistente, sin pipelining** | 2 RTT (handshake + HTML) + 4 × 1 RTT (un GET por vez sobre la misma conexión) | **6 RTT** |
| **HTTP/1.1 persistente, con pipelining** | 2 RTT (handshake + HTML) + 1 RTT (los 4 GET en ráfaga, las 4 respuestas vuelven juntas) | **3 RTT** |

Nota: si en HTTP/1.0 el navegador abriera las 4 conexiones de los objetos **en paralelo**, serían 2 + 2 = 4 RTT. Si no se resolvió el DNS antes, se suma la resolución al principio.


## Ejercicio 7

ok vamos a ver si entiendo
PC <-> stub resolver, una recursiva a uba.ar, el resolver stub consulta al isp, y el isp ya tiene cacheado la dirección del ns de uba.ar, entonces busca directo el mx, recibe mailserver.uba.ar, busca el A? de mailserver.uba.ar, recibe una IP 208.25.19.2.

para milagros.dc.uba.ar: el resolver no sabe nada de dc.uba.ar, así que le pregunta `milagros.dc.uba.ar A?` (iterativa) al ancestro más cercano que conoce, servidores.uba.ar. Como dc.uba.ar está delegado, servidores.uba.ar no es autoritativo y responde con un **referral** en una sola respuesta: `dc.uba.ar NS servidores.dc.uba.ar` + el glue `servidores.dc.uba.ar A 208.190.1.4`. De ahí el resolver le pregunta `milagros.dc.uba.ar A?` a 208.190.1.4, que responde autoritativamente 208.190.1.15.

Cacheado queda mailserver.uba.ar A, milagros.dc.uba.ar A, y el mx de uba.ar. También servidores.dc.uba.ar A. Y dc.uba.ar NS.

## Ejercicio 8

En criollo, se mandan headers de MIME, con su versión y formato que viene. Con el content-type sabemos que tipo de archivo viene, y el cte sabemos en que formato viene, para saber como decodificar la cadena ascii que vino. SMTP no cambia porque no se entera, solo lee el base64. después, con los headers de mime, cada cliente se encarga de pasar el base a lo que tenga que ser.

## Ejercicio 9

HTTP reusa los **tipos MIME** en el header `Content-Type` para decir qué es el contenido. A diferencia del mail, HTTP puede llevar binario en el cuerpo, así que el archivo va tal cual (sin base64 ni `Content-Transfer-Encoding`). `MIME-Version` es de mail: en HTTP no se usa.

**1. Persona A sube un paper (POST):**
```
POST /uploads HTTP/1.1
Host: archivos.uba.ar
Content-Type: application/pdf
Content-Length: 4096
(línea en blanco)
<4096 bytes del PDF>
```
Respuesta:
```
HTTP/1.1 201 Created
Location: /uploads/29837293
Content-Type: application/json
Content-Length: 31
(línea en blanco)
{"ok": true, "id": 29837293}
```
`201 Created` + `Location` le dice al cliente dónde quedó el recurso. El JSON con el id es opcional; si va, la respuesta lleva su propio `Content-Type: application/json`.

Otros tipos según lo que se comparta: datos → `text/csv`, software → `application/zip`, imagen → `image/png`.

**2. Persona B pregunta el tipo (HEAD):**
```
HEAD /uploads/29837293 HTTP/1.1
Host: archivos.uba.ar
(línea en blanco)
```
Respuesta: **solo headers, sin cuerpo**. El tipo viene en `Content-Type`:
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 4096
(línea en blanco)
```

**3. Persona B lo descarga (GET):**
```
GET /uploads/29837293 HTTP/1.1
Host: archivos.uba.ar
(línea en blanco)
```
Respuesta: los mismos headers que el HEAD, más el cuerpo:
```
HTTP/1.1 200 OK
Content-Type: application/pdf
Content-Length: 4096
(línea en blanco)
<4096 bytes del PDF>
```
Con el `Content-Type` el navegador sabe qué hacer con el archivo (abrirlo con el visor de PDF, descargarlo, etc.).

## Ejercicio 10

### a)

**Supuestos:** spameitor y smtp.unaempresadespam.com.ar usan como resolver a `dns-1.unaempresadespam.com.ar`. Todas sus consultas son **recursivas** a dns-1, que las responde **desde su caché** (enunciado: "rara vez faltan en caché") → respuestas **no autoritativas**, sin consultas iterativas a la raíz ni a los autoritativos. Asumo que el A de cada servidor de mail viene en la sección ADDITIONAL de la respuesta MX; si no, es una consulta `A?` más por dominio (también cache hit).

**1. spameitor → su servidor saliente.** spameitor ya tiene la lista de destinatarios; solo necesita la IP de su servidor SMTP:

| # | De → A | Consulta | Respuesta |
|---|---|---|---|
| 1 | spameitor → dns-1 | `smtp.unaempresadespam.com.ar A?` (recursiva) | A (caché, no autoritativa) |

**2. El saliente → cada dominio destino.** Para entregar cada mail necesita el MX del dominio del destinatario y la IP de ese servidor de mail. Una consulta por **dominio distinto** (bob, alice y trudy @uba.ar comparten MX):

| # | De → A | Consulta | Respuesta |
|---|---|---|---|
| 2 | smtp → dns-1 | `uba.ar MX?` (recursiva) | MX + A del servidor de mail (caché) |
| 3 | smtp → dns-1 | `dc.uba.ar MX?` (recursiva) | MX + A (caché) |
| 4 | smtp → dns-1 | `dm.uba.ar MX?` (recursiva) | MX + A (caché) |
| 5 | smtp → dns-1 | `df.uba.ar MX?` (recursiva) | MX + A (caché) |

**Total:** 5 consultas (9 si los A de los servidores de mail no vienen en ADDITIONAL). Después el saliente abre TCP + SMTP con cada servidor de mail.

### b)
**Supuestos:** el mail (con el HTML adentro) ya llegó al cliente del destinatario por SMTP + IMAP/POP3; el HTML **no** viaja por HTTP. Al abrirlo, el cliente dibuja el HTML y pide por HTTP/1.1 los recursos que se cargan **automáticamente**. Ejemplo para el destinatario bob@uba.ar.

**Recursos que se piden solos** (dos `<img>`, en dos hosts distintos → 2 conexiones TCP, con su DNS previo):

**1. La imagen de ofertas**
```
GET /ofertas.png HTTP/1.1
Host: www.unaempresadespam.com.ar
User-Agent: Thunderbird
(línea en blanco)
```
```
HTTP/1.1 200 OK
Content-Type: image/png
Content-Length: 48213
(línea en blanco)
<bytes del PNG>
```

**2. El pixel de rastreo (tracker)**
```
GET /count.php?CampaignID=10057&Email=bob@uba.ar HTTP/1.1
Host: tracker.unaempresadespam.com.ar
User-Agent: Thunderbird
(línea en blanco)
```
```
HTTP/1.1 200 OK
Content-Type: image/gif
Content-Length: 43
(línea en blanco)
<bytes de una imagen mínima>
```
No es una imagen real sino un **pixel de rastreo**: al pedirlo, el servidor registra que **ese mail fue abierto y por quién** (la dirección va en la URL). Un `.php` puede responder `image/gif` porque el tipo lo decide el servidor con `Content-Type`, no la extensión. Por eso muchos clientes bloquean las imágenes remotas por defecto.

## Ejercicio 11

**Supuestos**
- HTTP/1.1 con conexiones persistentes. Una conexión TCP por host.
- La PC tiene un **stub resolver** que hace consultas **recursivas** a su resolver. El resolver hace consultas **iterativas** y arranca con la caché vacía; lo que va aprendiendo no expira.
- Las zonas akamai.com y spameitor.com no se dan: sus NS e IPs son supuestos (`x.x.x.x`).

**Ojo con el archivo de zona.** Es la zona de **jmail.com**, y los nombres sin punto final son relativos a ella:
- `ads` es `ads.jmail.com`, no `ads.spameitor.com`.
- `cdn.akamai.com` (sin punto) es `cdn.akamai.com.jmail.com`.

Además, ns.jmail.com no es autoritativo para akamai.com ni para spameitor.com. Por eso **esos registros no se usan** para resolver lo que pide el HTML. (Lo normal sería al revés: `recursos.jmail.com CNAME cdn.akamai.com`.)

Tampoco se usan MX, mailserver ni elmailserver: es webmail y la bandeja viene dentro del HTML.

### 1. www.jmail.com → HTML

**DNS**

| # | De → A | Tipo | Mensaje |
|---|---|---|---|
| 1 | PC → resolver | recursiva | `www.jmail.com A?` |
| 2 | resolver → raíz | iterativa | `www.jmail.com A?` |
| 3 | raíz → resolver | referral | AUTHORITY: NS de `com.` · ADDITIONAL: A de esos NS (glue) |
| 4 | resolver → NS de com | iterativa | `www.jmail.com A?` |
| 5 | NS de com → resolver | referral | AUTHORITY: `jmail.com NS ns.jmail.com` · ADDITIONAL: `ns.jmail.com A 208.190.1.26` (glue) |
| 6 | resolver → ns.jmail.com | iterativa | `www.jmail.com A?` |
| 7 | ns.jmail.com → resolver | **autoritativa (aa)** | ANSWER: `www.jmail.com A 208.190.1.20` |
| 8 | resolver → PC | respuesta | `www.jmail.com A 208.190.1.20` (el resolver la guarda en caché) |

**TCP #1** con 208.190.1.20:80 (3-way handshake), y después:
```
GET / HTTP/1.1
Host: www.jmail.com
User-Agent: Firefox
(línea en blanco)
```
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 712
(línea en blanco)
<html> ... (el HTML del enunciado)
```

El navegador parsea el HTML. Se cargan solos el `<img>` y el `<iframe>`. Los `<button>` no generan pedidos sin un clic.

### 2. Logo: cdn.akamai.com

**DNS.** El resolver ya tiene en caché los NS de `com.`, así que **no vuelve a la raíz**:

| # | De → A | Tipo | Mensaje |
|---|---|---|---|
| 1 | PC → resolver | recursiva | `cdn.akamai.com A?` |
| 2 | resolver → NS de com | iterativa | `cdn.akamai.com A?` |
| 3 | NS de com → resolver | referral | NS de akamai.com + glue |
| 4 | resolver → NS de akamai.com | iterativa | `cdn.akamai.com A?` |
| 5 | NS de akamai.com → resolver | autoritativa (aa) | `cdn.akamai.com A x.x.x.x` (supuesto) |
| 6 | resolver → PC | respuesta | `cdn.akamai.com A x.x.x.x` |

**TCP #2** con x.x.x.x:80, y después:
```
GET /el-logo-de-jmail.png HTTP/1.1
Host: cdn.akamai.com
Referer: http://www.jmail.com/
(línea en blanco)
```
```
HTTP/1.1 200 OK
Content-Type: image/png
Content-Length: 15320
(línea en blanco)
<bytes del PNG>
```

### 3. Publicidad: ads.spameitor.com (iframe)

**DNS.** Igual que el paso 2: PC → resolver (recursiva), luego resolver → NS de com (de caché) → referral a los NS de spameitor.com, y por último NS de spameitor.com → `ads.spameitor.com A y.y.y.y` (aa, supuesto).

**TCP #3** con y.y.y.y:80, y después:
```
GET / HTTP/1.1
Host: ads.spameitor.com
Referer: http://www.jmail.com/
(línea en blanco)
```
```
HTTP/1.1 200 OK
Content-Type: text/html
Content-Length: 2048
(línea en blanco)
<html> ... (la publicidad)
```

El iframe es **otra página HTML**: si referencia más recursos, el navegador los pide igual que en el paso 1 (más DNS, y más TCP por cada host nuevo). Como no conocemos ese HTML, asumimos que no trae nada más.

### Conexiones TCP

**3**: una por host (www.jmail.com, cdn.akamai.com, ads.spameitor.com). El DNS va por **UDP** y no cuenta. Con HTTP/1.0 serían también 3, porque hay un solo objeto por host; si hubiera varios objetos en el mismo host, 1.0 abriría una conexión por objeto.