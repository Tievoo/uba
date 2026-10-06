# Guía 3: Monitores

## Ejercicio 1

### a)

El problema es que **el `signal` no tiene memoria**. Si nadie está esperando en
`permiso`, el `signal` no hace nada y se pierde (a diferencia de un semáforo, que
guardaría el permiso). Con "signal y espera urgente", si `importante` ya estaba
esperando, el orden sale bien: el `signal` le pasa el monitor en el acto. Pero si
el `signal` llega **antes** que el `wait`, falla.

Traza (T1 ejecuta `antesydespues`, T2 ejecuta `importante`):

| Paso | T1 | T2 | Cola de `permiso` |
|---|---|---|---|
| 1 | entra al monitor, ejecuta `antes` | | vacía |
| 2 | `permiso.signal()`: no hay nadie esperando, no pasa nada | | vacía |
| 3 | ejecuta `despues` y sale | | vacía |
| 4 | | entra, `permiso.wait()` | T2 |
| 5 | | queda esperando para siempre | T2 |

El orden fue `antes → despues`, `importante` no se ejecuta nunca y T2 queda
bloqueado. No se cumple `antes → importante → despues`.

### b)

Es peor. Además de la traza anterior, que falla igual, ahora falla también el
caso en el que T2 ya estaba esperando: quien hace el `signal` después de
`antes` **sigue** directo a `despues`, sin ceder el monitor.

1. T2 entra y hace `permiso.wait()`.
2. T1 ejecuta `antes` y `permiso.signal()`. T2 pasa a estar listo, pero T1
   conserva el monitor.
3. T1 ejecuta `despues` y sale.
4. T2 vuelve a entrar y ejecuta `importante`.

El orden queda `antes → despues → importante`, así que con "signal y continúa"
**nunca** se obtiene el orden pedido.

Para arreglarlo no alcanza con un `while` y una variable en `importante` (eso
solo resuelve el `signal` perdido): además, T1 tendría que **esperar** a que
termine `importante` antes de ejecutar `despues`, con otra condición y otra
variable.


## Ejercicio 2

```java
Monitor secuenciadorTernario {
    status = 0 // 0 primer, 1 segundo, 2 tercero
    Condition[] conds = { Condition, Condition, Condition }
    Func[] funciones = { primero, segundo, tercero }

    ejecutarInstruccion(n) {
        while (status != n) {
            wait(conds[n]);
        }

        funciones[n]()

        int next = (n+1)%3
        status = next
        signal(conds[next])
    }
}

```

## Ejercicio 3


### a)
```java
Monitor barrera(n) {
    threadsEsperando = 0;
    Condition esperando = new Condition()

    esperar() {
        threadsEsperando++;
        if (threadsEsperando == n) signalAll(esperando);
        while (threadsEsperando < n) wait(esperando);
    }
}
```

### b)

Resetear el contador en el `signalAll` no alcanza. Con Mesa, los despertados
vuelven a chequear `while (threadsEsperando < n)`, ven 0 y se vuelven a dormir.
Incluso el último, después de resetear, cae en su propio `while` y se duerme.
Bajar el contador después del `wait` tampoco sirve: el primero en salir lo deja
en `n−1`, y los demás, al rechequear, se vuelven a dormir.

El truco es no esperar sobre el contador, sino sobre **"¿terminó mi ronda?"**.
Se agrega un número de `fase`. Cada thread anota en qué fase llegó, y el último
en llegar avanza la fase, resetea el contador y despierta a todos:

```java
Monitor barrera(n) {
    threadsEsperando = 0;
    fase = 0;
    Condition esperando = new Condition()

    esperar() {
        int miFase = fase;
        threadsEsperando++;
        if (threadsEsperando == n) {
            threadsEsperando = 0;
            fase++;
            signalAll(esperando);
        } else {
            while (fase == miFase) wait(esperando);
        }
    }
}
```

- Resetear `threadsEsperando` ya no afecta a los que esperan, porque ellos miran
  `fase`.
- Si un thread rápido sale y vuelve a llamar a `esperar()` antes de que los demás
  salgan, anota la fase **nueva** y cuenta para la ronda siguiente, sin pisar la
  anterior.
- `fase` cumple el rol del segundo molinete de la barrera con semáforos.


## Ejercicio 4

