# Guía 6 — Mensajes

## Ejercicio 1 (resuelto por Claude, de ejemplo)

```go
type Cmd = string   // "Next" o "Count"

// a) servidor
func Srv(ch chan Cmd) {
    int cant = 0
    while true {
        Cmd msg = receive(ch)
        if msg == "Next" {
            cant = cant + 1
        } else {            // "Count"
            print(cant)
            cant = 0
        }
    }
}

// b) cliente
func Client(n int, ch chan Cmd) {
    while true {
        for i in range(n) {
            send(ch, "Next")
        }
        send(ch, "Count")
    }
}

// c) main
func main() {
    (channel Cmd) ch = create(channel Cmd, 0)   // sincrónico
    process Srv(ch)
    process Client(3, ch)
    process Client(5, ch)
}
// sin deadlock: el server siempre vuelve a receive y los clientes solo hacen send
// ojo: los Next de los dos clientes se mezclan en el canal -> el número impreso no es "el de un cliente"
```

## Ejercicio 2

```go
type Cmd struct {
    tipo string           // "Next" o "Count"
    resp chan int         // nil en los Next
}

func Srv(ch chan Cmd) {
    int cant = 0
    while true {
        Cmd msg = receive(ch)
        if msg.tipo == "Next" {
            cant = cant + 1
        } else {
            send(msg.resp, cant)   // responde por el canal que vino en el mensaje
            cant = 0
        }
    }
}

func Client(n int, ch chan Cmd) {
    (channel int) miResp = create(channel int, 0)   // uno por cliente, se crea una vez
    while true {
        for i in range(n) {
            send(ch, Cmd{"Next", nil})
        }
        send(ch, Cmd{"Count", miResp})
        int c = receive(miResp)    // se bloquea hasta que el server responde
        print(c)
    }
}

func main() {
    (channel Cmd) ch = create(channel Cmd, 0)
    process Srv(ch)
    process Client(3, ch)
    process Client(5, ch)
}
// sin deadlock: el cliente ya está esperando en receive(miResp) cuando el server hace send
```

## Ejercicio 3

```go
func Srv(ch1 chan int, ch2 chan int) {
    while true {
        int a = receive(ch1)
        int b = receive(ch2)
        if a == b {
            print("coinciden")
        } else {
            print("no coinciden")
        }
    }
}

func Cliente(ch chan int) {
    while true {
        send(ch, randInt(10))
    }
}

func main() {
    (channel int) ch1 = create(channel int, 0)
    (channel int) ch2 = create(channel int, 0)
    process Srv(ch1, ch2)
    process Cliente(ch1)
    process Cliente(ch2)
}
// sin deadlock: cada cliente solo hace send a su canal y el server alterna receive en ambos
```


## Ejercicio 4

```go
// a) un servidor, un cliente
func Server(intentos chan int, respuestas chan bool) {
    int secreto = randInt(11)          // [0,10]
    bool acerto = false
    while !acerto {
        int x = receive(intentos)
        acerto = (x == secreto)
        send(respuestas, acerto)
    }
}

func Cliente(intentos chan int, respuestas chan bool) {
    int x = 0
    bool acerto = false
    while !acerto {
        send(intentos, x)
        acerto = receive(respuestas)
        x = x + 1
    }
    print("adiviné!")
}

func main() {
    (channel int) intentos = create(channel int, 0)
    (channel bool) respuestas = create(channel bool, 0)
    process Server(intentos, respuestas)
    Cliente(intentos, respuestas)
}
// sin deadlock: el cliente siempre hace send y después receive; el server, receive y después send
```

```go
// b) varios clientes en secuencia
func Server(intentos chan int, respuestas chan bool) {
    while true {                        // atiende un juego tras otro
        int secreto = randInt(11)
        bool acerto = false
        while !acerto {
            int x = receive(intentos)
            acerto = (x == secreto)
            send(respuestas, acerto)
        }
    }
}

// Cliente igual que en a)

func main() {
    (channel int) intentos = create(channel int, 0)
    (channel bool) respuestas = create(channel bool, 0)
    process Server(intentos, respuestas)
    Cliente(intentos, respuestas)       // sin process: main espera a que termine
    Cliente(intentos, respuestas)
    Cliente(intentos, respuestas)
}
```

