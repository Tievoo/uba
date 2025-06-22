## Ejercicio 5

No, no voy a hacer el c).

### a)
A ojo no lo veo, pero planteemoslo. Dicese que
$DP \subseteq \Sigma_{2}^p \; \cap \; \Pi_{2}^p$

Entonces, si existe un lenguaje $L$ en $DP$ (significa que existen $L_1 \in \text{NP}$ y $L_2 \in \text{coNP}$), ese lenguaje L existe en $\Sigma_{2}^p \; \cap \; \Pi_{2}^p$. 

Esto significa que L pertenece a ambos, al sigma y al pi.
Estuve 5 minutitos pensando y drafteando si la intersección entre un sigma y su pi me da alguna clase de información respecto a los cuantificadores o algo, pero no me salió nada. Entonces, veo por separado

#### $\Sigma$)
$L \in \text{DP}$ $\implies$ $L \in \Sigma_{2}^p$

Recordemos rápidamente que NP y coNP son sigma y pi 1 respectivamente. Entonces, 
$$
L_1 \cap L_2 = (\exists u_1 (M_1(x, u_1) \; \land \; (\forall u_2 M_2(x, u_2)))
$$

Apa. Hay algo ahí, no? Bueno entonces tengo un $M$ que procesa ambas cosas. Es decir, tengo un $M$ que recibe algo así, emulando $M_1$ y $M_2$

$$
\exists u_1  \forall u_2 \,(M(x, u_1, u_2))
$$

Locura no?

La demostración para $\Pi$ es análoga.

### b)

Pseudo trivial, un lenguaje que te diga "hay un conjunto independiente >= k" (INDSET) y uno que niegue > k. El que niegue > k está en coNP, es un $\Pi_1^k$, ya que se puede representar como un (para todo conjunto de nodos) y chequeas cada conjunto de nodos no sea independiente. Es poco formal la prueba pero sale.