#include <stdio.h>
#include <string.h>

int checker_i_hardly_know_her(char *input) {
    return (input[4] == input[14] && input[14] == input[17] && input[17] == input[23] && input[23] == input[25]) && (input[9] == input[20]) && (input[10] == input[18]) && (input[11] == input[15] && input[15] == input[24] && input[24] == input[31] && input[31] == input[27]) && (input[13] == input[26]) && (input[16] == input[29]) && (input[19] == input[28] && input[28] == input[32]) && (input[36] == 125) && (input[6] == 123) && (input[8] == input[7]-0x20) && (strncmp(input, "byuctf", 6) == 0) && (input[9] + input[20] == input[31]+3  && input[31]+3 == input[0]) && (input[10] == input[7] + 6) && (input[8] == input[9]+27) && (input[12] == input[13]-1) && (input[13] == input[10]-3) && (input[10]==input[16]-1) && (input[16] == input[14]-1) && (input[35] == input[5]-2) && (input[5] == input[21]-1) && (input[21] == input[22]-1) && (input[22] == input[28]*2) && (input[33] == input[32]+1  && input[32]+1 == input[34]-3) && (input[30] == input[7]+1);
}

int main() {
    printf("Welcome to this totally normal flag checkern\n");
    printf("We're going to use a little bit of a different compiler tho\n");
    printf("Ever heard of clang? What makes it different than gcc?\n");
    char user_input[64];

    fgets(user_input, sizeof(user_input), stdin);
    if (checker_i_hardly_know_her(user_input)) {
        printf("You win!!\n");
        return 0;
    }
    else {
        printf("Womp womp\n");
        return 1;
    }
}