```go
// c) opción 1: un solo server, cada intento lleva el canal de respuesta del cliente
type Intento struct {
    x    int
    resp chan bool
}

func Server(intentos chan Intento) {
    map[chan bool]int secretos = {}           // canal del cliente -> su número
    while true {
        Intento m = receive(intentos)
        if !contains(secretos, m.resp) {      // cliente nuevo
            secretos[m.resp] = randInt(11)
        }
        bool acerto = (m.x == secretos[m.resp])
        if acerto {
            delete(secretos, m.resp)
        }
        send(m.resp, acerto)
    }
}

func Cliente(intentos chan Intento) {
    (channel bool) miResp = create(channel bool, 0)
    int x = 0
    bool acerto = false
    while !acerto {
        send(intentos, Intento{x, miResp})
        acerto = receive(miResp)
        x = x + 1
    }
    print("adiviné!")
}

func main() {
    (channel Intento) intentos = create(channel Intento, 0)
    process Server(intentos)
    process Cliente(intentos)
    process Cliente(intentos)
    process Cliente(intentos)
}
```

```go
// c) opción 2: un proceso por cliente, que juega el 4a con él
type Juego struct {
    intentos   chan int
    respuestas chan bool
}

// Server y Cliente del 4a, sin cambios

func Lobby(pedidos chan Juego) {
    while true {
        Juego j = receive(pedidos)
        process Server(j.intentos, j.respuestas)   // un server propio para este cliente
    }
}

func Jugador(pedidos chan Juego) {
    (channel int) intentos = create(channel int, 0)
    (channel bool) respuestas = create(channel bool, 0)
    send(pedidos, Juego{intentos, respuestas})
    Cliente(intentos, respuestas)
}

func main() {
    (channel Juego) pedidos = create(channel Juego, 0)
    process Lobby(pedidos)
    process Jugador(pedidos)
    process Jugador(pedidos)
    process Jugador(pedidos)
}
// sin deadlock en ambas: cada cliente hace send y después receive de su propio canal,
// y del otro lado siempre hay alguien que recibe y contesta
```


## Ejercicio 5

```go
func AsyncChan(entrada chan any, salida chan any) {
    any[] cola = []
    while true {
        (channel any) out = nil            // cola vacía -> el case de envío queda deshabilitado
        any primero = nil
        if len(cola) > 0 {
            out = salida
            primero = cola[0]              // se calcula afuera: el select evalúa el valor aunque el canal sea nil
        }
        select {
        case any x = receive(entrada):
            cola = append(cola, x)
        case send(out, primero):
            cola = cola[1:]
        }
    }
}

func main() {
    (channel any) entrada = create(channel any, 0)   // solo canales sincrónicos
    (channel any) salida = create(channel any, 0)
    process AsyncChan(entrada, salida)
    // productores: send(entrada, v) nunca se bloquea más que un instante
    // consumidores: receive(salida) se bloquea solo si la cola está vacía
}
```

## Ejercicio 6 (sobre el 4c opción 1, canales asincrónicos)

```go
type Intento struct {
    x    int
    resp chan Respuesta
}

type Respuesta struct {
    x      int             // a qué intento corresponde
    acerto bool
}

func Server(intentos chan Intento) {
    map[chan Respuesta]int secretos = {}
    map[chan Respuesta]bool ganadores = {}      // a estos no se les contesta más
    while true {
        Intento m = receive(intentos)
        if !contains(ganadores, m.resp) {
            if !contains(secretos, m.resp) {
                secretos[m.resp] = randInt(11)
            }
            bool acerto = (m.x == secretos[m.resp])
            if acerto {
                delete(secretos, m.resp)
                ganadores[m.resp] = true        // no se borra: si no, un intento tardío arranca otro juego
            }
            send(m.resp, Respuesta{m.x, acerto})
        }
    }
}

func Cliente(intentos chan Intento) {
    (channel Respuesta) miResp = create(channel Respuesta, 11)
    for x in range(11) {                        // manda todo sin esperar respuestas
        send(intentos, Intento{x, miResp})
    }
    Respuesta r = receive(miResp)
    while !r.acerto {
        r = receive(miResp)
    }
    print("adiviné el", r.x)
}

func main() {
    (channel Intento) intentos = create(channel Intento, 100)
    process Server(intentos)
    process Cliente(intentos)
    process Cliente(intentos)
}
// sin deadlock: los send son a canales con buffer; el cliente siempre recibe un true
// porque alguno de 0..10 es el secreto, y los intentos posteriores se ignoran
// (con la opción 2 sale gratis: el server de ese cliente termina y nadie lee lo que sobra)
```

## Ejercicio 7 (a y b, misma solución)

