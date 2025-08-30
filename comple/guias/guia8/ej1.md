## Ejercicio 1

Reinterpretemos la consigna un toque. Que un lenguaje sea esparso significa, en criollo, que todas sus palabras de tamaño n, para todo n, son menos en cantidad que el numero obtenido por pasarle n a algun polinomio p, cualquiera, mientras sea el mismo para cada n.

Entonces, la relación que uno tiene que hacer es saber que en P / poly los circuitos son de tamaño polinomial respecto a la entrada, por consiguiente, si hay menos palabras que elementos del circuito disponible para cada n, puedo directamente hardcodear cada respuesta, ya que puedo escribir la palabra explicitamente en el circuito. A lo sumo, tu tamaño de circuito es p(n) (cantidad de palabras) * n (tamaño de palabra), que sigue siendo polinomial sobre n.