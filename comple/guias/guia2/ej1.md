## Ejercicio 1 Probar que los siguientes lenguajes están en P

### a) COPRIME = {⟨a, b⟩ : (a : b) = 1, es decir, a y b son coprimos}

Esto alcanza con ver un código de python que lo compile por Tesis fuerte de Church-Turing

```py
def coprime(a,b): 
    return mcd(a,b) == 1

def mcd(a, b):
    while b != 0:
        b = a % b
        a = b
    return a
```

Euclides es polinomial a ojo no te lo vo a justificar pero es basicamente es polinomial sobre la cantidad de digitos de a CREO.

### b) POWER = {⟨$a$, $e$, $b$⟩ : $a^e = b$}

En clase tiraron una para hacer potencia en tiempo polinomial con el algoritmo de no se quien pero fija q se puede con el algortimo de kvarashkelia o algo

### c) TREE = {⟨$G$⟩ : $G$ es un grafo conexo sin ciclos}

DFS/BFS que es $O(|V| + |E|)$ pero si querés acotarlo por un solo valor de entrada haces una matriz de adyacencia y es $O(|V|^2)$ por consiguiente también polinomial.

### d) $L$ donde $|L| < \infty$ (es decir, probar que todo lenguaje finito está en P)

Si el lenguaje no es finito es regular entonces tiene un automata entonces es polinomial por [REDACTED] (no curse lenguajes)
