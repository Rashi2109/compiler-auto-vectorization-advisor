#include <stdio.h>

int main() {

  int a[100], b[100], c[100];

  for (int i = 0; i < 100; i++) {

    a[i] = b[i] + c[i];
  }

  return 0;
}
