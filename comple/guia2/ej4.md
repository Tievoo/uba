## 4. Probar que los siguientes problemas están en coNP

### a) PRIME= {$n : n \in$ $\mathbb{N}$ es primo}

Que primo este en co-NP se deduce de que NO-PRIMO = $\neg$PRIMO está en NP.
Entonces defino
NOT-PRIME =  {$n : n \in$ $\mathbb{N}$ NO es primo}

Como pruebo que esto está en NP? Diría que mi certificado podrían ser 2 números distintos de 1 y si mismo del que n sea producto.
Entonces el programa es tipo
```py
def not_prime(n, a, b):
    return n = a * b
```

la multiplicación es polinomial sobre el largo de n pq a y b no pueden tener más bits que n, así que digamos q multiplicar a*b es $O(|n|^2)$ (o menos si usas karatsuba o algún chiche raro)

Y con eso NOT PRIME es NP => PRIME es coNP

### b) GIRTH= {⟨G, k⟩ : G es un grafo tal que todos sus ciclos simples tienen k o menos vértices}

Puede ser co-NP si pruebo que NOT-GIRTH es np (que ALGUN ciclo simple tiene $> k$ vertices)

El certificado puede ser ese ciclo. Solo se revisa que el largo sea mayor a k, y se revisa que todos las aristas sean validas, y que esten conectadas y etc es todo polinomial

### c) TAUTOLOGY= {⟨ϕ⟩ : ϕ es tautología}

usas not tautology que basicamente define q no es tautologia, tu certificado es una valuacion tal que da false. Eso es np, se revisa en polinomial en base al tamano de la entrada y bla bla bla es np entonces taut es coNP
