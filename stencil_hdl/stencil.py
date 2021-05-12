# Stencil Computation for PYNQ 2021.04.29 Naoki F., AIT
# ライセンスについては LICENSE.txt を参照してください．

import numpy as np
from scipy.signal import convolve2d
from time import perf_counter

WEIGHT = np.ones((3, 3), dtype=np.uint32)

# from init_buf()
def init_buf(buf):
    buf.fill(0)
    for i in range(4, N, 8):
        for j in range(4, N, 8):
            buf[i, j] = (i << 16) + (j << 4)
    buf[4, 4] = 0x0fffffff

# from stencil_soft()
def stencil_soft(src, dst, coproc):
    for y in range(1, N - 1):
        for x in range(1, N - 1):
            dst[y, x] = (src[y-1, x-1] + src[y-1, x] + src[y-1, x+1] +
                         src[y  , x-1] + src[y  , x] + src[y  , x+1] +
                         src[y+1, x-1] + src[y+1, x] + src[y+1, x+1]) // 9
    dst[4, 4] = 0x0fffffff

def stencil_scipy(src, dst, coproc):
    dst[1:-1, 1:-1] = convolve2d(src[1:-1, 1:-1], WEIGHT, mode="same") // 9
    dst[4, 4] = 0x0fffffff

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

# for PYNQ
ADDR_GO   = 0x0
ADDR_DONE = 0x0
ADDR_SIZE = 0x4
ADDR_SRC  = 0x8
ADDR_DST  = 0xc

# from stencil_hard()
def stencil_hard(src, dst, coproc):
    coproc.write(ADDR_SIZE, N)
    coproc.write(ADDR_SRC, src.device_address)
    coproc.write(ADDR_DST, dst.device_address)
    coproc.write(ADDR_GO, 1)
    while coproc.read(ADDR_DONE) == 1:
        pass
    coproc.write(ADDR_GO, 0)
    while coproc.read(ADDR_DONE) == 0:
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

pl = Overlay("stencil.bit")
coproc = pl.stencil_top_0
buf1 = np.ndarray((N, N), dtype=np.uint32)
buf2 = np.ndarray((N, N), dtype=np.uint32)
hbuf1 = allocate(shape=(N, N), dtype=np.uint32)
hbuf2 = allocate(shape=(N, N), dtype=np.uint32)

print("-- SOFTWARE (w/o SciPy) --")
init_buf(buf1)
init_buf(buf2)
evaluate(stencil_soft, buf1, buf2)

print("-- SOFTWARE (w/ SciPy) --")
init_buf(buf1)
init_buf(buf2)
evaluate(stencil_scipy, buf1, buf2)

print("-- HARDWARE --")
init_buf(hbuf1)
init_buf(hbuf2)
evaluate(stencil_hard, hbuf1, hbuf2, coproc)

hbuf1.freebuffer()
hbuf2.freebuffer()