# Guía 8 — Arquitecturas

## Ej 1 — Diseñar escenarios (componentes, conectores, protocolos, niveles)
### a) 5 navegadores editan un documento compartido
### b) 10 búsquedas de alquileres; datos distribuidos en un datacenter
### c) Transferencia entre cuentas desde apps móviles

## Ej 2 — Compra de un e-book: interfaces, niveles, acoplamientos

## Ej 3 — Simulaciones atmosféricas con pub/sub
### 1. Diagrama
### 2. Event-based vs shared space
### 3. Notificaciones

## Ej 4 — Edificio inteligente (sensores, luces, middleware pub/sub)

**Supuestos:** la luminosidad exterior es la misma para todo el edificio (un solo sensor externo, o varios que publican lo mismo). Las luces son ON/OFF, sin intensidad.

**Componentes:** sensor de luminosidad externo, sensores de ocupación (uno por aula), **controlador de luces** (componente agregado), luces de cada aula y middleware pub/sub. **Todos se conectan solo al middleware**, ninguno conoce a los demás.

```
[Sensor luminosidad] ──pub──┐                 ┌──notif──▶ [Controlador]
                            ▼                 │               │
[Sensor ocup. aula X] ─pub─▶ [ Middleware pub/sub ] ◀──pub───────┘
                                              │
                                              └──notif──▶ [Luces aula X]
```

**Publicaciones y suscripciones.** Los publicadores mandan **valores** (atributo-valor) y los suscriptores filtran por **valor o rango**. El middleware hace el filtrado.

| Componente | Publica | Se suscribe a | Al recibir |
|---|---|---|---|
| Sensor de luminosidad | `(luminosidad=v)`, v en 0..100, periódico (~15 s) o solo cuando cambia de forma significativa | — | — |
| Sensor de ocupación aula X | `(aula=X, ocupacion=n)` cuando cambia n | — | — |
| Controlador | `(aula=X, luces=ON/OFF)` | `luminosidad` (todo el rango) y `ocupacion` de todas las aulas | actualiza su estado y reevalúa la regla de esa aula (o de todas, si cambió la luminosidad) |
| Luces aula X | — | `aula=X` (atributo-valor) sobre los comandos | prende o apaga |

**Regla del controlador:** guarda el último valor de luminosidad y la ocupación de cada aula, porque los eventos llegan por separado.
- `ocupacion(X) > 0` y `luminosidad < 30` → publica `(aula=X, luces=ON)`.
- `ocupacion(X) = 0` o `luminosidad ≥ 30` → publica `(aula=X, luces=OFF)`.

Se suscribe a **todo el rango** y no solo a `< 30` o `> 0`, porque necesita enterarse también de los eventos que apagan.

**¿Por qué un controlador y no luces "inteligentes"?** La condición combina **dos eventos** (ocupación **y** luminosidad), y una suscripción filtra un atributo por vez, así que alguien tiene que guardar estado y evaluar el "y". También podría hacerlo cada luz, suscrita a los dos eventos de su aula. Pero así la regla queda copiada en cada luz: cambiar el umbral o agregar un horario implica actualizarlas a todas, y cada luz necesita procesamiento. Con el controlador:
- la regla está en un solo lugar;
- las luces son actuadores tontos y baratos;
- se separan responsabilidades: los sensores miden, el controlador decide y las luces actúan.

El costo es que el controlador es un punto único de falla. Se mitiga replicándolo o con un default seguro en las luces (por ejemplo, quedarse encendidas si no reciben órdenes).

**¿Por qué las luces también van por el pub/sub y no conectadas directo al controlador?** Con conexión directa, el controlador tiene que conocer cada luz y la luz tiene que estar viva en el momento (acoplamiento referencial y temporal). Por pub/sub, el controlador publica para `aula=X` sin saber cuántas luces hay: agregar una luz es solo suscribirla.

## Ej 5 — Wrappers y broker
### a)
### b)
### c)

## Ej 6 — Transferencias sobre UDP: se pierde el 'OK'

## Ej 7 — Validaciones del formulario
### 1. Cliente vs servidor
### 2. Multi-tier

## Ej 8 — Sensores en un edificio de 5 pisos (WiFi + Bluetooth)
> **Overlay network:** red **lógica** montada sobre la física. Define quién considera vecino a quién a nivel aplicación; un enlace lógico puede ser varios saltos físicos. **AP** = access point (el "router WiFi").

