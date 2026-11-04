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
### 1. Overlay
### 2. Intercambio de mensajes
### 3. Flooding / random walk vs anillo

## Ej 9 — tar.gz de 1 TB en 100 servidores
### 1. Flooding
### 2. Random walk
### 3. Super peer

## Ej 10 — Aeropuerto con vehículos autónomos (cloud / fog / edge)
