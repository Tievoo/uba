## Ejercicio 5

### a) y b)
Rompería un poco con el concepto de round robin, porque no todos tendrían el mismo quantum (especialmente en casos $P_1$ -> $P_1$). Eso puede ser bueno, le podemos dar más quantum a algunos procesos más interesantes/cpu-intensive, de forma un poco más granular. 
Habría un pequeño overhead por el context switch de p1 a p1, pero fuera de eso, estaría bueno.

### c)
Poder seleccionar un quantum en base al proceso (no se como implementarías eso), o simplemente un multiplicador del quantum, y evitas el overhead
