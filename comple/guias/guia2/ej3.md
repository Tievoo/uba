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

Certificado: La clique (que nodos están en la clique). A lo sumo $|V|$ nodos entonces a lo sumo $|V|^2$ conexiones a chequear. Encima, podes chequear que el largo del certificado sea $\leq k$ antes de arrancar a recorrer, pero cambia poco. Es $O(|V|^2 * log(|V|))$ facilmente acotable a $O(|V|^3)$ => poli

### c) CLIQUE= {$⟨G, k⟩ : G$ es un grafo con subgrafo completo de tamaño mayor o igual a $k$}

es lo mismo q el de arriba pero el k viene codificado, mismo conceptito

### d) k-COLORING = {⟨G⟩ : G es un grafo que se puede particionar en k conjuntos indepenientes}

Hecho en clase, el certificado son los coloreos (f: nodo -> color)

### Me da paja seguir
