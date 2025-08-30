#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

int main(int argc, char const *argv[]) {
    int dato = 0;
    pid_t pid = fork();
    
    if (pid == -1) exit(EXIT_FAILURE);
    else if (pid == 0) {
        for (int i=0; i < 3; i++) {
            dato++;
            printf("Dato hijo %d\n", dato);
        }
    }
    else {
        for (int i = 0; i < 3; i++) {
            printf("Dato apdre> %d\n", dato);
        }
    }

    exit(EXIT_SUCCESS);
}