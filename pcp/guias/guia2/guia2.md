# Guía 2: Semáforos

## Ejercicio 1

Se deben garantizar las relaciones de precedencia `A → F` y `F → C`. Para
ello se utilizan dos semáforos, ambos inicializados sin permisos:

```java
Semaphore semA = new Semaphore(0);
Semaphore semF = new Semaphore(0);
```

`semA` indica que ya se imprimió `A`, mientras que `semF` indica que ya se
imprimió `F`.

```text
thread T1 {
    print(A)
    semA.release()

    print(B)

    semF.acquire()
    print(C)
}

thread T2 {
    print(E)

    semA.acquire()
    print(F)
    semF.release()

    print(G)
}
```

De esta manera, `T2` no puede imprimir `F` hasta que `T1` haya impreso `A`, y
`T1` no puede imprimir `C` hasta que `T2` haya impreso `F`.


## Ejercicio 2

Las únicas salidas posibles deben ser `ACERO` y `ACREO`. En ambas, primero
se imprime `A`, luego `C`, después `E` y `R` en cualquier orden y, finalmente,
`O`.

Se utilizan tres semáforos, todos inicializados sin permisos:

```java
Semaphore semA = new Semaphore(0);
Semaphore semC = new Semaphore(0);
Semaphore semE = new Semaphore(0);
```

```C#
thread T1 {
    semA.acquire()
    print(C)
    semC.release()

    print(E)
    semE.release()
}

thread T2 {
    print(A)
    semA.release()

    semC.acquire()
    print(R)

    semE.acquire()
    print(O)
}
```

`semA` garantiza que `A` se imprima antes que `C`, y `semC` garantiza que
`C` se imprima antes que `R`. Como `E` aparece después de `C` dentro de `T1`,
`E` y `R` pueden ejecutarse en cualquier orden. Por último, `semE` garantiza
que `O` se imprima después de `E`; por el orden interno de `T2`, también se
imprime después de `R`.


## Ejercicio 3

Se debe garantizar la secuencia `R I O OK OK OK`. No importa el orden relativo
entre los tres `OK`, porque todos imprimen lo mismo, pero ninguno puede aparecer
antes de `O`.

Se utilizan tres semáforos, todos inicializados sin permisos:

```java
Semaphore semR = new Semaphore(0);
Semaphore semI = new Semaphore(0);
Semaphore semOK = new Semaphore(0);
```

```text
thread T1 {
    print(R)
    semR.release()

    semOK.acquire()
    print(OK)
}

thread T2 {
    semR.acquire()
    print(I)
    semI.release()

    semOK.acquire()
    print(OK)
}

thread T3 {
    semI.acquire()
    print(O)
    semOK.release(3)

    semOK.acquire()
    print(OK)
}
```

`semR` garantiza que `I` se imprima después de `R`, mientras que `semI`
garantiza que `O` se imprima después de `I`. Una vez impresa `O`, `T3` libera
los tres permisos necesarios para que cada thread pueda imprimir su `OK`.


## Ejercicio 4

Cada desigualdad puede garantizarse usando un semáforo que contabilice cuántas
veces se imprimió el carácter que debe aparecer primero. Los tres semáforos se
inicializan sin permisos:

```java
Semaphore semA = new Semaphore(0);
Semaphore semE = new Semaphore(0);
Semaphore semG = new Semaphore(0);
```

```text
thread T1 {
    while (true) {
        print(A)
        semA.release()

        print(B)

        semG.acquire()
        print(C)
        print(D)
    }
}

thread T2 {
    while (true) {
        print(E)
        semE.release()

        semA.acquire()
        print(F)

        print(G)
        semG.release()
    }
}

thread T3 {
    while (true) {
        semE.acquire()
        print(H)
        print(I)
    }
}
```

Cada impresión de `F` consume un permiso producido por una impresión previa de
`A`, por lo que `#F ≤ #A`. De la misma manera, `semE` garantiza `#H ≤ #E` y
`semG` garantiza `#C ≤ #G`.

