## Ejercicio 6

### a)
Como la cantidad de frames es menor que la cantidad de páginas, vemos que, una vez que se llena, independienetemente de los golpes aleatorios a otras páginas, se llena de page faults. Second chance nunca mete un bit a nadie, menos a 431 y 332, pero es medio irrelevante. FIFO saca a los que van a entrar después, entonces es ciclico. LRU es lo mismo q FIFO básicamente, exceptuando el caso de 431 y 332. Muchisimos page faults.

### b)
Y, de base, LIFO funcionaría muchisimo mejor. Los únicos valores que se mueven son del 489 al 511 que van rotando entre sí, los demás ni bola. 

No se para qué había tiros aleatorios en esta secuencia, son irrelevantes.