### a)
```java
Monitor Atrapador {
    Condition atrapado = new Condition();
    aLiberar = 0;
    atrapados = 0;

    esperar() {
        atrapados++;
        while (aLiberar == 0) {
            wait(atrapado);
        }
        aLiberar--;
        atrapados--;
    }

    liberar(N) {
        if (atrapados - aLiberar < N) return;
        aLiberar += N;
        signalAll(atrapado)
    }
}
```

En mi solución, un thread que no esperó si puede pasar directamente. Se podrían implementar tickets con el objetivo de que cada thread tenga su número especifico y nadie se cuele. Entonces en vez de revisar si aLiberar es 0, chequea si aLiberar es mayor a su ticket, que sumó cuando entró. Algo así

```java
Monitor Atrapador {
    Condition atrapado = new Condition();
    aLiberarHasta = 0;
    proximoTicket = 0;

    esperar() {
        int miTicket = proximoTicket++;
        while (miTicket >= aLiberarHasta) {
            wait(atrapado);
        }
    }

    liberar(N) {
        if (proximoTicket - aLiberarHasta < N) return;
        aLiberarHasta += N;
        signalAll(atrapado)
    }
}
```

### b)

Partimos de la versión con tickets del (a). Ahora `liberar(N)` se bloquea hasta
que haya al menos `N` threads esperando sin liberar, y recién ahí los libera a
todos juntos.

Guardar el `N` en una variable global ("target") se rompe si hay varios
`liberar` esperando a la vez con `N` distintos. No hace falta: el `N` es un
parámetro, o sea local a cada liberador. Cada vez que llega un thread a
`esperar()`, avisa a todos los liberadores con `signalAll`, y cada uno rechequea
**su propio** `N` en un `while`.

```java
Monitor Atrapador {
    Condition atrapado = new Condition();
    Condition puedoLiberar = new Condition();
    aLiberarHasta = 0;
    proximoTicket = 0;

    esperar() {
        int miTicket = proximoTicket++;
        signalAll(puedoLiberar);         // llegó uno más: los liberadores rechequean
        while (miTicket >= aLiberarHasta) {
            wait(atrapado);
        }
    }

    liberar(N) {
        while (proximoTicket - aLiberarHasta < N) {
            wait(puedoLiberar);
        }
        aLiberarHasta += N;              // libera los N más viejos, todos juntos
        signalAll(atrapado);
    }
}
```

- Si dos liberadores con el mismo `N` se despiertan a la vez y hay justo `N`
  esperando, el monitor los hace entrar de a uno. El primero suma `N` y libera.
  El segundo rechequea, ve que ya no alcanza y se vuelve a dormir. Para eso
  tiene que ser un `while`.
- `signalAll(puedoLiberar)` y no `signal`, porque puede haber varios
  liberadores con `N` distintos, y no sabemos a cuál le alcanza.
- Entre liberadores puede haber inanición: un `liberar(10)` puede esperar para
  siempre si siempre llegan `liberar(2)` que se llevan a los atrapados antes de
  que se junten 10. Si se quiere que sea justo, se puede armar una cola (o
  tickets) de liberadores, atendidos en orden de llegada: al llegar a
  `esperar()` se mira solo el primero de la cola, a ver si ya le alcanza.


## Ejercicio 5

### a)

```java
Monitor Pelu {
    int clientesEsperando = 0;
    Condition condPeluquero = new Condition();
    Condition esperandoCorte = new Condition();
    int llamados = 0;
    int terminados = 0;
    Condition corteTerminado = new Condition();

    // Dominio del peluquero
    empezarCorte() {
        while(clientesEsperando == 0) {
            wait(condPeluquero)
        }
        clientesEsperando--;
        llamados++;
        signal(esperandoCorte);
    }
    terminarCorte() {
        terminados++;
        signal(corteTerminado);
    }

    // Dominio del cliente
    cortarseElPelo() {
        clientesEsperando++;
        signal(condPeluquero);
        while (llamados == 0){
            wait(esperandoCorte);
        }
        llamados--;
        // se corta el pelo
        while (terminados == 0) {
            wait(corteTerminado);
        }
        terminados--;
    }
}
```

Referencia: thread peluquero
```
while (true) {
    pelu.empezarCorte();
    ...
    pelu.terminarCorte();
}
```

Igual esta solución solo funciona con un solo peluquero. Si hubiesen multiples peluqueros trabajando en simultaneo (que creo que los hay? hubiesen preguntado eso en un parcial tho) se podría solucionar con tickets, y que cada peluquero marque su ticket como terminado cuando sea pertinente.

