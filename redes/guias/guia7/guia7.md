# Guía 7 — Seguridad

Notación: $E_Q(M)$ cifra, $D_Q(C)$ descifra, $H(M)$ hash, $K$ simétrica, $K_A^+$ pública de A, $K_A^-$ privada de A.

## Ej 1 — Cifrado César: estrategia para el desplazamiento
El César es una **sustitución monoalfabética con una rotación fija** $k$: cada letra se mapea siempre a la misma, y el orden se mantiene. Como el texto no tiene tildes, el alfabeto es de 26 letras y hay solo **25 claves posibles**.

1. **Fuerza bruta.** Probar los 25 desplazamientos y quedarse con el que da texto legible. Es viable porque el espacio de claves es chico.
2. **Análisis de frecuencias.** Como la sustitución es fija, el criptograma conserva las frecuencias del idioma. Se cuentan las letras: la más frecuente probablemente sea la cifrada de la **"e"**, que es la más común en inglés y en castellano, y el desplazamiento es la distancia entre ambas. Funciona mejor con textos largos; si falla, se prueba con la segunda más frecuente (t, a, o…).
3. **Patrones de palabras cortas.** Las palabras de 1 a 3 letras que se repiten suelen ser artículos o conectores ("the", "and", "a", "of" / "de", "la", "el"). En el criptograma hay una palabra de 3 letras que aparece varias veces: suponerla "the" da directamente $k$. También ayudan las letras dobles y la firma del final.
4. **Verificación.** Como el desplazamiento es único para todo el texto, el $k$ deducido de una sola letra se aplica a todo el criptograma. Si el resultado es legible, queda confirmado.

## Ej 2 — Confidencialidad + no repudio (esquema de cajas)
Pide **confidencialidad** (que solo B pueda leerlo) y **no repudio** (que B pueda probar que lo mandó A).

Regla: para probar quién sos usás **tu privada**; para que solo el otro lo lea usás **su pública**. Se asume que A tiene $K_B^+$ y B tiene $K_A^+$, y que ambos acuerdan los algoritmos (por ejemplo RSA + SHA-256).

### a)
| Cuadrado | Algoritmo | Casita (clave) | Salida |
|---|---|---|---|
| 1 | Hash $H$ | sin clave | $D = H(M)$ (message digest) |
| 2 | Cifrado asimétrico $E$ | $K_A^-$ (privada de A) | $F = E_{K_A^-}(D)$ (firma digital) |
| 3 | Cifrado asimétrico $E$ | $K_B^+$ (pública de B) | $C = E_{K_B^+}(M + F)$ (criptograma) |

1. A calcula el digest $D = H(M)$. Se firma el hash y no el documento porque es corto y de tamaño fijo, y la asimétrica es cara sobre datos largos.
2. A **firma** el digest con su privada: $F = E_{K_A^-}(H(M))$. Solo A tiene $K_A^-$, así que solo A pudo generar $F$ → **no repudio**.
3. A **cifra** documento y firma juntos con la pública de B: $C = E_{K_B^+}(M + F)$. Solo B tiene $K_B^-$ → **confidencialidad**.
4. A manda **solo $C$**. Ni el documento ni la firma viajan sueltos: en la red solo se ve el criptograma.

### b)
1. B **descifra** con su privada: $D_{K_B^-}(C) = M + F$. Ahora tiene el documento en claro y la firma.
2. B **descifra la firma** con la pública de A: $D' = D_{K_A^+}(F)$, que es el digest que calculó A.
3. B **calcula él mismo** el hash del documento recibido: $H(M)$. El hash no se invierte: se recalcula y se compara.
4. **Compara:** si $D_{K_A^+}(F) = H(M)$, entonces:
   - el documento no fue modificado → **integridad**;
   - la firma solo pudo generarla quien tiene $K_A^-$, o sea A → **autenticación y no repudio**. B puede guardar $M + F$ como prueba ante un tercero.

   Si no coinciden, el mensaje fue alterado o no lo firmó A, y se descarta.

## Ej 3 — Intercambio de claves públicas
### a) Cómo se vulnera si interceptan el intercambio
Con un ataque **man-in-the-middle**. Un atacante X se ubica entre A y B durante el intercambio de claves:

