## Ejercicio 3

En resumidas cuentas, decir esto es parecido a decir que lo hicimos antes. Recordemos que NP $= \Pi^p_1$. Y coNP, por consiguiente, es $\Sigma^p_1$. Con la reducción dada, lo que queremos hacer es intentar probar que coNP = NP. Y esto medio que sale. Veamos la hipotesis en detalle.
$$
\text{SAT} \leq_p \overline{\text{SAT}}
$$
Significa que existe un $f$ tal que $\phi \in \text{SAT} \iff f(\phi) \in \overline{\text{SAT}}$. O sea que si a $\phi$ la pasas por una función mágica y era satisfactible, ahora no lo es. Es decir, SAT complemento es NP-hard, entonces coNP es más dificl que NP! Por consiguiente, $NP \subseteq coNP$

Y la vuelta? esto ya lo probamos mil veces pero sabiendo lo de arriba sale esto. Te juro, creeme.

Bueno entonces como $NP = coNP$, tenemos un $k=1$ tal que $\Pi^p_1 = \Sigma^p_1$. Y con eso, por el punto 2, sabemos que colapsa la jerarquía y se da lo pedido.