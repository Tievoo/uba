## Ejercicio 5

```c
preparado()
mutex.wait()
count = count + 1
mutex.signal()
if (count == n)
    barrera.signal()
barrera.wait()
critica()
```

este código permite inanición porque accede a count sin el mutex waiteado, para compararlo con n. Voy a asumir que n es una variable local, y queda algo así. ademas le falta un signal al final del wait pq sino solo uno va a correr "critica", pq hay un solo signal a barrera

```c
preparado()
mutex.wait()
count = count + 1
if (count == n)
    barrera.signal()
mutex.signal()

barrera.wait()
barrera.signal()
critica()
```
