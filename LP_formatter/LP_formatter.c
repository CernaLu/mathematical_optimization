#include <stdio.h>
#include <stdlib.h>

int main(int argc, char **argv)
{
int n, N, c, m;
char str[256]; 
FILE *dst;

dst = fopen(argv[1], "w");

if(dst == NULL)
  {
  printf("\n\nError opening sorting file\n"\
    "in 'src_File_manage()'.\n\n");
    exit(1);
  }

printf("\n\nNumber of variables in object equation?: ");
scanf("%d", &N);
printf("\nEnter the obj equ coefficients in order followed by an ENTER:\n");

// TO FILE #####################
fprintf(dst, "Maximize\n");
fprintf(dst, "obj: ");
for(int i = 1; i <= N; i++)
  {
  scanf("%d", &c);
  fprintf(dst, "%d x%d", c, i);
  if (i < N)
    fprintf(dst, " + ");
  }
//##############################

printf("\n\nNumber of restrictions?: ");
scanf("%d", &n);
printf("\n\nEnter the restrictions followed by an ENTER between equations\n");

// TO FILE #########################
fprintf(dst, "\nSubject To\n");
for(int i = 0; i <= n; i++)
  {
  fgets(str, sizeof(str), stdin);
  if (i>=1)
    fprintf(dst, " c%d: %s", i, str);
  }
//##################################

printf("\n\nNumber of boundaries?: ");
scanf("%d", &m);

// TO FILE #####################
fprintf(dst, "Bounds\n");
for(int i = 0; i <= m; i++)
  {
  fgets(str, sizeof(str), stdin);
  if (i>=1)
    fprintf(dst, " %s", str);
  }
fprintf(dst, "%cGeneral\n", 37);
fprintf(dst, "%c x4\n", 37);
fprintf(dst, "END");
//##############################

return(0);
}
