// C Test Bench for Stencil Coprocessor 2021.07.31 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．
#include <stdio.h>
#include <stdlib.h>
#include <unistd.h>
#include <string.h>
#include "define.h"
#define xil_printf printf

unsigned int buf1[N][N], buf2[N][N];

// バッファを初期化する
void init_buf ()
{
    int i, j;
    memset(buf1, 0, sizeof(buf1));
    memset(buf2, 0, sizeof(buf2));
    for (i = 4; i < N; i += 8) {
        for (j = 4; j < N; j += 8) {
            buf1[i][j] = (i << 16) + (j << 4);
        }
    }
    buf1[4][4] = 0x0fffffff;
}

// ステンシル計算（ハードウェア処理）のプロトタイプ
void stencil (unsigned int src[][N], unsigned int dst[][N]);

// 結果を表示
void printresult (unsigned int dst[][N])
{
    int x, y;
    unsigned int sum = 0;
    for (y = 0; y < N; y++) {
        for (x = 0; x < N; x++) {
            sum += dst[y][x];
        }
    }
    for (y = 0; y < 16; y++) {
        for (x = 0; x < 8; x++) {
            xil_printf("%08x ", dst[y][x]);
        }
        xil_printf("\n");
    }
    xil_printf("checksum         : %08x\n", sum);
}

// メイン: ハードでステンシル計算
int main ()
{
    int i;
    unsigned int (*src)[N], (*dst)[N];
    xil_printf("== STENCIL ==\n");
    xil_printf("size = %d, iteration = %d\n\n", N, ITER);

    init_buf();
    for (i = 0; i < ITER; i += 2) {
        src = buf1;
        dst = buf2;
        stencil(src, dst);
        if (i == ITER - 1)
            break;
        src = buf2;
        dst = buf1;
        stencil(src, dst);
    }
    printresult(dst);
    return 0;
}