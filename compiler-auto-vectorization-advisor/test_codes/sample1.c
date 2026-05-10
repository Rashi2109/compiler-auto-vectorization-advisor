#include <stdio.h>
#include <time.h>

int main() {

  const int SIZE = 10000000;

  static int a[10000000];
  static int b[10000000];
  static int c[10000000];

  for (int i = 0; i < SIZE; i++) {

    b[i] = i;
    c[i] = i * 2;
  }

  // Benchmark loop
  for (int i = 0; i < SIZE; i++) {

    a[i] = b[i] + c[i];
  }

  printf("Execution completed\n");

  return 0;
}
