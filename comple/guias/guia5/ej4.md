## Considerar el siguiente juego...

Dado un grafo $G$, dos jugadores toman turnos para mover una
piedra. Inicialmente la piedra está en un nodo $v$, y el jugador 1 debe elegir un nodo $w ∈ N(v)$ a
donde mover la piedra. Luego, el jugador 2 hace lo mismo: elige un vecino $z ∈ N(w)$ y mueve la piedra hacia ahí. El juego termina cuando un jugador solo puede mover la piedra a nodos que ya
fueron antes visitados. En ese caso, el jugador que está obligado a mover la piedra a una posición ya visitada pierde. A este juego lo llamamos Generalized Geography, o bien GG.

Probar que el lenguaje GEO = {$\langle G, v\rangle$ : $G$ es un grafo con un nodo $v$, y el jugador 1 tiene una estrategia ganadora jugando GG sobre el grafo $G$ empezando el juego en $v$} es PSPACE-complete.

En clase ya probamos que es PSPACE, es bastante fácil, es un backtracking y un and grande para probar que para cualquier movimiento de 2 existe un movimiento de 1 y etc. Es pspace, creeme. Ahora, tengo q probar que es PSPACE-hard. Siento que tengo q hacer la reducción con TQBF porque los problemas son prácticamente identicos. Diría inlcuso que GEO es una aplicación de TQBF

La reducción es sencilla, nuestro $G_\phi$ es un grafo armado de manera que, asumiendo que j1 empieza, primero van las variables existenciales, después las universales, después las existenciales y así sucesivamente, lo que nos deja un grafo "equivalente" a la formula $\phi$ que cumple con $\text{TQBF}$. La ida y la vuelta son triviales diría, consultar si es el caso.

