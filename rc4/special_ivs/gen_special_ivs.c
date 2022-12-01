#include <stdio.h>
#include <stdlib.h>
#include <time.h>

int calc_S_1(int* IV, int b){
    int* S = (int*)calloc(256, sizeof(int));
    for(int i = 0; i < 256; i++){
        S[i] = i;
    }
    int j = 0;
    int tmp;
    for(int i = 0; i < b; i++){
        j = (j + S[i] + IV[i]) % 256;
        tmp = S[i];
        S[i] = S[j];
        S[j] = S[i];
    }
    int S_1 = S[1];
    free(S);
    return S_1;
}

void calc_ivs(FILE* fp, int b, int keylen){
    int i = 0;
    int* IV = (int*)calloc(b, sizeof(int));
    IV[0] = 0;
    for(int c = 0; c < keylen; c++){
        IV[1] = b + c - 1;                      // S[1] = b + c after the 1st round of KS
        while (i < 115500){                     // enough IV values
            for(int j = 2; j < b; j++){         // gen random IV
                IV[j] = rand() % 256;
            }

            if (calc_S_1(IV, b) == b + c){      // check IV for speciality
                fprintf(fp, "%d,[", b);

                for(int k = 0; k < b; k++){
                    fprintf(fp, "%d,", IV[k]);
                }
                fprintf(fp, "],");
                fprintf(fp, "%d\n", c);
                i++;
                if (i % 10000 == 0){
                    printf("%d/115500\n", i);
                }
            }

        }
    }
    free(IV);
}

// contribution to cause,вклад в дело,100.0,1
int main(){
    srand(time(0));

    int b;
    printf("The length of IV: ");
    scanf("%d", &b);
    char* filename = (char*)calloc(16, sizeof(char));
    sprintf(filename, "db/IV_%d.csv", b);
    FILE* fp = fopen(filename, "wt");
    fprintf(fp, "IVlen, [IV], keybyte\n");
    
    for(int keylen = 1; keylen <= 64 - b; keylen++){
        calc_ivs(fp, b, keylen);
    }
    fclose(fp);
}
