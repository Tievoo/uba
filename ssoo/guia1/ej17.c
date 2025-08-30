#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <signal.h>

int myPipe[2];
int N;

int calcular(int numero) {
    int res = 2*numero;

    write(myPipe);
    kill(getppid(), SIGUSR1);
    exit(EXIT_SUCCESS);
}

int dameNumero(int pid) {
    return pid / 2;
}

void informarResultado(int numero, int resultado) {
    printf("Se calculo %d en base a %d\n", resultado, numero);
}

void sigusr1_handler() {
    int res;
    read(myPipe[0], &res, sizeof(int));

}

void ejecutarHijo(int i, int pipes[][2])
{
    // Me da paja crearlo pq no puedo ejecutarlo realmente, tendria q escribir mas funciones
    // Primero hacemos un read de pipes[i][READ] para el numero secreto
    // en criollo, forkeo, el nieto corre "calcular" que hace no se algo, con el numero secreto
    // Despues de calcular, tira signal al medio. no se cual. no se de signals. buscar
    // El medio tendra un handler para eso, que recibira mediante read el resultado.
    // Ahi mismo, se corre un write (como? el handler no tiene los pipes a mano?)
    // Diria que se puede crear una global miPipe  = pipes[i] y que se maneje c eso, ya que cada proceso
    // Tiene un valor distinto ahi y fue
    // El proceso medio calculo q espera la senal con un pause, y despues exitea
    // Al main le faltan waits igualmente
    // Y con eso masommenos tiras
    myPipe = pipes[i];

    int numero;
    read(myPipe[0], &numero, sizeof(int));

    if (fork() == 0) calcular(numero);

    pause();
}

int main(int argc, char *argv[])
{
    if (argc < 2)
    {
        printf("Debe ejecutar con la cantidad de hijos como parametro\n");
        return 0;
    }
    N = atoi(argv[1]);
    int pipes[N * 2][2];
    for (int i = 0; i < N * 2; i++)
    {
        pipe(pipes[i]);
    }
    for (int i = 0; i < N; i++)
    {
        int pid = fork();
        if (pid == 0)
        {
            ejecutarHijo(i, pipes);
            return 0;
        }
        else
        {
            int numero = dameNumero(pid);
            write(pipes[i][1], &numero, sizeof(numero));
        }
    }
    int cantidadTerminados = 0;
    char hijoTermino[N];
    while (cantidadTerminados < N)
    {
        for (int i = 0; i < N; i++)
        {
            if (hijoTermino[i])
            {
                continue;
            }
            char termino = 0;
            write(pipes[i][1], &termino, sizeof(termino));
            read(pipes[N + i][0], &termino, sizeof(termino));
            if (termino)
            {
                int numero;
                int resultado;
                read(pipes[N + i][0], &numero, sizeof(numero));
                read(pipes[N + i][0], &resultado, sizeof(resultado));
                informarResultado(numero, resultado);
                hijoTermino[i] = 1;
                cantidadTerminados++;
            }
        }
    }
    wait(NULL);
    return 0;
}