```go
type Pedido struct {
    tipo  string     // "Leer" o "Escribir"
    valor int        // solo si escribe
    resp  chan int   // siempre: el server contesta con el valor actual
}

func Variable(pedidos chan Pedido, inicial int) {
    int v = inicial
    while true {
        Pedido p = receive(pedidos)
        if p.tipo == "Escribir" {
            v = p.valor
        }
        send(p.resp, v)                 // confirma lectura y escritura
    }
}

func leer(pedidos chan Pedido, miResp chan int) int {
    send(pedidos, Pedido{"Leer", 0, miResp})
    return receive(miResp)
}

func escribir(pedidos chan Pedido, miResp chan int, x int) {
    send(pedidos, Pedido{"Escribir", x, miResp})
    receive(miResp)                     // espera a que se haya aplicado
}

func Cliente(pedidos chan Pedido) {
    (channel int) miResp = create(channel int, 0)
    while true {
        int x = leer(pedidos, miResp)
        escribir(pedidos, miResp, x + 1)    // ojo: leer + escribir NO es atómico
    }
}

func main() {
    (channel Pedido) pedidos = create(channel Pedido, 0)
    process Variable(pedidos, 0)
    process Cliente(pedidos)
    process Cliente(pedidos)
}
// exclusión: un solo proceso toca v y atiende un pedido por vuelta
// b) asincrónico: sigue siendo correcta porque toda operación espera su confirmación
// sin deadlock: el cliente siempre está en receive(miResp) cuando el server hace send
```

## Ejercicio 8 (resuelto por Claude)

```go
type unit = struct{}

// a) lista fija de canales
func Timer(t int, chans []chan unit) {
    while true {
        Sleep(t)
        for ch in range(chans) {
            send(ch, unit{})            // canales asincrónicos: no se traba con un cliente lento
        }
    }
}

func main() {
    (channel unit) ch1 = create(channel unit, 10)
    (channel unit) ch2 = create(channel unit, 10)
    (channel unit) ch3 = create(channel unit, 10)
    (channel unit) ch4 = create(channel unit, 10)
    process Timer(100, []chan unit{ch1, ch2, ch3, ch4})
}
```

```go
// b) los clientes se registran en cualquier momento
func Timer(t int, registro chan (chan unit)) {
    []chan unit chans = []
    (channel unit) tick = Ticker(t)     // canal que recibe un valor cada t ms
    while true {
        select {
        case chan unit nuevo = receive(registro):
            chans = append(chans, nuevo)
        case receive(tick):
            for ch in range(chans) {
                send(ch, unit{})
            }
        }
    }
}

func Cliente(registro chan (chan unit)) {
    (channel unit) miTick = create(channel unit, 10)
    send(registro, miTick)
    while true {
        receive(miTick)
        // hacer algo en cada tick
    }
}

func main() {
    (channel (chan unit)) registro = create(channel (chan unit), 10)
    process Timer(100, registro)
    process Cliente(registro)
    process Cliente(registro)
}
// select: no puede quedarse en Sleep porque un registro puede llegar en cualquier momento
// Ticker y no After dentro del loop: After se reiniciaría con cada registro y atrasaría los ticks
```

## Ejercicio 9

```go
// a)
func T(deC chan string, aR chan string) {
    while true {
        string m = receive(deC)
        send(aR, codificar(m))
    }
}
// orden preservado: un solo proceso, un mensaje por vuelta
```

```go
// b) un solo canal: texto o cambio de destino, el orden FIFO se mantiene
type Msg struct {
    tipo    string        // "Texto" o "Cambio"
    texto   string        // si es Texto
    destino chan string   // si es Cambio
}

func T(deC chan Msg) {
    (channel string) aR = nil           // el cliente siempre arranca con un Cambio
    while true {
        Msg m = receive(deC)
        if m.tipo == "Cambio" {
            aR = m.destino
        } else {
            send(aR, codificar(m.texto))
        }
    }
}
```

```go
// c) claves de K, pedidas por adelantado
func T(deC chan Msg, pedidosK chan (chan string)) {
    (channel string) miClave = create(channel string, 1)   // buffer 1: K deja la clave y sigue
    (channel string) aR = nil
    send(pedidosK, miClave)             // primera clave por adelantado
    while true {
        Msg m = receive(deC)
        if m.tipo == "Cambio" {
            aR = m.destino
        } else {
            string clave = receive(miClave)     // casi siempre ya está
            send(pedidosK, miClave)             // pido la próxima antes de seguir
            send(aR, codificar(m.texto, clave))
        }
    }
}
// nunca hay más de un pedido pendiente -> el buffer de 1 alcanza y K nunca se bloquea
```
