#include <unistd.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/wait.h>

pid_t pid_child_1;
pid_t pid_child_2;

enum { P_C, C_C, C_P }; // Parent/child, child/child, child/parent
enum { READ, WRITE };

int pipes[3][2]; // 3 sets de pipes, pc, cc y cp

void child1() {
    int val;
    while (val < 49) {
        read(pipes[P_C][READ], &val, sizeof(val));
        printf("A hijo 1 (%d) le llego %d\n",getpid(), val);

        val++;
        write(pipes[C_C][WRITE], &val, sizeof(val));
    }
    exit(EXIT_SUCCESS);
}

void child2() {
    int val;
    while (val < 49) {
        read(pipes[C_C][READ], &val, sizeof(val));
        printf("A hijo 2 (%d) le llego %d\n",getpid(), val);

        val++;
        write(pipes[C_P][WRITE], &val, sizeof(val));
    }
    exit(EXIT_SUCCESS);
}

int main() {
    for (int i = 0; i < 3; i++) {
        pipe(pipes[i]);
    }
    pid_child_1 = fork();
    if (pid_child_1) child1();

    pid_child_2 = fork();
    if (pid_child_2) child2();

    printf("comienza el show\n");
    printf("Padre (%d) envia 0 al hijo 1", getpid());

    int val = 0;
    write(pipes[P_C][WRITE], &val, sizeof(val));

    while (val < 49) {
        read(pipes[C_P][READ], &val, sizeof(val));
        printf("A padre (%d) le llego %d\n",getpid(), val);

        val++;
        write(pipes[P_C][WRITE], &val, sizeof(val));
    }
    wait(NULL);
    wait(NULL);

    return 0;
}