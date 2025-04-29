## Ejercicio 4

### a) Round Robin
Rara vez, es un sistema _hecho_ para evitarlo y el convoy effect. A no ser que estemos en multicola, no creo q pase

### b) Por prioridad
Si totalmente. Si hay un proceso con k+1 prioridad constantemente y no tenemos aging ni nada, el proceso con prioridad k queda quieto

### c) SJF
Y si, si siempre te vienen short jobs puede quedar uno más largado trabado atrás.

### d) SRTF
Idem SJF, pero encima con desalojo, peor

### e) FCFS
No debería, capaz Convoy effect pero no starvation, vienen, terminan y se van, en orden de entrada, así que eventualmente llega a todos

### f) Multinivel
Depende como las implementes. Si una cola de alta prioridad siempre está con procesos, nunca se baja a los niveles bajos, entonces, sin aging, hay starvation

### g) Multinivel con feedback
Lo dicho arriba, con aging (bien implementado) safas del starvation 
