
#include <stdlib.h>
#include <stdio.h>
#include <string.h>

int foo(char *str)
{
    int arr[27];
    // char buffer[413];
    char buffer[437];
    // char buffer[461];

    /* The following statement has a buffer overflow problem */ 
    strcpy(buffer, str);

    return 1;
}

int main(int argc, char **argv)
{
    char str[644];
    FILE *badfile;

    badfile = fopen("badfile", "r");
    fread(str, sizeof(char), 644, badfile);
    foo(str);

    printf("Try Again\n");
    return 1;
}

