#include <stdio.h>
#include <stdlib.h>
#include <string.h>

#define PARAM_1 205
#define PARAM_2 410

int foo(char *input) {
    int canary = 0xDEADBEEF; 
    char buffer[PARAM_1];

    strcpy(buffer, input);

    if (canary != 0xDEADBEEF) {
        printf("Stack corrupted!\n");
        exit(1);
    }

    printf("Returning from foo...\n");
    return 0;
}

int main() {
    FILE *badfile;
    char data[PARAM_2];

    badfile = fopen("badfile", "r");
    fread(data, sizeof(char), PARAM_2, badfile);
    foo(data);
    printf("Finished main\n");

    return 0;
}
