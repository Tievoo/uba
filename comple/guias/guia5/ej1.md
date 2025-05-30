## Probar que los siguientes lenguajes están en PSPACE.

### a) CLIQUE.
$NP \subseteq PSPACE$ y CLIQUE $\in NP$ entonces está en PSPACE, pero bueno, veamoslo bien.

A ojo, diría que podemos ir generando matrices de adyacencia de cada subgrafo posible de por lo menos k nodos, que eso es exponencialisimo, pero se guarda como una matriz de adyacencia $O(|V|^2)$, y despues probamos en cada matriz si es completa, determinando si hay o no clique.

### b) FORMULA_MAS_CHICA = {$\langle\phi, k\rangle$: $\phi$ es una fórmula booleana proposicional, y no existe una fórmula $\phi'$ tal que $\phi ≡ \phi'$ y $|\phi'| ≤ k$}.

bueno tenemos una suerte de cota, simplemente tenemos que generar absolutamente todas las $\phi'$ de tamaño $\leq k$. Eso es recontra requete exponencial, pero tenemos que guardar de a una nomás! Cada una ocupa a lo sumo $O(k)$ (creo?)

Iteras sobre cada una y vas generando las combinaciones de valuación, de a una! que toman espacio polinomial tambien, son a lo sumo k valores 1 o 0

Entonces es aprox O(2k) el espacio

### c) TA-TE-TI = {$\langle T, k\rangle$ : T es una matriz con entradas de valor 0, 1 y 2 tal que el jugador 1 tiene una estrategia ganadora.}

Bueno esto es en resolución es parecido al GEOGRAPHY que vimos en clase, en el sentido que el concepto de "estrategia ganadora" implica que para todo movimiento de 2 existe un movimiento de 1 que para todo movimiento de 2 existe un etc... hasta maximo k veces. Se puede encontrar un paralelismo con TQBF

Podemos haer un Backtracking guardando el estado de la matriz, que toma k x k o lo que es lo mismo, $O(|T|)$. Para demostrar la estrategia ganadora, se tiene que hacer un and grande en las salidas de las ramas, para demostrar que, desde el estado inicial del tablero T, hay una jugada que si o si hace ganar a 1. Como tomamos O(|T|) espacio a lo sumo, es polinomial sobre el tamaño de entrada, y esta en PSPACE.
