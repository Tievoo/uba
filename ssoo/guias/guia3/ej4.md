## Ejercicio 4

Demostrar? En SSOO?

el código visto en clase es
```c
void wait(s){
    while(s<=0) dormir;
    s--;
}

void signal(s){
    s++;
    if(alguien espera por s) despertar a alguno;
}
```

Bueno si no es atomico aca podes agarrar en s++ a un wait y con el despertar a alguno a otro wait.

Entonces no cumple

fin
