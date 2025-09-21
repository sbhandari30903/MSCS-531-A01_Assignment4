#include <stdio.h>
#include <stdint.h>
int main(){
    volatile uint64_t s=0;
    for (uint64_t i=0;i<50000000ULL;i++) s += (i*7) ^ (i>>3);
    printf("%llu\\n",(unsigned long long)s);
    return 0;
}

