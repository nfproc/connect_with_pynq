#include <stdio.h>
#include "define.h"

unsigned int pattern_checksum (hls::stream<pixel_t> &pdata)
{
    unsigned int result = 0;
    pixel_t p;
    for (int i = 0; i < 800 * 480; i++) {
        pdata >> p;
        result += p.data;
    }
    return result;
}

int main ()
{
    hls::stream<pixel_t> pdata;
    unsigned int checksum;
    for (int i = 0; i < 30; i += 10) {
        pattern_sender(i, pdata);
        checksum = pattern_checksum(pdata);
        printf("frame %2d: checksum = %08x\n", i, checksum);
    }
    return 0;
}