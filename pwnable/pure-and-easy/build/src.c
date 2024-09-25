#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>

int main() {
  char buf[0x100] = {0};
  printf("> ");
  read(0, buf, 0xff);
  printf(buf);
  exit(0);
}

void win() {
  char buf[0x50];
  FILE *fp = fopen("./flag.txt", "r");
  fgets(buf, 0x50, fp);
  puts(buf);
}

__attribute__((constructor)) void init() {
  setvbuf(stdin, NULL, _IONBF, 0);
  setvbuf(stdout, NULL, _IONBF, 0);
  alarm(120);
}
