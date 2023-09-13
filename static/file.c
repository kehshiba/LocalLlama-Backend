#include <stdio.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: to return same value - %s <argument>\n", argv[0]);
        return 1;
    }

    printf("Running in C: %s", argv[1]);
    return 0;
}