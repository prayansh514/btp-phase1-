#include<stdio.h>
#include<stdlib.h>
int autocorrelation(int a[], int b[], int N)
{
	 int i, t;
	 int sum = 0;
	 for(t=0; t<=N-1;t++){
	   for (i=0; i<=N-1;i++)
	 	sum = sum + (2*b[i]-1)*(2*a[i+t]-1);
	 printf("%d,%d\n", t, sum);
	 sum=0;
     }
     return(0);
}

int main(){
	
	int  len, i, j;
	
	scanf("%d", &len);
	int *a = (int *)malloc(2 * len * sizeof(int));
	int *b = (int *)malloc(len * sizeof(int));
	for(i=0; i<len; i++)
	 scanf("%d", &b[i]);
	for(i=0; i<len; i++)
	    a[i] = b[i];
	j=0;
	 for(i=len;i<2*len; i++) {
	     a[i] = b[j]; j++;
     }
    //  printf("***\n");
     autocorrelation(a, b, len);
     return(0);
}
