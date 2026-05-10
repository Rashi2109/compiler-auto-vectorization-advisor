#include <stdio.h>

#define N 10

int main() {
  int graph[N][N] = {
{0, 1, 1, 0, 0, 0, 0, 0, 0, 0},
{1, 0, 1, 1, 1, 0, 0, 0, 0, 0},
{1, 1, 0, 0, 0, 1, 1, 0, 0, 0},
{0, 1, 0, 0, 1, 0, 0, 1, 1, 0},
{0, 1, 0, 1, 0, 0, 0, 0, 1, 0},
{0, 0, 1, 0, 0, 0, 1, 0, 0, 0},
{0, 0, 1, 0, 0, 1, 0, 0, 0, 0},
{0, 0, 0, 1, 0, 0, 0, 0, 1, 0},
{0, 0, 0, 1, 1, 0, 0, 1, 0, 1},
{0, 0, 0, 0, 0, 0, 0, 0, 1, 0}
};

int visited[N] = {0};
int color[N];
int queue[N];
int front = 0 ,rear = 0;
int source = 0;
int bipartite = 1;

visited[source] = 1;
color[source] = 0;
queue[rear++] = source;

printf("Node\tcolor\n");

while(front < rear){
  int node  = queue[front++];
  printf("%d\t%s\n" , node +1 , color[node] ? "Blue" : "Red");

  for(int  i = 0 ; i < N ; i++){

    if(graph[node][i] == 1){
      if(visited[i] == 0){
        visited[i] = 1;
        color[i] = 1 - color[node];
        queue[rear++] = i;

  }
  else if(color[i] == color[node])
  bipartite = 0;

    }
  }
}

if(bipartite)
   printf("The graph is bipartite\n");
   else
   printf("The graph is not bipartite\n");

   return 0;
}
