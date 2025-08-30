## Suponiendo que P = NP, diseñar un algoritmo polinomial que dado un grafo G retorne una clique de tamaño máximo de G.

Hago un loop desde $|V|$ hasta 1 para ver el tamaño máximo de la clique
Después, itero sobre $|V|$ y reviso si el grafo sin un nodo sigue teniendo el mismo tamaño de clique, y si es así, lo saco, sino, sigo. Y me queda la clique.
