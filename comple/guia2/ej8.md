## Ejercicio 8

Considerar el siguiente lenguaje:
CONNECTED = {⟨G, s, t⟩ : G es un digrafo y s y t dos nodos de G tales que hay un
recorrido de s a t}
Para un digrafo G, sea H el digrafo que tiene un vértice (S, v) para cada S $\subseteq$ V (G) y cada
v $\in$ V (G), donde (S, v) $\rightarrow$ (R, w) es una arista de H si y solo si w $\notin$ S, R = S $\cup$ {w} y v $\rightarrow$ w es
una arista de G.

### a) Demostrar que $⟨G, s, t⟩ \in$ HAMPATH $\iff$ $⟨H,(\{s\}, s),(V (G), t)⟩ \in$ CONNECTED

Dios que PAJA de consigna

En criollo por cada posible subconjunto de nodos de G y para cada posible nodo de G hay una tupla que es un nuevo nodo en H. Después, estas tuplas solo tienen aristas entre sí en caso de que, la parte del conjunto _crezca_ con la arista, y la parte nodal este conectada en G. no se si se entiende. medio falopa

Planteo la ida y veo

#### $\Rightarrow$)
Recordemos que hampath implica q hay un camino hamiltoniano (pasa por todos los vértices!) entre s y t. Esto a ojo es trivial pero es dificil de poner en palabaras, mucho menos en terminos formales. Sabemos que hay un camino hamiltoniano de s a t. Entonces, en H, por definición, existe un camino (algo, s) $\rightarrow$ (algo2, t). Ahora, por definición de H, las aristas solo existen si los conjuntos son "constructivos", es decir, para cualesquiera nodos conectados de H: (S, v) y (R, w), R = S $\cup$ {w}. Como hay un camino hamiltoniano, sabemos que _en el camino_ vamos a acumular en el conjunto del primer elemento _todos los nodos_ de G. De esta manera, $(\{s\}, s) \rightarrow (V(G), t)$.

#### $\Leftarrow$)

La vuelta es básicamente el mismo principio. Probablemente haya una forma más formal de decir esto, pero sabemos que si H tiene un camino en el que "construyó", desde un ({s}, s) a un (Y, t), un Y = $V(G)$, significa que en G había un camino hamiltoniano de s a t. El conjunto del primer elemento de la tupla es un "historial". Si en el principio del camino solo tenemos a s, y al final del camino recorrimos todos los nodos, y tal camino existe, es porque G tiene un camino hamiltoniano que nos permite armar este historial.


### b) Mostrar que la reducción de HAMPATH a CONNECTED implicada por el punto anterior **no** es polinomial.

Y esto a ojimetro es exponencialoide, sobre el tamaño de entrada, porque cada arista se forma en base a cada camino posible sobre el que se puede llegar a esa arista, lo cual es exponencial sobre tamaño de entrada.
