## Ejercicio 7

Bueno, voy a asumir que tanto `i` como `N` son variables estáticas entonces no hace falta mutex, ya que su valor no cambia.

voy a tener N semáforos, desde 0 hasta N-1. El semáforo i arranca en 1, el resto en 0. Asumo que cada proceso conoce su propio índice, que tomo como `me`. Los semáforos están implementados en un vector que doy por asumido como atómico y que no genera race-cond y bla bla, tal que sems[j] es el semaforo del proceso j

```c
void proc(int me) {
    sems[me].wait();
    // Ejecuto algo...
    int next = me == N - 1 ? 0 : me + 1;
    sems[next].signal();
}
```

