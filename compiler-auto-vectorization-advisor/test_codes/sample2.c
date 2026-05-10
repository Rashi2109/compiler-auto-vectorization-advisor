#include <stdio.h>

int main() {

  int a[100];

  for (int i = 1; i < 100; i++) {

    a[i] = a[i - 1] + 1;
  }

  return 0;
}