1. B le manda $K_B^+$ a A. X la intercepta y le entrega a A **su propia** $K_X^+$. En el otro sentido hace lo mismo: le da a B $K_X^+$ en lugar de $K_A^+$.
2. A cifra $E_{K_X^+}(M)$ creyendo que usa la clave de B.
3. X descifra con $K_X^-$. Ahora **lee** el mensaje, así que se rompe la confidencialidad, y además **puede modificarlo**.
4. X lo vuelve a cifrar con la verdadera $K_B^+$ y se lo reenvía a B. Lo mismo en el sentido B → A.
5. Ni A ni B detectan nada, porque todo descifra correctamente de su lado.

El problema de fondo es que **nada ata una clave pública a la identidad de su dueño**: A no puede distinguir $K_B^+$ de $K_X^+$.

### b) Certificados digitales
Un certificado es un documento firmado por una **Autoridad Certificante (CA)**, un tercero en el que todos confían, que **vincula una identidad con su clave pública**. En el estándar X.509 tiene:

- **Sujeto:** a quién pertenece (por ejemplo, B o `www.banco.com`).
- **Clave pública del sujeto:** $K_B^+$. Es lo que se certifica.
- **Emisor:** qué CA lo firmó.
- **Validez:** fechas desde / hasta.
- **Número de serie:** sirve para revocarlo.
- **Algoritmos** usados (por ejemplo, RSA + SHA-256).
- **Firma de la CA:** $F_{CA} = E_{K_{CA}^-}(H(\text{sujeto} + K_B^+ + \dots))$

Es decir, $Cert_B = (B;\ K_B^+;\ F_{CA})$.

**Cómo se usa.** B no manda su clave pública suelta: manda $Cert_B$. A lo verifica así:

1. **Firma:** comprueba que $D_{K_{CA}^+}(F_{CA}) = H(B + K_B^+ + \dots)$.
2. **Vigencia:** que esté dentro de las fechas y que no esté revocado (lista CRL u OCSP).
3. **Identidad:** que el sujeto sea efectivamente B, con quien A quiere hablar.

**De dónde sale $K_{CA}^+$:** ya está **instalada de antemano** en el sistema operativo o el navegador, o la carga a mano un administrador si la organización tiene su propia CA. Es la **raíz de confianza**: no viaja por la red, así que X no puede reemplazarla. Si hay CAs intermedias, se verifica la **cadena** hasta llegar a una raíz instalada.

**Por qué frena el ataque del a).** Si X reemplaza la clave:

- Si manda un certificado "B; $K_X^+$" hecho por él, no tiene $K_{CA}^-$ para firmarlo, así que la verificación de la firma falla.
- Si modifica un certificado real cambiándole la clave, la firma deja de coincidir con el hash del contenido.
- Si manda su propio certificado legítimo ("X; $K_X^+$"), A ve que el sujeto no es B y lo rechaza.

Mandar el certificado de B sin más no le sirve a X: el certificado es público, pero X no tiene $K_B^-$ para descifrar ni para firmar como B.

## Ej 4 — Handshake SSL/TLS
### a) Parámetro → etapa (HELLO / Key-Exchange / Data-sharing)
| Parámetro | Etapa | Por qué |
|---|---|---|
| Parámetros criptográficos | HELLO | Se negocian al inicio (tamaños de clave, parámetros del intercambio). |
| Valor al azar | HELLO y Key-Exchange | Cada lado manda su nonce ($R_C$, $R_S$) en el HELLO; en el Key-Exchange se usan para derivar la clave maestra, de modo que cada sesión tenga claves distintas (anti-replay). |
| Conjunto de algoritmos de encripción | HELLO | El cliente ofrece su lista de cipher suites y el servidor elige una. |
| Versión del protocolo | HELLO | Se acuerda la versión de SSL/TLS a usar. |
| Certificado del destinatario (peer) | Key-Exchange | El servidor manda su certificado, y el cliente saca de ahí $K_S^+$ para cifrar la pre-master. |
| Clave maestra (master key) | Key-Exchange | Cada lado la calcula por su cuenta: $master = f(PMS, R_C, R_S)$. |
| Criptograma | Data-sharing | Los datos de la aplicación viajan cifrados con la clave simétrica de sesión. |

### b) Diagrama de secuencia
Handshake con autenticación del servidor e intercambio de clave por RSA. Las líneas marcadas con (*) son opcionales y solo aparecen si el servidor también pide autenticar al cliente (TLS mutuo).

