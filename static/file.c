#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main(int argc, char *argv[]) {
    if (argc != 2) {
        printf("Usage: to return same value - %s <argument>\n", argv[0]);
        return 1;
    }

    printf("Running in C: %s\n", argv[1]);

    // Add a delay to simulate a slow process
    for (int i = 0; i < 10; i++) {
        printf("Progress: %d%%\n", i * 10);
        fflush(stdout);
        sleep(1);
    }

    return 0;
}
