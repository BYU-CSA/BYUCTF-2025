#include <stdio.h>
#include <stdlib.h>
#include <string.h>

__attribute__((constructor)) void flush_buf() {
    setbuf(stdin, NULL);
    setbuf(stdout, NULL);
    setbuf(stderr, NULL);
}

int reads = 0;

void win() {
    system("/bin/sh");
    exit(0);
}

void menu() {
    puts("1. Read memory");
    puts("2. Enter your name");
}

uint get_choice() {
    uint choice = 0;
    char buffer[16];

    printf("> ");
    fgets(buffer, sizeof(buffer), stdin);
    sscanf(buffer, "%u", &choice);

    return choice;
}

void loop() {
    uint choice = 0;
    char name[0x10];

    memset(name, 0, sizeof(name));

    while (1) {
        menu();
        choice = get_choice();

        switch (choice) {
            case 1:
                // you only get 2 reads
                if (reads >= 2) {
                    puts("You have already read memory twice.");
                    break;
                }
                reads++;
                printf("Enter the address to read from: ");

                uint addr = 0;
                scanf("0x%x", &addr);
                getchar(); // consume the newline character

                // print the uint at that address as a pointer
                uint *ptr = (uint *)addr;
                uint value = *ptr;
                printf("0x%x\n", value);
                break;
            case 2:
                puts("Enter your name:");
                fgets(name, 0x30, stdin);
                return;
            default:
                puts("Invalid choice. Try again.");
                break;
        }
    }
}

int main() {
    puts("Welcome to mipsel32! This is a great place to be!");
    puts("(I apologize in advance)");
    loop();

    return 0;
}