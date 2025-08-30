## Ej 8

### ELEMENTARY SP $\in$ NP-C

Para ver que ESP esta en NP es medio trivial, tu certificado es literalmente las aristas que componen el camino, lo tenes que revisar nomas, es a ojo polinomial

Para ver que es NP-hard voy a reducir con hampath, que es NP-c. Para la funcion que pasa de hampath a ESP, recordemos que con hampath tengo un G con un camino de s a t que pasa por todos los nodos una sola vez (es decir, es un camino simple!). Entonces, defino G' = G, pero con pesos = 1, en todas las aristas, con k siendo la cantidad de nodos en G. s y t son lo mismo, masomenos.

$\Rightarrow$) La ida es facil, si se que se cumple que hay un camino hamiltoniano, se por definicion que existe un camino de s a t, que es simple, y toma n-1 aristas. Entonces, existe en G' un camino simple de s a t con peso exactamente n-1, ya que todos los pesos son 1, entonces cumple con ESP.

$\Leftarrow$) La vuelta, veamosla. Sabemos que k = n-1, y sabemos que como G' esta armada con G, hay un camino de ...
Puedo asumir eso por construccion? preguntar


que el otro es P es trivial corres dijkstra que es polinomial $O(|V|^2)$ worst case sin p-q. 