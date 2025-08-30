## Ejercicio 8

### a)

Para este modelo simplemente uso 3 semaforos, sem_a, sem_b, sem_c. sem_a empieza en 1, el resto en 0.

```c
void Pa() {
    while(1) {
        sem_a.wait();
        // ejecuta
        sem_b.signal();
    }
}
```
Idem b, c

No hay starvation a no ser que algun proceso se cuelgue. En su defeceto, cada proceso habilita a su sucesor.

### b)
bien, es masomenos lo mismo pero el proceso A le tira dos signals al sem_b, el sem_b arranca en 2, y el P_b se ve algo así

```c
void Pb() {
    int contador = 0;
    while (1) {
        sem_b.wait();
        //ejecutar
        contador++;
        if (contador == 2) {
            contador = 0;
            sem_c.signal();
        }
    }
}
```

C es lo mismo q antes, ejecuta y habilita A.

### c)

Diría que hay dos formas de encarar este problema. En la primera, B y C son secuenciales: digamos, A solo tira una signal, que lo agarra B o C, y después B o C tira el segundo signal, que agarra, de vuelta, B o C. El contador sube a 2, entonces se habilita A. 

La segunda solución, en la que si importa el mutex, es en la que A tira dos signals. Ahí, el contador tiene q ser atómico, o se tiene que cubrir con un mutex.

En clase hicimos la primera y el tipo no chistó pq no tenía tiempo, pero diría que la consigna pide hacer la segunda. Veamosla.

Defino variables compartidas:
```c
atomic<int> contador(0);
sem_cons = init(0);
sem_prod = init(0);
```

```c
void productor_a() {
    while(1) {
        sem_prod.wait();
        //producir
        sem_cons.signal();
        sem_cons.signal();
    }
}

void consumidor() {
    while (1) {
        sem_cons.wait();
        //consumir
        contador++;
        if (contador == 2) {
            sem_prod.signal();
        }
    }
}
```

esto es asumiendo que el contador es atomico, sino armas un mutex y le pones un wait antes del consumir y un signal despues del if y listo
