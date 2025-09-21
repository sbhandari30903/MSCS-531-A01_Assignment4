#include <stdio.h>
int main(){
    volatile double x=1.0, y=1.0000001, s=0.0;
    for (unsigned i=0;i<50000000U;i++) { x = x*y + 0.000001; s += x; }
    printf("%.6f\\n", (double)s);
    return 0;
}

