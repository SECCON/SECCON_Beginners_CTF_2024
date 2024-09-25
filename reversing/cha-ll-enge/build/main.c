#include <stdio.h>
#include <string.h>

int main(void) {
  char input[70];
  int key[50] = {119, 20, 96,  6,  50, 80,  43, 28, 117, 22,  125, 34, 21,
                 116, 23, 124, 35, 18, 35,  85, 56, 103, 14,  96,  20, 39,
                 85,  56, 93,  57, 8,  60,  72, 45, 114, 0,   101, 21, 103,
                 84,  39, 66,  44, 27, 122, 77, 36, 20,  122, 7};

  printf("Input FLAG : ");
  scanf("%s", input);

  if (strlen(input) == 49) {
    int check = 0;
    int tmp = 0;
    for (size_t i = 0; i < 49; i++) {
      tmp = input[i] ^ key[i] ^ key[i + 1];
      if (tmp == 0) {
        check += 1;
      }
    }
    if (check == 49) {
      printf("Correct! FLAG is %s.\n", input);
      return 0;
    }
  }
  puts("Incorrect FLAG.");
  return 1;
}
