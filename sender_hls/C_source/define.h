#include <ap_int.h>
#include <hls_stream.h>
#include <ap_axi_sdata.h>

typedef ap_axiu<24,1,1,1> pixel_t;

void pattern_sender (int, hls::stream<pixel_t> &);