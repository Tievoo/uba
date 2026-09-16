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

Ejercicio 6

ok una gloal se llama impar, empieza en N, ysuma en 0. para buscar el i-esimo número impar, haces 2*i-1. ej, el primer numero impar es 2\*1-1, el quinto impar es 9 (1,3,5,7,9), etc. 