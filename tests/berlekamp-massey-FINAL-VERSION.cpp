#include<stdio.h>
#include<stdlib.h>


void intialize(int x[], int n){
	 int i;
	 x[0]=1;
	 for(i=1; i< n; i++){
	    x[i]=0;
    }
}

void intialize2(int x[], int n){
	 int i;
	 x[0]=0;
	 for(i=1; i< n; i++){
	    x[i]=0;
    }
}

void copy( int x[], int y[], int n ){
	int i =0;
	for(i=0; i<n ; i++){
	   x[i]= y[i];
   }
}



void printpoly(int x[], int n){

    int i;
    for(i=0; i<n; i++)
	  if (x[i]==1){if (i==0) printf("1"); else printf("+D^%d", i);}
}


	  
int main() {
	int *s;

    int   *C, *B, *T;
    
	int L, N, m, i, d;
	
	int len;
	
	scanf("%d\n", &len);
	
	s = (int *)malloc(len*sizeof(int));
	
	for(i=0; i <len; i++)
	  scanf("%d", &s[i]);
	
	C= (int *)malloc(len*sizeof(int));
	B= (int *)malloc(len*sizeof(int));
	T= (int *)malloc(len*sizeof(int));
	
	intialize(C, len); intialize (B, len); intialize2(T, len);
	
	
	
	
	L = 0; m= -1; N = 0;
	
	while(N<len){
	printf("%d,%d\n", N, L);//added by me 
	d=s[N];
            for (int i=1; i<=L; i++)
            d^=C[i]&s[N-i];            //(d+=c[i]*s[N-i] mod 2)
            if (d==1)
            {
                copy(T, C, len);    //T(D)<-C(D)
                for (int i=0; (i+N-m)<len; i++)
                    C[i+N-m]^=B[i];
                if (L<=(N>>1))
                {
                    L=N+1-L;
                    m=N;
                    copy(B, T, len);    //B(D)<-T(D)
                }
            }
			  
	    // printf("N=%d", N);
	    // printf("m = %d  ", m);
	    // printf("L = %d  ", L);
	    // printf("   T(D)=");
	    // printpoly(T, len);
	    // printf("   C(D)=");
	    // printpoly(C, len);
	    // printf("   B(D)=");
		// printpoly(B, len);
	    // printf("\n");
		N++;	
	}
	printf("Final Linear Complexity (L): %d\n", L);
	return(0);	
}