Con varios peluqueros, un cliente podría llevarse el aviso de "terminé" de otro
e irse con el corte a medias. Se arregla emparejando cliente y peluquero, por
ejemplo con un ticket que `empezarCorte()` devuelve y `terminarCorte(ticket)`
recibe.

### b)

Calculo que se podría hacer que haya una sola, que tire notifyAll siempre, y que haya gente que se despierte y vea que no le toca. Como si estuviesemos usando synchronized. Hay que usar notifyAll porque solo notify puede prender a alguien que no necesitaba el mensaje. No es ideal, pero es simil a lo que haría uno con synchronized. 

## Ejercicio 6

### a)
```java
Monitor Auditorio {
    int LIMITE = 50;
    int genteAdentro = 0;
    boolean enCurso = false;
    int charlasTerminadas = 0;
    Condition puedeEntrar = new Condition();
    Condition finCharla = new Condition();

    // asistente
    asistir() {
        while (enCurso || genteAdentro == LIMITE) wait(puedeEntrar);
        genteAdentro++;
        int miCharla = charlasTerminadas;          // la próxima que termine es la mía
        while (charlasTerminadas == miCharla) wait(finCharla);
    }

    // orador
    boolean empezarCharla() {
        if (genteAdentro == 0) return false;       // sala vacía: no arranco
        enCurso = true;
        return true;
    }

    terminarCharla() {
        enCurso = false;
        genteAdentro = 0;                          // se van todos juntos
        charlasTerminadas++;
        signalAll(finCharla);
        signalAll(puedeEntrar);
    }
}

thread orador {
    while (true) {
        descansar(5)
        while (!auditorio.empezarCharla()) descansar(5)
        darCharla()
        auditorio.terminarCharla()
    }
}
```

### b)

Suposiciones: los asistentes no eligen charla, entran a la próxima que se dé. No
se busca justicia entre oradores.

Cambian dos cosas respecto del (a):

- El orador **espera** (con `wait`) a que haya al menos 40 personas, en vez de
  descansar y reintentar. `asistir()` le avisa cuando se llega a 40.
- Hay tres oradores y una sola sala, así que compiten por ella. La condición de
  espera incluye `enCurso`: sin eso, dos oradores podrían ver 40 personas a la
  vez y arrancar los dos.

```java
Monitor Auditorio {
    int LIMITE = 50;
    int MINIMO = 40;
    int genteAdentro = 0;
    boolean enCurso = false;
    int charlasTerminadas = 0;
    Condition puedeEntrar = new Condition();
    Condition finCharla = new Condition();
    Condition puedoEmpezar = new Condition();

    // asistente
    asistir() {
        while (enCurso || genteAdentro == LIMITE) wait(puedeEntrar);
        genteAdentro++;
        if (genteAdentro == MINIMO) signal(puedoEmpezar);   // ya se puede dar una charla
        int miCharla = charlasTerminadas;
        while (charlasTerminadas == miCharla) wait(finCharla);
    }

    // orador
    empezarCharla() {
        while (enCurso || genteAdentro < MINIMO) wait(puedoEmpezar);
        enCurso = true;
    }

    terminarCharla() {
        enCurso = false;
        genteAdentro = 0;
        charlasTerminadas++;
        signalAll(finCharla);
        signalAll(puedeEntrar);
    }
}

thread orador {
    while (true) {
        descansar(5)
        auditorio.empezarCharla()
        darCharla()
        auditorio.terminarCharla()
    }
}
```

- `signal(puedoEmpezar)` y no `signalAll`: arranca un solo orador y cualquiera
  sirve. Si se colara otro orador antes que el despertado, este rechequea, ve
  `enCurso` y se vuelve a dormir.
- Cuando termina una charla, `genteAdentro` vuelve a 0, así que los otros
  oradores siguen esperando hasta que entren 40 personas nuevas, y ese aviso lo
  da `asistir()`.
- Puede haber inanición entre oradores (uno podría ganar siempre la sala), pero
  no se pide justicia.


## Ejercicio 7

### a)
```java
thread Jugador(sala) {
    int monto;
    boolean gane = false;
    while(!sala.concluido()) {
        String palabra = palabra_random();
        monto = monto_random();
        gane = sala.apostar(palabra, monto);
    }
    if (gane) {
        print("la rompi viejo gane", monto*10);
    } else print("le erre la con");
}
```

### b)

