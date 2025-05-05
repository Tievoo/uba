#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>
#include <signal.h>

void sigurs1_handler() {
    printf("(%d - hijo) pong\n", getpid());
    kill(getppid(), SIGCONT);
}

int hijo() {
    signal(SIGUSR1, sigurs1_handler);
    kill(getppid(), SIGCONT);
    while (1) {}
}

void sigcont_handler() {
    return;
}

int main() {
    signal(SIGCONT, sigcont_handler);
    pid_t pid = fork();

    if (pid == 0) hijo();

    pause();

    char* respuesta;
    do {
        for (int i = 0; i < 3; i++) {
            printf("(%d - padre) ping\n", getpid());
            kill(pid, SIGUSR1);
            pause();
        }

        printf("Seguimos (y/n): ");
        scanf(" %c", respuesta);

    } while (respuesta[0] == 'y');

    kill(pid, SIGKILL);
    wait(NULL);
    return 0;
}