## Ejercicio 5

### a)

Se utilizan dos semáforos cruzados. Ambos comienzan con un permiso, de modo que
cualquiera de los threads puede imprimir primero:

```java
Semaphore semA = new Semaphore(1);
Semaphore semB = new Semaphore(1);
```

```text
thread T1 {
    while (true) {
        semB.acquire()
        print(A)
        semA.release()
    }
}

thread T2 {
    while (true) {
        semA.acquire()
        print(B)
        semB.release()
    }
}
```

Después de imprimir, cada thread habilita una impresión del otro. Así, ninguno
puede adelantarse en más de una impresión y se garantiza `|#A - #B| ≤ 1`.

### b)

Para obtener únicamente la secuencia `A B A B A B...`, se utiliza el mismo
código, pero se cambian los valores iniciales:

```java
Semaphore semA = new Semaphore(0);
Semaphore semB = new Semaphore(1);
```

Como `T1` adquiere `semB`, es el único que puede comenzar. Después de imprimir
`A` habilita a `T2`, que imprime `B` y vuelve a habilitar a `T1`.

### c)

Para obtener únicamente la secuencia `A B B A B B...`, se mantienen los
valores iniciales del punto anterior y `T2` imprime dos veces antes de habilitar
nuevamente a `T1`:

```text
thread T1 {
    while (true) {
        semB.acquire()
        print(A)
        semA.release()
    }
}

thread T2 {
    while (true) {
        semA.acquire()
        print(B)
        print(B)
        semB.release()
    }
}
```

## Ejercicio 6

buscamos sumar N primeros impares
"impar" es nuestro contador
suma es el acumulador.

Tenemosdos threads, generador que mueve el contador (impar = i, cuando acumulador deba sumar el i-esimo numero impar) y acumulador, que computa cual es y lo acumula e suma. 

me piden que lo implemente en java, lo voy a escribir en pseudo y que lo revise claude en java.

globales
```java
impar = N
suma = 0

puedoSumar = new Sem(0)    // generador -> acumulador: "ya puse el numero"
nuevoNumero = new Sem(0)   // acumulador -> generador: "ya lo sume, pone otro"

thread generador {
    for (i = N; i >= 1; i--) {
        impar = i                // primero pongo el valor (asi tambien se suma el N)
        puedoSumar.release()
        nuevoNumero.acquire()    // espero que lo sume; en la ultima vuelta, que termino todo
    }
    print(suma)
}

thread acumulador {
    for (k = 0; k < N; k++) {    // N vueltas fijas: no leo impar para saber cuando parar
        puedoSumar.acquire()
        suma += 2*impar - 1
        nuevoNumero.release()
    }
}
```

## Ejercicio 7

### a)

Agentes activos: los **clientes**, uno por thread. Cada uno recorre su rutina,
que es una secuencia finita de pasos `(aparato, k)`: usar ese aparato con `k`
discos.

Recursos compartidos:

- Los **4 aparatos**: cada uno lo usa un cliente a la vez. Un semáforo por
  aparato, `aparatos[i] = Sem(1)`.
- Los **discos** del depósito: son todos iguales, así que alcanza con contarlos.
  `discos = Sem(D)`.

Suposiciones:

- El enunciado no da la cantidad de discos, pero dice que hay un lugar destinado
  a su almacenamiento, así que son finitos: hay `D` en total.
- Ningún paso de una rutina pide más de `D` discos (si no, ese cliente nunca
  podría cargar el aparato).
- Un cliente usa un aparato a la vez, y al terminar descarga **todos** sus discos
  antes de pasar al siguiente paso (lo exige el gimnasio, aun si vuelve a usar el
  mismo aparato).

### b)

Idea: primero se toma el **aparato** y después los **discos**. Los `k` discos se
toman de a uno, pero bajo `mutexDiscos`, para que dos clientes no se queden cada
uno con una parte de lo que necesitan.

Se utiliza un semáforo por aparato, uno que cuenta los discos del depósito y
un mutex para tomar los discos:

