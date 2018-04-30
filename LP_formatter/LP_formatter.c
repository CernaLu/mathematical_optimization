#include <stdio.h>
#include <stdlib.h>

int main( void )
{
int n, N, c, m;
int obj;
char str[256]; 
char opt[100];                      
char scp[100];
char del[50];
FILE *dst;

snprintf(del, sizeof(del), "> sol.txt");
system(del);

dst = fopen("src.lp", "w");

if(dst == NULL)
  {
  printf("\n\nError opening sorting file\n"\
    "in 'src_File_manage()'.\n\n");
    exit(1);
  }
printf("1) Maximize\n2) Minimize\n\n");
scanf("%d", &obj);
printf("\n\nNumber of variables in object equation?: ");
scanf("%d", &N);
printf("\nEnter the obj equ coefficients in order followed by an ENTER:\n");

// TO FILE #####################
if (obj == 1)
  fprintf(dst, "Maximize\n");
if (obj == 2)
  fprintf(dst, "Minimize\n");
fprintf(dst, " obj: ");
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
fprintf(dst, "END");
//##############################

snprintf(scp, sizeof(scp), "./scip -f src.lp -l sol.txt");
    system(scp);
    
snprintf(opt, sizeof(opt), "python read_solution.py");
    system(opt);

fclose(dst);
return(0);
}
