## Ejercicio 8

Probemos la inclusión de $\text{PSPACE}^{\text{PSPACE}} \subseteq \text{PSPACE}$ (ya que la otra es trivial). 

Funciona masomenos igual que $P = P^P$. Nuestra máquina M con un lenguaje en $\text{PSPACE}^{\text{PSPACE}}$ corre con espacio polinomial y un oraculo que también ocupa espacio polinomial teórico. Entonces, una máquina M', simula cada paso de M, y cuando se llama al oraculo, hace el calculo, ocupando espacio polinomial respecto a la entrada, y listo.