```java
Semaphore[] aparatos = new Semaphore[4];       // cada uno new Semaphore(1, true)
Semaphore discos = new Semaphore(D);
Semaphore mutexDiscos = new Semaphore(1, true);
```

Cada cliente recorre su rutina, donde cada paso es `(aparato, k)`:

```text
thread Cliente(rutina) {
    for ((aparato, k) in rutina) {
        aparatos[aparato].acquire()

        mutexDiscos.acquire()          // tomo los k discos "de una"
        for (j = 0; j < k; j++) {
            discos.acquire()
        }
        mutexDiscos.release()

        entrenar()

        for (j = 0; j < k; j++) {      // descargo los discos (sin mutex)
            discos.release()
        }
        aparatos[aparato].release()
    }
}
```

**Exclusión mutua:**

- Aparatos: `aparatos[i]` arranca en 1, así que por el invariante
  `#usando(i) + aparatos[i].V = 1` hay a lo sumo un cliente en cada aparato.
- Discos: `discos.V = D − #discosEnUso ≥ 0`, así que nunca hay más de `D` discos
  cargados.

**Sin deadlock:**

- Tomar los discos de a uno **sin** mutex daría deadlock. Por ejemplo, con
  `D = 4`, A y B piden 3 cada uno, toman 2 cada uno, y los dos esperan un disco
  que tiene el otro. Con `mutexDiscos`, un solo cliente a la vez está juntando
  discos, así que nunca hay dos pedidos a medias.
- El orden es aparato → discos. Al revés, un cliente podría tener discos y
  esperar un aparato que tiene otro cliente, que a su vez espera esos discos.
- Todo cliente que tiene discos ya tiene todo lo que necesita (su aparato y sus
  `k` discos), así que termina de entrenar y los devuelve. Entonces el que tiene
  `mutexDiscos` y espera discos eventualmente los consigue, porque `k ≤ D`.
- Devolver los discos **no** pide `mutexDiscos`. Si lo pidiera, habría deadlock:
  el que tiene el mutex espera discos, y el que los quiere devolver espera el
  mutex.
- Un cliente nunca tiene dos aparatos a la vez: suelta todo antes del siguiente
  paso. Así que entre aparatos no hay retención y espera, y no puede haber ciclo.

**Sin livelock:** todas las esperas son `acquire` bloqueantes y nadie suelta un
recurso para reintentar, así que no hay threads que se pasen la vida
reintentando sin avanzar.

### c)

La solución está libre de inanición, porque `aparatos[i]` y `mutexDiscos` son
**fuertes** (FIFO). Suponemos que `entrenar()` siempre termina. Un cliente
puede quedar esperando en tres lugares:

1. **En `aparatos[i].acquire()`:** el que tiene el aparato lo suelta en un tiempo
   finito (consigue sus discos por el punto 3 y termina de entrenar). Como el
   semáforo es FIFO, antes que él pasan como mucho los que ya estaban en la
   cola, así que eventualmente lo consigue.
2. **En `mutexDiscos.acquire()`:** el que tiene el mutex lo suelta cuando junta
   sus `k` discos, que pasa en un tiempo finito por el punto 3. Como el mutex es
   FIFO, también le llega el turno.
3. **En `discos.acquire()`:** ahí espera a lo sumo un cliente, el que tiene
   `mutexDiscos`. Mientras lo tiene, nadie más puede tomar discos. Los que están
   entrenando terminan y devuelven los suyos, así que el depósito solo se va
   llenando. Como `k ≤ D`, en algún momento junta los `k`.

Que `discos` sea fuerte o débil no importa: como mucho hay un thread esperando
ahí, así que no tiene contra quién perder.

**Si los semáforos fueran débiles** (`new Semaphore(1)`), sí podría haber
inanición. Por ejemplo, con el aparato 0 débil, cada vez que A lo suelta, B lo
vuelve a tomar antes que C (barging), y así para siempre. Lo mismo pasa con
`mutexDiscos`. Se resuelve como hicimos acá: `new Semaphore(1, true)` para los
aparatos y para `mutexDiscos`.