```java
monitor SalaDeJuego {
    boolean terminado = false;
    String nuestraPalabra = palabra_random();
    Thread ultimoApostador = null;
    Condition consecutivo = new Condition();

    concluido() {
        return terminado;
    }

    boolean apostar(palabra, monto) {
        Thread jugador = Thread.currentThread();
        while (jugador === ultimoApostador && !terminado) {
            wait(consecutivo);
        }
        
        if (terminado) return false
        ultimoApostador = jugador
        if (palabra === nuestraPalabra) {
            terminado = true;
            signalAll(consecutivo)
            return true;
        };
        signalAll(consecutivo)
        return false;
    }
}
```

## Ejercicio 8

### a)
```java
Monitor Pizzeria {
    int grandes = 0;
    int chicas = 0;
    Condition hayPizza = new Condition();
    // pizzero llama a
    dejarPizza(tamaño) {
        if (tamaño == GRANDE) {
            grandes++;
            signal(hayPizza);
        } else {
            chicas++;
            if (chicas>1) signal(hayPizza); 
        }
    }

    //gente llama a
    agarrarPizza() {
        while(grandes == 0 && chicas < 2) {
            wait(hayPizza);
        }

        if (grandes > 0) { grandes--; return; }
        if (chicas > 1)  { chicas -= 2; return; }
    }
}
```

for reference, cliente se vería algo como
```java
thread Cliente() {
    run() {
        agarrarPizza();
        // paso x caja.
    }
}
```
## Ejercicio 9

### a)
```java
int NORTE = 0, SUR = 1;
int LIMITE = 50;
Monitor Bote {
    int orillaActual = NORTE;
    boolean autorizado = false;
    boolean subiendoGente = true;
    int genteAbordo = 0;

    Condition barcoDisponible = new Condition();
    Condition barcoListo = new Condition();
    Condition llegamos = new Condition();
    Condition seBajaronTodos = new Condition();

    // gente llama 
    subirseAlBarco(orilla) {
        while (orillaActual != orilla || genteAbordo == LIMITE || !subiendoGente) {
            wait(barcoDisponible)
        }
        genteAbordo++;
        if (genteAbordo == LIMITE) {
            signal(barcoListo)
            subiendoGente = false;
        };

        // viajamo cuando haya autorización...

        while (orillaActual == orilla) {
            wait(llegamos);
        }
        genteAbordo--;
        if (genteAbordo == 0) {
            signal(seBajaronTodos)
        }
    }

    // llama el barco? idfk
    esperarAPartir() {
        while (!autorizado || genteAbordo != LIMITE) {
            wait(barcoListo);
        }
        autorizado = false;
    }

    llegar() {
        // viaje... 
        orillaActual = la_opuesta;
        signalAll(llegamos)
        while (genteAbordo > 0) {
            wait(seBajaronTodos)
        }
        subiendoGente = true;

        // ahora subo a los demás!
        signalAll(barcoDisponible);
    }

    // llama el autorizador?
    autorizar() {
        autorizado = true
        signal(barcoListo);
    }
}
```

```java
Thread barco(viaje) {
    while true {
        viaje.esperarPartir();
        cruzar();
        viaje.llegar();
    }
}
```

### b)

No! podríamos implementar una cola, que tenga una variable de condición per capita, y que se haga un peek de la cola cuando lleguemos y se llame a esas personas. No se si se podría lograr con tickets por orilla, sino. Podrías poner un proximoTicket por orilla, que cada perosna trabada tenga un miTicket = proximoTicket[orilla]++, y que cada vez q haya un signalAll() de barcoDisponible, se revise quien va, que suba y tire el signalAll() para el proximo, hasta que llenemos.


## Ejercicio 10

### a)
El enunciado pide Java, así que el monitor es una clase con métodos
`synchronized`, y la condición es la cola implícita del objeto (`wait` /
`notify`).

```java
import java.util.ArrayDeque;
import java.util.Deque;

public class ResourceManager<R> {
    private final Deque<R> cola = new ArrayDeque<>();

    public synchronized R tomar() throws InterruptedException {
        while (cola.isEmpty()) {
            wait();                  // espero a que alguien libere un recurso
        }
        return cola.removeFirst();
    }

    public synchronized void liberar(R r) {
        cola.addLast(r);
        notify();                    // hay un recurso más: despierto a uno que espera
    }
}
```

- `notify` alcanza, porque en la cola implícita solo esperan threads que quieren
  tomar un recurso, y son intercambiables.
