#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <sys/wait.h>

int pipes[2];

// Plab de accion: tirar exec del ls -al y pipear el resultado de salida a un wc -l
void sub_ls() {
    close(pipes[0]);
    dup2(pipes[1], STDOUT_FILENO);
    execlp("ls", "ls", "-al", NULL);
    exit(EXIT_SUCCESS);
}

void sub_wc() {
    close(pipes[1]);
    dup2(pipes[0], STDIN_FILENO);
    execlp("wc", "wc", "-l", NULL);
    exit(EXIT_SUCCESS);
}

int main() {
    pipe(pipes);

    if (fork() == 0) sub_ls();

    if (fork() == 0) sub_wc();
    close(pipes[0]);
    close(pipes[1]);

    wait(NULL);
    wait(NULL);

    //close(pipe_fd)

    return 0;
}