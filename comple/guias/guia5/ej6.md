## Probar que $P \neq SPACE(n)$. Ayuda: observar que ambas clases tienen propiedades de clausura distintas.

Bueno planteemos esto. SPACE(n) es todo lenguaje $L$ tal que hay una maquina deterministica $M$ que decide $L$ y usa espacio $O(n)$. Queremos ver que es distinto de P.

Después de leer foros, llegué a una conclusión parecida a esto:

Asumiendo que P = SPACE(n), implica que existe un problema que toma espacio $O(n)$ y tiempo $O(n^c)$ para una $c$ constante. Entonces, también dicta que P = SPACE(n^2), ya que existira un problema con tiempo $O(n^{2c})$ con espacio $O(n^2)$ entonces SPACE(n) = SPACE(n^2) ! Lo que rompe la jerarquía de espacios.