**Supuestos:**
- El Bluetooth tiene **alcance corto** (~10 m): un sensor llega a los de su piso y a los del piso **adyacente** (2↔3, 3↔4), no a pisos más lejanos. Si solo llegara al mismo piso, los pisos 2–4 quedarían aislados y no habría solución.
- Algún sensor del **piso 1 tiene WiFi y Bluetooth**: es el **gateway** entre los dos mundos.

### 1. Overlay

**Overlay jerárquica con super peers:**
- **Pisos 0 y 1:** los sensores se conectan por WiFi al **AP**, que es el super peer raíz.
- **Pisos 2, 3 y 4:** cada piso tiene un **super peer**. Los sensores del piso son sus **hijos** (Bluetooth dentro del piso).
- **Columna vertical:** los super peers se encadenan por Bluetooth entre pisos adyacentes, hasta el gateway del piso 1 que lo pasa al AP.

```
          SP4 ── sensores piso 4
           │  (BT)
          SP3 ── sensores piso 3
           │  (BT)
          SP2 ── sensores piso 2
           │  (BT)
  gateway piso 1 (BT + WiFi)
           │  (WiFi)
          AP  ── sensores pisos 0 y 1 (WiFi)
```

**Punto débil:** es una **cadena**. Si cae el SP del piso 3, el piso 4 queda aislado. Se mitiga con más de un nodo puente por piso o eligiendo otro super peer cuando uno cae.

### 2. Intercambio de mensajes

Es un **pull por el árbol, con agregación de vuelta**:
1. El **AP** inicia el `pedido(id)`: lo manda a sus hijos WiFi y, por el gateway, a SP2.
2. Cada **super peer**, **en paralelo**:
   - reenvía el pedido a sus hijos del piso;
   - reenvía el pedido al super peer del piso de arriba.
3. Cada sensor responde a su super peer con sus datos.
4. Cada super peer espera las respuestas de sus hijos y el acumulado del piso de arriba, con un **timeout T**, y baja **un solo mensaje agregado**: los datos de su piso más los de los pisos superiores.
5. El AP termina con la información de toda la red.

Detalles:
- **En paralelo:** el tiempo total depende de la altura de la cadena, no de la suma de todo.
- **Timeout:** si un piso no contesta, se baja el resultado parcial marcando "sin respuesta del piso k". Una caída no bloquea todo.
- **Agregación:** ahorra mensajes en el Bluetooth, que es lento.
- **Alternativa push:** cada super peer empuja periódicamente sus datos hacia abajo. Da menos latencia al consultar, a cambio de tráfico constante.

### 3. Flooding / random walk vs anillo

El objetivo es **recuperar la información de toda la red**.

| | Flooding | Random walk | Anillo |
|---|---|---|---|
| **Cómo** | reenvía a **todos** los vecinos (TTL y descarte de duplicados) | reenvía a **un** vecino al azar | cada nodo conoce a su sucesor; el pedido da una vuelta juntando datos |
| **Mensajes** | muchísimos duplicados: `R(k)=d(d−1)^(k−1)` por salto | pocos | **exactamente N** |
| **¿Llega a todos?** | sí | **no garantizado** | sí, determinístico |
| **Latencia** | baja (avanza en paralelo) | alta | orden N (secuencial) |
| **Estructura** | ninguna: usa los vecinos físicos | ninguna | hay que mantenerla en altas y bajas |
| **Ante fallas** | muy robusto (otros caminos) | robusto | se corta la vuelta; se mitiga con una lista de sucesores |

**En esta red:**
- **Flooding** gasta mucha batería y Bluetooth en duplicados, pero no hay que mantener nada.
- **Random walk** sirve para *encontrar* algo, no para *juntar todo*: es la peor opción para este objetivo.
- **Anillo:** si el orden lógico no sigue la física, un salto lógico (por ejemplo, de piso 0 a piso 4) son varios saltos Bluetooth. Conviene armarlo **siguiendo los pisos**, y así queda casi la misma cadena del inciso 1.

**Conclusión:** para recolectar todo, anillo o jerarquía ganan en mensajes; flooding gana en robustez y simplicidad.

## Ej 9 — tar.gz de 1 TB en 100 servidores
### 1. Flooding
### 2. Random walk
### 3. Super peer

## Ej 10 — Aeropuerto con vehículos autónomos (cloud / fog / edge)
