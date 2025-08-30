## Ejercicio 5

QVQ $P = NP \iff NP \subseteq P / log(n)$

La ida es trivial, ya que $P \subset P_{advice}$ para cualquier advice, y P = NP

La vuelta, por otro lado.

Sabemos que si SAT $\in$ P, P = NP. Esto significa que SAT se puede resolver con una máquina deterministica polinomial con un advice logaritmico a la entrada.

Ahora, ese advice es logaritmico, entonces puedo _fabricarlo_/averiguarlo en base al tamaño de n. Ya que hay 2^log(n) combinaciones para cada n, => se puede encontrar cada tira en tiempo polinomial, y con eso simular la máquina de advice, pasandole el advice adivinado.