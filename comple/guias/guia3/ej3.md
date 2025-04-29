##  Sean $Π$ y $Γ$ dos lenguajes tales que $Π ≤_p Γ$. ¿Qué se puede inferir?

### a) Si $\Pi \in$ P entonces $\Gamma \in$ P

Veamos esto por intuición levemente; $\leq_p$, en criollo, significa "Más difícil que". Entonces, $\Gamma$ es "más difícil" que $\Pi$. $\Gamma$ podría ser, por ejemplo, SAT, que claramente _no_ es P.

### b) Si $\Gamma \in$ P, entonces $\Pi \in$ P
Este es V, por el mismo motivo!

### c) $\Gamma \in NPC \Rightarrow \Pi \in NPC$
### d) $\Pi \in NPC \Rightarrow \Gamma \in NPC$

ambos falsos. en el c simplemente $\Pi$ podría ser, no sé, P
en el d, $\Gamma$ podría ser halt y ser np-hard nomas, no npc

### e) $\Gamma \in NPC$ y $\Pi \in NP \Rightarrow \Pi \in NPC$

$\Pi$ podria no ser hard, falso

### f) $\Pi \in NPC$ y $\Gamma \in NP \Rightarrow \Gamma \in NPC$ 

Sí, ya que si todo NP se reduce a $\Pi$ y $\Pi \leq_p \Gamma$, entonces todo NP reduce a $\Gamma$. Como ya es np y eso prueba q es np hard, es npc, verdadero

### g) $\Pi$ y $\Gamma$ no pueden pertenecer ambos a NPC

trivialmente falso