## Ejercicio 8

Es un productor-consumidor con dos diferencias: la capacidad de la bolsa es la
cantidad de generadores que están jugando, así que cambia mientras corre el juego,
y los consumidores sacan de a pares.

Suposición: cada participante es un thread que entra al juego, juega una
cantidad arbitraria de rondas y se va. Como no se conoce la cantidad de
participantes, pueden entrar y salir en cualquier momento.

```java
Semaphore bolitas = new Semaphore(0);   // bolitas en la bolsa (notEmpty)
Semaphore lugares = new Semaphore(0);   // lugares libres (notFull); arranca en 0 porque no hay generadores
Semaphore mutexC = new Semaphore(1);    // un consumidor a la vez juntando su par
```

```text
thread Generador {
    lugares.release()          // entro: la bolsa acepta una bolita más
    while (sigoJugando) {
        lugares.acquire()      // espero lugar libre
        poner bolita, sumar punto
        bolitas.release()
    }
    lugares.acquire()          // me voy: la capacidad baja 1
}

thread Consumidor {
    while (sigoJugando) {
        mutexC.acquire()       // tomo el par "de una"
        bolitas.acquire()
        bolitas.acquire()
        mutexC.release()
        lugares.release()      // un lugar por cada bolita que saqué
        lugares.release()
        sumar punto
    }
}
```

Cómo cierran las cuentas de `lugares`:

- Por la capacidad: `+1` cuando entra un generador y `−1` cuando se va.
- Por cada bolita: `−1` cuando un generador la pone y `+1` cuando un consumidor
  la saca.

**Nunca hay más bolitas que generadores.** Sea `G` la cantidad de generadores
jugando, `B` las bolitas en la bolsa, `H` las bolitas en manos de un consumidor
(que todavía no devolvió sus lugares) y `R` los generadores que ya tomaron un
lugar y todavía no pusieron la bolita. Vale el invariante:

`lugares.V = G − B − H − R`

Como `lugares.V ≥ 0`, sale que `B ≤ G`. La parte clave es la salida: un
generador que se va tiene que llevarse un lugar libre. Si la bolsa está llena,
espera a que un consumidor saque un par, así que irse nunca rompe el invariante.

**Sin deadlock (con 2 o más generadores jugando):**

- Si los consumidores tomaran las bolitas de a una sin `mutexC`, podría haber
  deadlock. Por ejemplo, con 2 generadores la bolsa tiene 2 bolitas, C1 toma
  una, C2 toma la otra, y `lugares = 0` porque los lugares se devuelven recién
  después del par. Los consumidores esperan su segunda bolita y los generadores
  esperan lugar. Con `mutexC`, a lo sumo un consumidor tiene un par a medias, o
  sea `H ≤ 1`.
- Supongamos que están todos bloqueados. El consumidor que tiene `mutexC` espera
  bolitas, así que `B = 0`. Los generadores están bloqueados en `lugares`, así
  que `R = 0`. Entonces `lugares.V = G − H ≥ 2 − 1 = 1`, y algún generador
  podría pasar su `lugares.acquire()`. Absurdo.
- Con un solo generador sí hay deadlock, y por eso el enunciado pide 2 o más. La
  capacidad es 1, así que nunca hay 2 bolitas en la bolsa. El consumidor con
  `mutexC` se queda con una bolita esperando la segunda, y el generador espera
  un lugar que nunca se libera.


## Ejercicio 9

### a)
```
int n;
Sem sentados = new Semaphore(0)
Sem llegada = new Semaphore(0)
Sem bajados = new Semaphore(0)
Sem[] subirse = { new Semaphore(n), new Semaphore(0) }
int direccionActual = 0;
```


```java
Thread transbordador {
    run() {
        while (true) {
            for (i : 0..n) sentados.acquire()
            //Estamos todos, zarpamos
            direccionActual = (direccionActual+1)%2
            // ... viajamo
            for (i : 0..n) llegada.release()
            //bajense TODOS
            for (i : 0..n) bajados.acquire()
            //subanse todos
            for (i : 0..n) subirse[direccionActual].release()
        }
    }
}
```

