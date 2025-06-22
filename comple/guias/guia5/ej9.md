## Ejercicio 9
Bueno, que $x \in L$ significa que tenemos que poder computar un problema de decision en espacio logaritmico. Podes hacer un algoritmo, en el que vas contando la cantida de parentesis de apertura y los de cierre. Si en algun momento el numero es negativo (ej: `())(`  haria 1 0 -1 0),es falso. Si al final,el numero es 0, es verdadero. Cualquier numero entre 0 y n toma log n bits, entonces sigo usando log n space. Lo mismo para guardar el tamaño de entrada.


```py
def parentesi(input: str) {
    cont = 0
    for c in input:
        if c == ')':
            cont += 1
        else:
            cont -=1
        if cont < 0:
            return False
    
    return cont == 0
}
```