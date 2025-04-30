## Sabiendo que CLIQUE es NP-completo, demostrar que SUBGRAPH ISOMORPHISM es NPcompleto.

Bien, lo que tenemos que demostrar es que CLIQUE $\leq_p$ SUBGRAPH-ISOMORPHISM. Para ello, tenemos que encontrar un $f$ tal que con <G, k> en CLIQUE $f(G, k) = <G', H'>$ tal que $<G', H'> \in$ SUBGRAPH-ISOMORPHISM. Despues ver que 
1. esa funcion es polinomial
2. se prueba con un si y solo si

Lo que propongo como transformacion seria lo sigiuente: G' es literalmente G. H' es un subgrafo inducido de G, completo con k nodos, que llamamos K.

$\Rightarrow$) Si G k esta en clique, significa que tenemos un K de k nodos completo, que es, efecivamente la clique. Por esto, sabemos que existe un subgrafo H (= K) que es isomorfo a un subgrafo inducido de G (la clique)

$\Leftarrow$) Para la vuelta es medio un idem. Sabemos que tenemos H, subgrafo inducido de G, que definimos ser = K, un grafo completo de k nodos, que es, por consiguiente, una clique de k nodos, y como G = G', G tiene una clique de k nodos.