```java
Thread persona(direccion) {
    // asumo que cada persona no loopea, se sube y se baja..
    run() {
        subirse[direccion].acquire()
        // se subió
        sentados.release()
        //se sentó, espera a que llegue
        llegada.acquire()
        // llegamos, se baja
        bajados.release()
        // listo
    }
}
```

### b)
Creo que es hasta más simple

```
int n;
Sem sentados = new Semaphore(0)
Sem[] llegada = { new Semaphore(0), new Semaphore(0) }
Sem[] subirse = { new Semaphore(n), new Semaphore(0) }
int direccionActual = 0;
```


```java
Thread transbordador {
    run() {
        while (true) {
            for (i : 0..n) sentados.acquire()
            //Estamos todos, zarpamos
            direccionActual = (direccionActual+1)%2
            // ... viajamo
            for (i : 0..n) llegada[direccionActual].release()
        }
    }
}
```

```java
Thread persona(direccion) {
    // asumo que cada persona no loopea, se sube y se baja..
    run() {
        int destino = (direccion+1)%2
        subirse[direccion].acquire()
        // se subió
        sentados.release()
        //se sentó, espera a que llegue
        llegada[destino].acquire()
        // llegamos, se baja
        subirse[destino].release()
        // listo
    }
}
```

## Ejercicio 10

Globales
```
Sem[] mutexCargar = 8x new Semaphore(1, true)
Sem[] quiereCargar = 8x new Semaphore(0)
Sem[] terminoCargar = 8x new Semaphore(0)

Sem[] mutexDescargar = 8x new Semaphore(1, true)
Sem[] quiereDescargar = 8x new Semaphore(0)
Sem[] terminoDescargar = 8x new Semaphore(0)
```

```
Thread maquina(i) {
    while (true) {
        // espero a quien descargue
        quiereDescargar[i].acquire()
        // descargo...
        terminoDescargar[i].release()

        // proceso ...

        // espero a que alguien quiera cargar
        quiereCargar[i].acquire()
        // cargo...
        terminoCargar[i].release()
        // he cargado

    }
}
```

```java
Thread vehiculo(pasos) {
    cargar(maquina) {
        // YO voy a cargar
        mutexCargar[maquina].acquire()

        // hola vengo a cargar
        quiereCargar[maquina].release()
        // cuando termine de cargar avisame
        terminoCargar[maquina].acquire()

        //listo puede cargar otro
        mutexCargar[maquina].release()
    }

    descargar(maquina) {
        //lo mismo pero con descargar
    }

    run() {
        while(pasos.length) {
            Paso paso = pasos.shift(); // ponele ni idea es pseudocódigo
            // no tienen sincronización, van y cargan o descargan gratis
            if (paso.lugar is PLATAFORMA) continue;
            if (paso.accion == CARGA) cargar(paso.maquina);
            if (paso.accion == DESCARGA) descargar(paso.maquina);
        }
    }
}
```

## Ejercicio 11

### a)

```
Sem toilettesMultiplex = new Semaphore(8);
Sem resource = new Semaphore(1);
Sem mutexCantPersonas = new Semaphore(1);
int cantPersonas = 0;
```

```
Thread persona() {
    mutexCantPersonas.acquire()
    cantPersonas++
    if (cantPersonas == 1){
        resource.acquire()
    }
    mutexCantPersonas.release()

    toilettesMultiplex.acquire()
    //mear idfk
    toilettesMultiplex.release()

    mutexCantPersonas.acq()
    cantPersonas--
    if (cantPersonas == 0){
        resource.release()
    }
    mutexCantPersonas.release()
}
```

```
Thread personal() {
    resource.acquire()
    // limpiar
    resource.release()
}
```

