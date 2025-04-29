## Determinar cuáles de las siguientes afirmaciones son verdaderas y cuáles falsas. Demostrar aquellas que son verdaderas y dar contraejemplos para aquellas que son falsas.

### a) P $\subseteq$ NP y P $\subseteq$ coNP

P $\subseteq$ NP es masomenos trivia. Si se puede hacer en una maquina deterministica, tambien se puede hacer con una maquina deterministica con un certificado. Nada más que el certificado es irrelevante.

P $\subseteq$ coNP también es trivial porque P es cerrada por complemento, es decir, $Π^c$ (con $Π \in$ P) también es P. Por consiguiente, $Π \in$ NP, entonces P $\subseteq$ coNP

### b) Si P = NP entonces coNP = NP

Trivial. Si todo $Π \in$ NP tambien $\in$ P, significa que su complemento también está en P, porque P es cerrada por complemento. Entonces, más formalmente
$\forall Π \in NP (P) : Π^c \in NP(P) \implies NP = coNP$

### c) Si P = NP, entonces todos los lenguajes pertenecen a P
Esto tiene que ser falso no? Que alguien piense en los exponenciales o HALT no se

### d) Si coNP = NP, SAT $\in$ coNP
SAT es trivialmente NP (visto en clase), entonces Verdadero

### e) Si coNP $\subseteq$ NP, entonces NP = coNP

Bueno el enunciado nos da la ida probada, tenemos q ver la vuelta, es decir,
NP $\subseteq$ coNP

Esto es a es verdadero, pero es dificil de explicar, así que lo escribo en palabras.
Si un problema $Π$ está en NP, entonces, su complemento $Π^c$ está en coNP. Que NP $\subseteq$ coNP, significa que todo $Π$ está en coNP, es decir, que todo $Π^c$ está en NP. Y sabemos que eso es cierto. Por consiguiente, es verdad.
