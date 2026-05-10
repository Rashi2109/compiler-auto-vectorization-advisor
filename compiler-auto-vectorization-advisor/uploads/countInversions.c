#include <stdio.h>
#define N 8

int countInversions(int a[]) {
  int count = 0;
  for (int i = 0; i < N; i++) {
    for (int j = i + 1; j < N; j++) {
      if (a[i] > a[j]) {
        count++;
      }
    }
  }
  return count;
}

int main() {

  int user1[N] = {1, 2, 3, 4, 5, 6, 7, 8};
  int user2[N] = {2, 1, 4, 3, 6, 5, 8, 7};
  int user3[N] = {1, 2, 3, 4, 5, 6, 7, 8};

  int inv1 = countInversions(user1);
  int inv2 = countInversions(user2);
  int inv3 = countInversions(user3);

  printf("User 1 inversions:%d", inv1);
  printf("User 2 inversions:%d", inv2);
  printf("User 3 inversions:%d", inv3);

  int min = inv1;
  int user = 1;

  if (inv2 < min) {
    min = inv2;
    user = 2;
  }
  if (inv3 < min) {
    min = inv3;
    user = 3;
  }

  return 0;
}