```
Cliente                                                      Servidor
   |                                                             |
   |  ===================== HELLO ============================  |
   |-- ClientHello: versión, cipher suites, R_C ---------------->|  en claro
   |<-- ServerHello: versión y suite elegidas, R_S --------------|  en claro
   |                                                             |
   |  ================== KEY-EXCHANGE ========================  |
   |<-- Certificate: Cert_S = (S; K+S; firma CA) ----------------|  en claro
   |<-- (*) CertificateRequest ----------------------------------|  en claro
   |<-- ServerHelloDone -----------------------------------------|  en claro
   |                                                             |
   |   cliente valida Cert_S con K+CA (firma, vigencia, nombre)  |
   |   y genera la pre-master secret (PMS) al azar               |
   |                                                             |
   |-- (*) Certificate: Cert_C --------------------------------->|  en claro
   |-- ClientKeyExchange: E_{K+S}(PMS) ------------------------->|  cifrado con la pública de S
   |-- (*) CertificateVerify: E_{K-C}(H(handshake)) ------------>|  firmado con la privada de C
   |                                                             |
   |   ambos: master = f(PMS, R_C, R_S) → claves de sesión       |
   |                                                             |
   |-- ChangeCipherSpec ---------------------------------------->|
   |-- Finished: MAC(todo el handshake) ------------------------>|  cifrado simétrico
   |<-- ChangeCipherSpec ----------------------------------------|
   |<-- Finished: MAC(todo el handshake) ------------------------|  cifrado simétrico
   |                                                             |
   |  ================== DATA-SHARING ========================  |
   |== datos de aplicación (por ej. HTTP): E_{K_sesión}(M)+MAC ==>|  criptogramas
   |<===========================================================|
```

**Qué viaja en claro y qué cifrado, y por qué**
- **En claro:** los HELLO, los certificados y el CertificateRequest. No son secretos: los certificados son públicos y los nonces solo tienen que ser únicos. Lo que se negocia en claro se protege al final con el `Finished`.
- **Cifrado asimétrico:** la PMS, con $K_S^+$ que sale del certificado. Solo el servidor verdadero la puede descifrar, así que un impostor no puede derivar las claves de sesión (esto **autentica al servidor** y da confidencialidad a la clave).
- **Firmado:** el CertificateVerify (solo en TLS mutuo). Prueba que el cliente tiene $K_C^-$, porque mandar el certificado solo no prueba nada.
- **Cifrado simétrico:** el `Finished` y todos los datos. El `Finished` lleva un MAC de todo el handshake, así se detecta si alguien modificó los mensajes en claro (por ejemplo, para forzar una suite débil).

**Por qué se pasa a simétrica:** es mucho más rápida que la asimétrica para volúmenes grandes de datos. Además, las claves de sesión son nuevas en cada conexión (dependen de $R_C$ y $R_S$), así que repetir mensajes grabados de otra sesión no sirve.

## Ej 5 — Autenticidad con un servicio (SSH / TLS)
### a) Autenticar clientes con SSH
Quien se autentica es **cada cliente**, y quien verifica es el **servidor**.

**Cuántas y dónde.** Con $N$ clientes $C_1 \dots C_N$:
- Cada cliente $C_i$ genera **su propio par** $(K_{C_i}^+, K_{C_i}^-)$. Son **$N$ pares** en total.
- Cada **privada** $K_{C_i}^-$ queda **solo en el equipo de $C_i$** y nunca sale de ahí.
- Las **$N$ públicas** $K_{C_i}^+$ se instalan **en el servidor**, cada una asociada a su usuario (en SSH, `~/.ssh/authorized_keys`). Tienen que cargarse por un **canal confiable**, por ejemplo copiadas por un administrador; si no, un atacante podría colar su propia pública (MITM, ej. 3).
- El servidor **no necesita una privada propia** para esto: solo verifica.

**Challenge-response.**
1. $C_i$ se conecta y dice quién es.
2. El servidor busca $K_{C_i}^+$ y le manda un **challenge** $R$: un número aleatorio grande y nuevo en cada intento, para que una respuesta grabada no sirva (anti-replay).
3. $C_i$ responde **firmándolo** con su privada: $E_{K_{C_i}^-}(R)$.
4. El servidor verifica que $D_{K_{C_i}^+}(E_{K_{C_i}^-}(R)) = R$. Como solo $C_i$ tiene $K_{C_i}^-$, queda autenticado.

Una variante equivalente es que el servidor mande $E_{K_{C_i}^+}(R)$ y $C_i$ devuelva $R$ descifrado con su privada. Así lo hacía SSHv1. En los dos casos se prueba la **posesión de la privada**.

### b) Autenticar el servidor

