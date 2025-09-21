#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
int main(){
    size_t N = 32*1024*1024/sizeof(uint64_t); // 32 MB
    uint64_t *a = (uint64_t*)malloc(N*sizeof(uint64_t));
    for(size_t i=0;i<N;i++) a[i]=i;
    volatile uint64_t s=0;
    for(size_t i=0;i<N;i++) s += a[i];
    printf("%llu\\n",(unsigned long long)s);
    free(a);
    return 0;
}

