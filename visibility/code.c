#include <stdio.h>
void f(int x) {
    x = x + 7;
    printf("%d\n", x);
}
int main() {
    int x = 2;
    {
        int x = 3;
        x = x * 2;
        f(x);
        printf("%d\n", x);
    }
    x = x + 1;
    printf("%d\n", x);
}
