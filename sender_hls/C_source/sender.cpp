// Pattern Sender (HLS) for PYNQ 2021.07.13 Naoki F., AIT
// ライセンスについては LICENSE.txt を参照してください．

#include "define.h"

void pattern_sender (int frame, hls::stream<pixel_t> &pout)
{
#pragma HLS INTERFACE s_axilite port=return bundle=ctrl
#pragma HLS INTERFACE s_axilite port=frame bundle=ctrl
#pragma HLS INTERFACE axis port=pout

    pixel_t p;
    p.data = 0;
    p.keep = p.strb = 0x7;
    p.user = p.last = p.id = p.dest = 0;
    ap_uint<9> col_x;
    ap_uint<8> col_y;
    const ap_uint<8> zero = 0x00;
    
    col_y = (frame >> 1) & 0xff;
    for (int y = 0; y < 480; y++) {
        col_x = frame & 0x1ff;
        for (int x = 0; x < 800; x++) {
#pragma HLS PIPELINE
            p.data.range(23, 16) = (col_x[8]) ? col_y : zero;
            p.data.range(15,  8) = (col_x[6]) ? col_y : zero;
            p.data.range( 7,  0) = (col_x[7]) ? col_y : zero;
            p.user[0] = (x == 0 && y == 0);
            p.last    = (x == 799);
            pout << p;
            col_x++;
        }
        col_y++;
    }
}