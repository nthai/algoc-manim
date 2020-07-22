#include <stdio.h>

void kiir(int* tomb, int meret) {
    if (meret == 0) return;
    printf("%d ", *tomb);
    kiir(tomb + 1, meret - 1);
}

int main() {
    int szamok[10] = {3, 4, 1, 2, -4, -4, 7, 11, -1, 0};
    kiir(szamok, 10);
}