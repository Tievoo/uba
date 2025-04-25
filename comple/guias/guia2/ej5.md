## Considerar los siguientes lenguajes:
### PATH = {⟨G, s, t, k⟩ : G es un digrafo con dos nodos s y t tales que hay un recorrido de longitud menor o igual a k de s a t}:
### EVEN PATH= {⟨G, s, t, k⟩ : G es un digrafo con dos nodos s y t tales que hay un recorrido de longitud par y menor o igual a k de s a t}
Dado un digrafo $G$, definimos $G^{'}$ como el digrafo que tiene dos copias $(v, p)$ y $(v, i)$ de cada vértice v ∈ V (G) donde $(v, x) → (w, y)$ es una arista de G′ si y solo si $v → w ∈ E(G)$ y $x \neq y$

### a) Demostrar que ⟨G, s, t, k⟩ ∈ EVEN-PATH ⇐⇒ ⟨G′,(s, p),(t, p), k⟩ ∈ PATH.

Veamos la ida

$\Rightarrow$)

Asumimos que $⟨G, s, t, k⟩ \in$ **EVEN-PATH**. Entonces, por hipotesis, G es un digrafo con dos nodos s y t tales que hay un recorrdio de longitud PAR y con tamano $\leq k$. Para demostrar, asumo un camino de tamanio k

O sea, tenemos que s, $v_1$, $v_2$, ..., $v_{k-2}$, t existe, va de s a t y es par. O sea, el subcamino que no incluye a s y a t tambien es de tamanio par. Entonces de $G^{'}$, podemos afirmar que un camino que tiene TAMA;O PAR va a empezar con el mismo indice con el que termina. Por consiguiente, por hipotesis de G', el camino de s a t, al ser par, va de (s,p) a (t,p)

$\Leftarrow$)

La vuelta sale parecido a la ida. Sabemos que existe un camino 
$(s,p)$, $(v_1,i)$, $(v_2,p)$ ..., $(v_{k-2}, i)$, $(t, p)$
Como empieza en $p$ y termina en $p$, implica que tiene una cantidad PAR de elementos. Tambien, por funcionamiento de G', sabemos que en G, $s$ tiene un camino par a $t$.
Y que es menor que k es trivial

### b) Mostrar que la reducción de EVEN-PATH a PATH implicada por el punto anterior es polinomial.

EVEN-PATH $\leq_p$ PATH.

Se sabe que reduce por el $\iff$ del punto anterior, de forma que
$f(⟨G, s, t, k⟩) = ⟨G', (s,p), (t,p), k⟩$

Veamos que $f$ es polinomial.

Que hace $f$?
- copia 2 veces cada nodo. Esto toma $O(|V|)$
- genera 2 aristas por cada arista existente. Esto toma $O(2 \dot |E|)$
El resto es trivial; es polinomial.