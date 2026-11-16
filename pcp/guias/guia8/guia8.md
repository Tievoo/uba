# Guía 8 — Cómputo Paralelo

## Ejercicio 1

```
T_P ≈ T1/P + T∞
Π:  T1 = 2048, span T∞  (incógnita)
Π': T1' = 1024, span T∞' (incógnita)

con 32 procesadores Π' tarda menos:
1024/32 + T∞' < 2048/32 + T∞
     32 + T∞' < 64 + T∞
          T∞' < T∞ + 32

con 512 procesadores Π' tarda más:
1024/512 + T∞' > 2048/512 + T∞
       2 + T∞' > 4 + T∞
           T∞' > T∞ + 2

condición:
2 < T∞' − T∞ < 32
Π' redujo el work pero alargó el span: con pocos procesadores manda el work (gana Π'),
con muchos manda el span (gana Π)
```

## Ejercicio 2

```
c pasos completos, k pasos incompletos

```

## Ejercicio 3

```
T4 = 80, T64 = 10

cotas superiores de T1 y T∞ (de las mediciones):
ley del work  T_P ≥ T1/P  ->  T1 ≤ P·T_P:  4·80 = 320,  64·10 = 640   ->  T1 ≤ 320
ley del span  T_P ≥ T∞    ->  T∞ ≤ T_P:    80, 10                     ->  T∞ ≤ 10

cota ajustada del ej 2 con P = 10:
T10 ≤ (T1 − T∞)/10 + T∞ = T1/10 + (9/10)·T∞     creciente en T1 y en T∞ (9/10 > 0): puedo enchufar las cotas superiores
    ≤ 320/10 + (9/10)·10
    = 32 + 9
    = 41

T10 ≤ 41 pasos
```

## Ejercicio 4

```
vectorSum
class VectorSum extends RecursiveTask<Integer> {
    int[] A;
    int low, high;

    VectorSum(int[] A, int low, int high) {
        this.A = A; this.low = low; this.high = high;
    }

    protected Integer compute() {
        // |A| es potencia de 2; llamada inicial: new VectorSum(A, 0, n - 1).compute()
        if (low == high) {
            return A[low];
        }
        else if (high - low == 1) {
            // evito forkear para dos numeros que se conviertan en un fork per numero
            return A[low] + A[high];
        } else {
            int mid = (low + high) / 2;
            VectorSum left = new VectorSum(A, low, mid);
            VectorSum right = new VectorSum(A, mid + 1, high);
            left.fork();
            int rightAns = right.compute();
            int leftAns = left.join();
            return leftAns + rightAns;
        }
    }
}
work:
W(1) = Θ(1)
W(n) = 2·W(n/2) + Θ(1)      dos mitades + combinar (una suma)
a = 2, b = 2, n^(log_b a) = n
f(n) = Θ(1) = O(n^(1-ε)) con ε = 1  ->  caso 1  ->  W(n) = Θ(n)

span:
S(1) = Θ(1)
S(n) = S(n/2) + Θ(1)        una sola copia: las dos mitades corren en paralelo
     = Θ(log n)             log n niveles · Θ(1) por nivel

paralelismo:
W(n) / S(n) = Θ(n / log n)
```

## Ejercicio 5

```
power(int x, int c) {
    if (c == 0) return 1;
    else {
        int y = power(x, c / 2);        // una sola subtarea y dependo de su resultado: nada que forkear
        if (c % 2 == 0) return y * y;
        else return x * y * y;
    }
}

DAG: una cadena (camino), de Θ(log c) nodos. Cada llamada espera el resultado de la anterior
     para multiplicar; no hay dos nodos independientes.

work:
W(0) = Θ(1)
W(c) = W(c/2) + Θ(1)        una llamada de la mitad + 1 o 2 multiplicaciones
     = Θ(log c)             c se divide por 2 en cada paso: log c llamadas · Θ(1)
(maestro: a = 1, b = 2, n^(log_b a) = 1, f = Θ(1) = Θ(1) -> caso 2 -> Θ(log c))

span:
S(c) = S(c/2) + Θ(1) = Θ(log c)     igual al work: es una cadena, todo es camino crítico

paralelismo:
W(c) / S(c) = Θ(1)          no hay paralelismo: más procesadores no ayudan
```

## Ejercicio 6

```
class Transponer extends RecursiveAction {
    int[][] A, AT;
    int fila, columna, tam;     // bloque de A con esquina (fila, columna) y lado tam

    Transponer(int[][] A, int[][] AT, int fila, int columna, int tam) {
        this.A = A; this.AT = AT;
        this.fila = fila; this.columna = columna; this.tam = tam;
    }

    protected void compute() {
        // n es potencia de 2; llamada inicial: new Transponer(A, AT, 0, 0, n).compute()
        // el bloque (fila, columna) de A va al bloque (columna, fila) de AT
        if (tam == 1) {
            AT[columna][fila] = A[fila][columna];
        } else {
            int mitad = tam / 2;
            Transponer t1 = new Transponer(A, AT, fila, columna, mitad);
            Transponer t2 = new Transponer(A, AT, fila, columna + mitad, mitad);
            Transponer t3 = new Transponer(A, AT, fila + mitad, columna, mitad);
            t1.fork(); t2.fork(); t3.fork();
            new Transponer(A, AT, fila + mitad, columna + mitad, mitad).compute();
            t1.join(); t2.join(); t3.join();    // sin resultado: join = esperar que terminen
        }
    }
}

work:
W(1) = Θ(1)
W(n) = 4·W(n/2) + Θ(1)      4 cuadrantes de lado n/2 (n = lado de la matriz)
a = 4, b = 2, n^(log_b a) = n²
f(n) = Θ(1) = O(n^(2-ε)) con ε = 2  ->  caso 1  ->  W(n) = Θ(n²)   (cada elemento se copia una vez)

span:
S(1) = Θ(1)
S(n) = S(n/2) + Θ(1)        una sola copia: los 4 cuadrantes corren en paralelo
     = Θ(log n)             log n niveles · Θ(1) por nivel

paralelismo:
W(n) / S(n) = Θ(n² / log n)
```

## Ejercicio 7

```
work:
W(1) = Θ(1)
W(n) = 2·W(n/2) + Θ(n)      dos mitades + merge lineal
a = 2, b = 2, n^(log_b a) = n
f(n) = Θ(n) = Θ(n^(log_b a))  ->  caso 2  ->  W(n) = Θ(n log n)   (igual que el secuencial)

span:
S(1) = Θ(1)
S(n) = S(n/2) + Θ(n)        una sola copia (mitades en paralelo) + merge entero: va después del join y es secuencial
a = 1, b = 2, n^(log_b a) = 1
f(n) = Θ(n) = Ω(n^(0+ε)) con ε = 1; regularidad: 1·f(n/2) = n/2 ≤ c·n con c = 1/2
->  caso 3  ->  S(n) = Θ(n)     (n + n/2 + n/4 + ... ≤ 2n: manda el merge de la raíz)

paralelismo:
W(n) / S(n) = Θ(n log n) / Θ(n) = Θ(log n)     cuello de botella: el merge secuencial
```

## Ejercicio 8

```
a)

```

```
b) merge
work:        T1(n) =
span:        T∞(n) =
paralelismo:
```

```
c) mergeSort con merge paralelo
work:        T1(n) =
span:        T∞(n) =
paralelismo:
```
