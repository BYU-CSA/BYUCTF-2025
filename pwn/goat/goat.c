#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int main() {
    char buf[0x40];
    char intro[0x60];
    char name[0x10] = "GOAT\x00";

    // set up the intro
    snprintf(intro, 0x5f, "Welcome to the %s simulator!\nLet's see if you're the %s...\nWhat's your name? ", name, name);
    printf(intro);
    fgets(buf, 0x20, stdin);

    // check
    snprintf(intro, 0x5f, "Are you sure? You said:\n%s\n", buf);
    printf(intro);
    fgets(buf, 0x10, stdin);

    // end
    if (strncmp(buf, "no", 2) != 0) {
        snprintf(buf, 0x3f, "\nSorry, you're not the %s...", name);
        puts(buf);
    } else {
        printf("\n?? Why would you lie to me about something so stupid?\n");
    }

    return 0;
}