Es lo mismo que en a), pero al revés: ahora el que se autentica es el **servidor** y los que verifican son los **clientes**.

**Cuántas y dónde.**
- El servidor genera **un solo par** $(K_S^+, K_S^-)$.
- La **privada** $K_S^-$ vive **solo en el servidor**.
- La **pública** $K_S^+$ se instala **en cada uno de los $N$ clientes** (en SSH, `~/.ssh/known_hosts`).

Es el espejo de a): allá eran $N$ públicas en un servidor; acá es una pública copiada en $N$ clientes.

**Challenge-response.** El cliente manda un $R$ aleatorio, el servidor responde $E_{K_S^-}(R)$ y el cliente verifica que $D_{K_S^+}(\cdot) = R$. Si coincide, es el servidor verdadero: solo él tiene $K_S^-$.

**Cómo llega $K_S^+$ al cliente.** En SSH, la primera vez que te conectás a un host nuevo el cliente muestra el **fingerprint**, que es el hash de $K_S^+$, y pregunta si confiás. Si aceptás, la guarda en `known_hosts`, y en las conexiones siguientes la compara: si cambia, avisa.

Esa primera conexión es el punto débil. Si en ese momento hay un MITM, te guardás la clave del atacante. Para evitarlo, $K_S^+$ se preinstala por un canal confiable (por ejemplo, la carga un administrador) o se verifica el fingerprint por otro medio.

### c) Con certificado firmado por una CA
La autenticación pasa a hacerse con el **handshake SSL/TLS** del ej. 4b. Para autenticar también a los clientes se usa **TLS mutuo**: CertificateRequest → Certificate → CertificateVerify.

**Qué se instala en cada máquina**

| Dónde | Qué | Para qué |
|---|---|---|
| Todas (servidor y clientes) | Certificado de la CA, con $K_{CA}^+$ | Raíz de confianza: verificar cualquier certificado firmado por la CA |
| Servidor | Su par $(K_S^+, K_S^-)$ y $Cert_S = (S;\ K_S^+;\ E_{K_{CA}^-}(H(S + K_S^+)))$ | Presentarse en el handshake |
| Cada cliente $C_i$ | Su par $(K_{C_i}^+, K_{C_i}^-)$ y $Cert_{C_i} = (C_i;\ K_{C_i}^+;\ E_{K_{CA}^-}(H(C_i + K_{C_i}^+)))$ | Presentarse cuando el servidor lo pide |

Cada uno guarda **solo su propio certificado y su privada**. El certificado del otro **no se guarda de antemano**: llega en el handshake, y se verifica con $K_{CA}^+$ (firma, vigencia / no revocado, y que el nombre coincida).

**Cómo cambian a) y b)**
- **a) Autenticar clientes.** El servidor deja de guardar $N$ públicas sueltas y guarda **solo $K_{CA}^+$**.
  - Para verificar al cliente: el cliente manda $Cert_{C_i}$, el servidor lo valida con $K_{CA}^+$, y después comprueba con $K_{C_i}^+$ la firma del **CertificateVerify** $E_{K_{C_i}^-}(H(\text{handshake}))$. Esa firma es la que prueba que el cliente tiene la privada: mandar el certificado solo no prueba nada, porque es público.
  - Altas y bajas sin tocar el servidor: un usuario nuevo solo necesita que la CA le firme el certificado, y para dar de baja a uno se revoca su certificado (CRL / OCSP).
- **b) Autenticar el servidor.** Los clientes dejan de guardar $K_S^+$ en `known_hosts` y guardan **solo $K_{CA}^+$**.
  - Para verificar al servidor: el servidor manda $Cert_S$, el cliente lo valida, y le manda la pre-master cifrada con $K_S^+$. Solo el servidor verdadero puede descifrarla y terminar el handshake (`Finished`).
  - Desaparece el punto débil de la **primera conexión**: no hay que confiar a ciegas en un fingerprint, porque el certificado viene firmado por la CA.

En resumen, cada parte pasa de guardar una pública por cada entidad en la que confía a guardar **una sola, la de la CA**. Confía en la CA y, por transitividad, en todo lo que la CA firma.

## Ej 6 — Proxy HTTPS: autenticar usuarios

## Ej 7 — WiFi del hotel: autenticidad del proxy + confidencialidad

## Ej 8 — No repudio en mensajes internos

## Ej 9 — API Security First (integridad + no repudio, sin cifrar ni sesiones)
### 1. Qué tiene cada parte
### 2. URL
### 3. Qué hace cada parte
