## Ejercicio 8: Probar que la relación $\leq_L$ es transitiva

La prueba es masomenos sencilla, no estoy en casa y odio este teclado asi que vamos con latex.

QVQ $A \leq_L B \land B \leq_L C \Rightarrow A \leq_L C$

A ojos veamos que lo primero implica que
$x \in A \Rightarrow f(x) \in B$ y que $y \in B \Rightarrow g(y) \in C$. Entonces, definiendo $h(x) = g(f(x))$, se cumple. Las reducciones ambas toman espacio logaritmico, entonces su composicion, trivialmente, tambien. ¿Por que? Esta demostrado que si g y f son computables implicitamente en L, su composición también lo es. Por lo tanto, h es computable implicitamente en L, entonces esto vale.