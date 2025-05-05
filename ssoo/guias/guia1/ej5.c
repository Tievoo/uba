#include <stdlib.h>
#include <unistd.h>
#include <stdio.h>
#include <sys/wait.h>

void bart(){
    printf("El barto\n");
    exit(EXIT_SUCCESS);
}
void lisa(){
    printf("la lisa\n");
    exit(EXIT_SUCCESS);
}
void maggie(){
    printf("maggie\n");
    exit(EXIT_SUCCESS);
}

void homero() {
    printf("Homero simpson, id %d\n", getpid());
    if (fork() == 0) bart();
    if (fork() == 0) lisa();
    if (fork() == 0) maggie();
    
    wait(NULL);
    wait(NULL);
    wait(NULL);

    exit(EXIT_SUCCESS);
}

int main() {
    // Abraham
    printf("Abraham simpson, id %d\n", getpid());
    if (fork() == 0) homero();
    wait(NULL);

    return 0;
}