// Optimized Stencil Coprocessor for Vivado HLS 2021.09.04 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．
#include "define.h"

void stencil (unsigned int src[N][N], unsigned int dst[N][N])
{
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
#pragma HLS INTERFACE s_axilite port=src bundle=ctrl
#pragma HLS INTERFACE m_axi port=src offset=slave bundle=gmem depth=262144
#pragma HLS INTERFACE s_axilite port=dst bundle=ctrl
#pragma HLS INTERFACE m_axi port=dst offset=slave bundle=gmem depth=262144

    unsigned int in_data, hsum, vsum;
    unsigned int hbuf[2], vbuf[2][N];
    int x, y;
    for (y = 0; y < N; y++) {
        for (x = 0; x < N; x++) {
#pragma HLS PIPELINE
            in_data = src[y][x];
            // 横3要素の和を求める
            hsum = hbuf[0] + hbuf[1] + in_data;
            hbuf[0] = hbuf[1];
            hbuf[1] = in_data;
            // 縦3要素分について，求めた和の合計を求める
            vsum = vbuf[0][x] + vbuf[1][x] + hsum;
            vbuf[0][x] = vbuf[1][x];
            vbuf[1][x] = hsum;
            // 外周でなければ，9で割ってから書き込み
            if (x == 5 && y == 5) {
                dst[y-1][x-1] = 0x0fffffff; // (4, 4) はホットスポット
            } else if (x >= 2 && y >= 2) {
                dst[y-1][x-1] = vsum / 9;
            }
        }
    }
}
