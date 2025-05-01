## Ejercicio 9

```c
// Memoria compartida
sem = init(0)
atomic<int> contador(0);
```

```c
void proceso(){
    a_i();
    contador++;
    if (contador == N) {
        sem.signal(); // Si terminaron los A, habilito al primero q agarre
    }
    sem.wait(); // Espero
    sem.signal(); // Habilito al próximo
    b_i();
}
```
