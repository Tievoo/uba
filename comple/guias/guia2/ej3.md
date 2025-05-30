## Probar que los siguientes lenguajes están en NP.

### a) HAMPATH = {⟨G, s, t⟩ : G es un grafo con dos nodos s y t tales que hay un camino hamiltoniando de s a t}

Nota: un camino hamiltoniano es un camino que pasa por TODOS los nodos UNA sola vez

Bueno para buscar un lenguaje en NP la forma sencilla es buscar un certificado con el que pueda correr una maquina deterministica.

En este caso, el certificado puede ser una lista de pares de nodos (o aristas)

El algoritmo te lo debo, pero consiste en:
- Iterar por cada arista y chequear q exista en el grafo
- Chequear que cert[0] = s y cert[-1] = t
- Chequear que no tenga repetidos 
- Chequear que haya tantas conexiones como nodos

Todas las operaciones son polinomiales. La codificación de la lista tiene como máximo $|V|-1$ aristas (pasamos una vez x nodo, acoto a $|V|$) entonces queda $O(|V| * log(|V|))$ que es polinomial

### b) $k$-CLIQUE= {$⟨G⟩$ : $G$ es un grafo con subgrafo completo de tamaño mayor o igual a $k$}

En particular, k-CLIQUE es P y por consiguiente NP. Dado que podes generar el combinatorio (n k) en tiempo $O(n^k)$. Como k es fijo, eso es polinomial, y despues los chequeas en el mismo tiempo masomenos acotado, a lo sumo te tiro burdamente $O(n^{3k})$.

### c) CLIQUE= {$⟨G, k⟩ : G$ es un grafo con subgrafo completo de tamaño mayor o igual a $k$}

Este si que es NP. Porque k es un parámetro de entrada, entonces no es constante! Acá mi certificado sería, en sí, la clique. Asumo que el certificador no es boludo y no me pasa un k mayor que la cantidad de nodos de G. Lo puedo pasar como bitmaks (asi no me morfo el codificado). Sea como sea, chequeas que todos los nodos estén en G y que las aristas q pasaste existan, y es $O(|V|^3)$ si tiramos manteca al techo.

### d) k-COLORING = {⟨G⟩ : G es un grafo que se puede particionar en k conjuntos indepenientes}

Hecho en clase, el certificado son los coloreos (f: nodo -> color). No es P como el anterior (a no ser que k sea 2) porque... no se lo dijo gente con mucha mente.

### e) ISOMORPHISM

El certificado sería una biyección entre G y H, es decir, un "mapa" o función a la que le pasas un nodo de G y te devuelve uno de H.  Después, iteras por cada arista de G, y vas aplicando las funciones, y revisas si la arista generada por $(f(u), f(v))$ está en $E(H)$. Eso es polinomial medio cuadrado en base al tamaño de G. Hay a lo sumo $O(n^2)$ aristas a revisar, y, si representas los grafos como matrices, revisar $(f(u), f(v))$ es O(1), entonces nos quedamos en $O(n^2)$

### f) SUBGRAPH ISOMORPHISM

El conceptito es similar, pero revisamos desde H acá. Por qué? Porque H es subgrafo de G, entonces es menor o igual en tamaño. Además, no hace falta ver los nodos de G que no están involucrados. La biyección es de H a G en este caso, y revisas con el mismo algoritmo. 

### g) $\neg$SAT

Certificado: La valuación.
Con mi certificado, simulo SAT, si me da 1 devuelvo 0, si me da 0 devuelvo 1.
