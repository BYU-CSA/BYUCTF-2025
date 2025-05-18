#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

void play() {
    char buffer[256];
    read(0, buffer, 0x256);
}

void nothing() {
    asm volatile (
        "mov rdi, rsi; ret;"
    );
    printf("\n");
}

void game() {
    play();
    printf("You can't yap!\n");
}

void yap() {
    printf("%p\n", (void *)play);
}

int main() {
    printf("Can you yap?\n");
    printf("Here's your first chance...\n");
    game();
    printf("One more try...\n");
    game();
}