- El `while` es necesario con Mesa: otro thread puede llevarse el recurso entre
  el `notify` y el momento en que el despertado vuelve a entrar.

### b)

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class ResourceManager<R> {
    private final Deque<R> cola = new ArrayDeque<>();

    public synchronized List<R> tomar(int n) throws InterruptedException {
        while (cola.size() < n) {
            wait();
        }
        List<R> tomados = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            tomados.add(cola.removeFirst());
        }
        return tomados;
    }

    public synchronized void liberar(R[] resources) {
        for (R r : resources) {
            cola.addLast(r);
        }
        notifyAll();
    }
}
```

### c)

Con la solución del (b), un pedido grande puede esperar para siempre: si siempre
llegan pedidos chicos que se llevan los recursos, nunca se juntan los que
necesita. Para que no se lo perjudique, los pedidos se atienden **en orden de
llegada**: solo el primero puede tomar, y los de atrás no le pasan adelante
aunque pidan poco.

El costo es que se pierde concurrencia. Mientras el pedido grande espera, los
chicos de atrás también esperan, aunque haya recursos de sobra para ellos. Es
el precio de no perjudicar a los grandes.

**Opción 1: tickets.** Cada pedido saca un número. Solo puede tomar el que tiene
el turno, y cuando termina avanza el turno y despierta a todos para que el
siguiente rechequee.

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;

public class ResourceManager<R> {
    private final Deque<R> cola = new ArrayDeque<>();
    private long proximoTicket = 0;   // número que recibe el próximo pedido
    private long turno = 0;           // ticket del pedido que puede tomar ahora

    public synchronized List<R> tomar(int n) throws InterruptedException {
        long miTicket = proximoTicket++;
        while (miTicket != turno || cola.size() < n) {
            wait();                   // no es mi turno, o todavía no alcanzan
        }
        List<R> tomados = new ArrayList<>();
        for (int i = 0; i < n; i++) {
            tomados.add(cola.removeFirst());
        }
        turno++;
        notifyAll();                  // le toca al siguiente: que rechequee
        return tomados;
    }

    public synchronized void liberar(R[] resources) {
        for (R r : resources) {
            cola.addLast(r);
        }
        notifyAll();
    }
}
```

**Opción 2: cola de pedidos, cada uno con su propia condición.** Misma idea,
pero en vez de despertar a todos con `notifyAll`, se despierta solo al primero
de la cola. Con `synchronized` hay una sola cola de espera por objeto, así que
para tener una condición por pedido hace falta `ReentrantLock` y
`newCondition()`.

```java
import java.util.ArrayDeque;
import java.util.ArrayList;
import java.util.Deque;
import java.util.List;
import java.util.concurrent.locks.Condition;
import java.util.concurrent.locks.ReentrantLock;

public class ResourceManager<R> {
    private final Deque<R> cola = new ArrayDeque<>();
    private final ReentrantLock lock = new ReentrantLock();
    private final Deque<Pedido> pedidos = new ArrayDeque<>();   // en orden de llegada

    private class Pedido {
        final Condition miTurno = lock.newCondition();          // cada pedido espera en la suya
    }

    public List<R> tomar(int n) throws InterruptedException {
        lock.lock();
        try {
            Pedido yo = new Pedido();
            pedidos.addLast(yo);
            while (pedidos.peekFirst() != yo || cola.size() < n) {
                yo.miTurno.await();   // no soy el primero, o todavía no alcanzan
            }
            pedidos.removeFirst();
            List<R> tomados = new ArrayList<>();
            for (int i = 0; i < n; i++) {
                tomados.add(cola.removeFirst());
            }
            avisarAlPrimero();        // quizás al siguiente también le alcanza
            return tomados;
        } finally {
            lock.unlock();
        }
    }

    public void liberar(R[] resources) {
        lock.lock();
        try {
            for (R r : resources) {
                cola.addLast(r);
            }
            avisarAlPrimero();
        } finally {
            lock.unlock();
        }
    }

    private void avisarAlPrimero() {
        Pedido primero = pedidos.peekFirst();
        if (primero != null) {
            primero.miTurno.signal();
        }
    }
}
```

- Es más eficiente que la opción 1: cada aviso despierta a uno solo, el que puede
  avanzar, en vez de a todos.
- Después de tomar, el pedido avisa al nuevo primero, porque quizás a ese también
  le alcanza con lo que quedó.
- El `unlock()` va en un `finally`, para que el lock se libere aunque salte una
  excepción.
