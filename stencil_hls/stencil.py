# Stencil Computation (HLS) for PYNQ 2021.05.21 Naoki F., AIT
# ライセンスについては LICENSE.txt を参照してください．

import numpy as np
from time import perf_counter

# from init_buf()
def init_buf(buf):
    buf.fill(0)
    for i in range(4, N, 8):
        for j in range(4, N, 8):
            buf[i, j] = (i << 16) + (j << 4)
    buf[4, 4] = 0x0fffffff

# from printresult()
def printresult(dst, elapsed):
    for y in range(16):
        for x in range(8):
            print("%08x " % dst[y, x], end="")
        print("")
    print("checksum         : %08x" % np.sum(dst, dtype=np.uint32))
    print("elapsed time [ms]: %.3f" % (elapsed * 1000))
    print("")

def evaluate(func, buf1, buf2, coproc=None):
    start_time = perf_counter()
    for i in range(ITER):
        func(buf1, buf2, coproc)
        buf1, buf2 = buf2, buf1
    end_time = perf_counter()
    printresult(buf1, end_time - start_time)

# from stencil_hard()
def stencil_hard1(src, dst, coproc):
    coproc.register_map.src_1.src = src.device_address
    coproc.register_map.dst_1.dst = dst.device_address
    coproc.register_map.CTRL.AP_START = 1
    while coproc.register_map.CTRL.AP_DONE == 0:
        pass

def stencil_hard2(src, dst, coproc):
    coproc.write(0x10, src.device_address)
    coproc.write(0x1C, dst.device_address)
    ctrl = coproc.read(0x00)
    coproc.write(0x00, (ctrl & 0x80) | 0x01)
    while (coproc.read(0x00) & 0x02) == 0:
        pass

# main routine
from pynq import Overlay
from pynq import allocate
import numpy as np

N = 512
ITER = 100

print("== STENCIL ==")
print("size = %d, iteration = %d" % (N, ITER))
print("")

pl = Overlay("stencil_hls.bit")
coproc = pl.stencil_0
hbuf1 = allocate(shape=(N, N), dtype=np.uint32)
hbuf2 = allocate(shape=(N, N), dtype=np.uint32)

print("-- HARDWARE (HLS1) --")
init_buf(hbuf1)
init_buf(hbuf2)
evaluate(stencil_hard1, hbuf1, hbuf2, coproc)

print("-- HARDWARE (HLS2) --")
init_buf(hbuf1)
init_buf(hbuf2)
evaluate(stencil_hard2, hbuf1, hbuf2, coproc)

hbuf1.freebuffer()
hbuf2.freebuffer()