### b)
Agregaríamos un turnstile fuerte; en persona es instant relase, en personal es release despues del acquire de resource. queda así.
```
Thread persona() {
    turnstile.acquire()
    turnstile.release()

    mutexCantPersonas.acquire()
    cantPersonas++
    if (cantPersonas == 1){
        resource.acquire()
    }
    mutexCantPersonas.release()

    toilettesMultiplex.acquire()
    //mear idfk
    toilettesMultiplex.release()

    mutexCantPersonas.acq()
    cantPersonas--
    if (cantPersonas == 0){
        resource.release()
    }
    mutexCantPersonas.release()
}
```

```
Thread personal() {
    tursntile.acquire()
    resource.acquire()
    turnstile.release()
    // limpiar
    resource.release()
}
```

### c)

```java
Thread persona() {
    //hay toilette disponible?
    toilettesMultiplex.acquire()

    turnstile.acquire()
    turnstile.release()
    
    // si lo hay arrancas a contar como persona en el baño. caso contrario ni te gastes
    // en intentar reservar el resource.
    mutexCantPersonas.acquire()
    cantPersonas++
    if (cantPersonas == 1){
        resource.acquire()
    }
    mutexCantPersonas.release()
    //mear idfk
    mutexCantPersonas.acq()
    cantPersonas--
    if (cantPersonas == 0){
        resource.release()
    }
    mutexCantPersonas.release()

    toilettesMultiplex.release()
}
```

```java
Thread personal() {
    tursntile.acquire()
    resource.acquire()
    turnstile.release()
    // limpiar
    resource.release()
}
```

## Ejercicio 12
Saldungaray, once again.

Esto es un lightswitch por lado, o Barrera como le ponen ellos en saldungaray
el b es agregar un multiplex de 3 (por lado? maybe?)
el c es volver fuerte el mutiplex, creería? tendría que programarlo para verlo.


### a)

Globales
```
Sem resource = new Sem(1);
int[] cantCruzando = { 0, 0 }
Sem[] mutexCantCruzando { new Sem(1), new Sem(1) }
```

```java
Thread vehiculo(dir) {
    run() {
        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]++;
        if (cantEsperando[dir] == 1) {
            resource.acquire();
        }
        mutexCantCruzando[dir].release()

        // cruzo...

        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]--;
        if (cantEsperando[dir] == 0) {
            resource.release()
        }
        mutexCantCruzando[dir].release()
    }
}
```

### b)

```
Sem resource = new Sem(1);
int[] cantCruzando = { 0, 0 }
Sem[] mutexCantCruzando = { new Sem(1), new Sem(1) }
Sem multiplexCantidad = new Sem(3)
```

```java
Thread vehiculo(dir) {
    run() {
        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]++;
        if (cantCruzando[dir] == 1) {
            resource.acquire();
        }
        mutexCantCruzando[dir].release()

        multiplexCantidad.acquire()
        // cruzo
        multiplexCantidad.release()

        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]--;
        if (cantCruzando[dir] == 0) {
            resource.release()
        }
        mutexCantCruzando[dir].release()
    }
}
```

### c)
Evitamos inanición de dos cosas
1. de que el lado contrario nunca pase (molinete)
2. de que uno del lado válido se quede permanentemente esperando

entonces ponemos fuerte el multiplex mas un turnstile.

```
Sem resource = new Sem(1);
int[] cantCruzando = { 0, 0 }
Sem[] mutexCantCruzando = { new Sem(1), new Sem(1) }
Sem multiplexCantidad = new Sem(3, true)
Sem turnstile = new Sem(1, true)
```

```java
Thread vehiculo(dir) {
    run() {
        turnstile.acquire()

        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]++;
        if (cantCruzando[dir] == 1) {
            resource.acquire();
        }
        mutexCantCruzando[dir].release()
        turnstile.release()

        multiplexCantidad.acquire()
        // cruzo
        multiplexCantidad.release()

        mutexCantCruzando[dir].acquire()
        cantCruzando[dir]--;
        if (cantCruzando[dir] == 0) {
            resource.release()
        }
        mutexCantCruzando[dir].release()
    }
}
```