## Ejercicio 2

Queremos probar que 
$$
\exists k \in \mathbb{N} : \Sigma^p_k = \Pi^p_k \implies \text{PH} = \Sigma^p_k 
$$

Lo que queremos ver es que la jerarquía colapse como consecuencia de que un sigma sea igual a un pi. Es decir, que todo sigma es igual que su proximo. Sabemos que un pi es igual a un sigma, lo que significa que _puedo invertir los cuantificadores cuando quiera_. 

Sale por inducción sobre el sub, es decir
$\Sigma^p_{k+n}$. n = 0 es trivial, el paso inductivo consiste en ver que 
$\Sigma^p_{k+n} = \Sigma^p_{k+n+1}$. Usemos palabras, que carajo significa esto? significa que agrego un cuantificador más al final. en el n+1.

Como $\Sigma^p_{k+n} = \Sigma^p_{k}$ y tambien $\Sigma^p_{k} = \Pi^p_{k}$, puedo simplementer buscar un "complemento" válido para cambiar el orden de los $k+n$ cuantificadores y combinar el último.