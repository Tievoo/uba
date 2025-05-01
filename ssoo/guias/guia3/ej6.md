## Ejercicio 6

Entiendo que esto implica que puedo usar `atomic<int>`, así que me voy a dar ese lujo. Quedaría algo tipo

```c++
atomic<int> count(0); // compartida

// código general
preparado();
count++;
while (count < n){}
critica();
```

### a)
Este es mucho más legible pq evito tener que handlear los semáforos, y dejo que el compilador se encargue.

### b) 
Desconozco como funciona una variable atomica con atomic\<int\> internamente, pero asumo que es más eficiente porque no la hice yo y la hizo un loco con ganas de optimizar su compilador al mango.

Por otro lado, no usar el semáforo implica que estamos constantemente en el while, porque al no usar el semáforo, no podemos dejar el proceso dormido hasta que el propio semáforo lo despierte. Entonces esto es suboptimo y lo que dije arriba medio que no tiene valor

### c)

Del HW, la versión atómica necesita el uso de instrucciones atómicas no interrumpibles, cosa que es bastante frecuente ya a día de hoy

La versión de semáforos necesita lo mismo del hw, y del SO la implementación de los semaforos

Me parece medio redundante la pregunta?
