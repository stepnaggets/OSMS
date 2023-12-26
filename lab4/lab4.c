#include <stdio.h>

#define LENGTH 5
#define SEQUENCE_LENGTH 31
#define MAX 40


void printArray(int arr[], int len) {
    for (int i = 0; i < len; i++) {
        printf("%d ", arr[i]);
    }
}


double autocorrelation(int original[], int shifted[], int length) {
    int matches = 0;
    for (int i = 0; i < length; i++) {
        if (original[i] == shifted[i]) {
            matches++;
        }
    }
    return (double)(matches - (length - matches)) / length;
}

int main() {
    int x[LENGTH] = {1, 0, 0, 0, 0};
    int y[LENGTH] = {1, 0, 1, 1, 1};

    printf("Array x: ");
    printArray(x, LENGTH);
    printf("\nArray y: ");
    printArray(y, LENGTH);
    printf ("\n");

    int original[SEQUENCE_LENGTH] = {0};
    int shifted[SEQUENCE_LENGTH] = {0};


    int goldSequence[SEQUENCE_LENGTH];
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        goldSequence[i] = x[4] ^ y[4];

        original[i] = goldSequence[i]; 
        shifted[i] = goldSequence[i];  

        int temp = x[3] ^ x[4];
        for (int j = 4; j >= 0; j--) {
            x[j] = x[j - 1];
        }
        x[0] = temp;
 
        temp = y[1] ^ y[4];
        for (int j = 4; j >= 0; j--) {
            y[j] = y[j - 1];
        }
        y[0] = temp;
    }


    printf("\nGenerated Gold sequence: ");
    printArray(goldSequence, SEQUENCE_LENGTH);

    printf("\n\nShift|                              Bits                            |AutoCorr\n");


    for (int shift = 0; shift < MAX; shift++) {
        double autocorr = autocorrelation(original, shifted, SEQUENCE_LENGTH);
        printf("%5d|", shift+1);
        printArray(shifted, SEQUENCE_LENGTH);
        printf("|");
        printf(" %.3f", autocorr);
        printf("\n");


        int temp = shifted[SEQUENCE_LENGTH - 1];
        for (int i = SEQUENCE_LENGTH-1; i >= 0; i--) {
            shifted[i] = shifted[i - 1];
        }
        shifted[0] = temp;
    }

    int edin = 0;
    for (int i = 0; i < SEQUENCE_LENGTH; i++) {
        if (goldSequence[i] == 1) {
            edin++;
        }
    }
    int nuli = SEQUENCE_LENGTH - edin;
    printf("Сбалансированность (количество единиц в последовательности Голда): %d\n", edin);
    printf("Сбалансированность (количество нулей в последовательности Голда): %d\n", nuli);

    printf ("\nколичество циклов из 1 по одному элементу = 8\n количество циклов из 0 по одному элементу = 5\n количество циклов из 1 по два элемента = 2\n количество циклов из 0 по два элемента = 4\n количество циклов из 1 по три элемента = 1\n количество циклов из 0 по три элемента = 1");

    return 0;
}