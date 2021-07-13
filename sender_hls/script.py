from pynq import allocate
import numpy as np

def initial_fbuf ():
    base = np.zeros((48, 64, 1), dtype=np.uint8)
    for y in range(24):
        for x in range(32):
            base[y + 24][x][0] = 0x80
            base[y][x + 32][0] = 0xc0
    return np.tile(base, (15, 20, 3))

def video_initialize (vdma):
    # video width and height
    VWIDTH = 1280
    VHEIGHT = 720
    # pattern shape
    PWIDTH = 800
    PHEIGHT = 480
    PLEFT = (VWIDTH - PWIDTH) // 2
    PTOP = (VHEIGHT - PHEIGHT) // 2
    
    # frame buffers
    fbuf0 = allocate(shape=(VHEIGHT, VWIDTH, 3), dtype=np.uint8)
    fbuf1 = allocate(shape=(VHEIGHT, VWIDTH, 3), dtype=np.uint8)
    fbuf2 = allocate(shape=(VHEIGHT, VWIDTH, 3), dtype=np.uint8)
    fbuf_base = initial_fbuf()
    fbuf0[:] = fbuf_base
    fbuf1[:] = fbuf_base
    fbuf2[:] = fbuf_base
    
    # initialize VDMA
    vdma = pl.axi_vdma_0
    vdma.write(0x30, 0x8b) # pattern write
    vdma.write(0xac, fbuf0.device_address + (PTOP * VWIDTH + PLEFT) * 3)
    vdma.write(0xb0, fbuf1.device_address + (PTOP * VWIDTH + PLEFT) * 3)
    vdma.write(0xb4, fbuf2.device_address + (PTOP * VWIDTH + PLEFT) * 3)
    vdma.write(0xa8, VWIDTH * 3)
    vdma.write(0xa4, PWIDTH * 3)
    vdma.write(0xa0, PHEIGHT)
    vdma.write(0x00, 0x8b) # video read
    vdma.write(0x5c, fbuf0.device_address)
    vdma.write(0x60, fbuf1.device_address)
    vdma.write(0x64, fbuf2.device_address)
    vdma.write(0x58, VWIDTH * 3)
    vdma.write(0x54, VWIDTH * 3)
    vdma.write(0x50, VHEIGHT)
    
    return fbuf0, fbuf1, fbuf2

def video_finalize (vdma, fbuf0, fbuf1, fbuf2):
    # stop DMA
    vdma.write(0x30, 0x8a)
    while ((vdma.read(0x34) & 0x1) == 0):
        pass
    vdma.write(0x00, 0x8a)
    while ((vdma.read(0x04) & 0x1) == 0):
        pass
    
    # delete frame buffers
    fbuf0.freebuffer()
    fbuf1.freebuffer()
    fbuf2.freebuffer()

# main routine
from pynq import Overlay
import time
import math

pl = Overlay("hdmi_sender.bit")
sender = pl.pattern_sender_0
vdma = pl.axi_vdma_0

fbuf0, fbuf1, fbuf2 = video_initialize(vdma)
start_time = current_time = time.time()
current_frame = -1
frame_processed = 0

while current_time - start_time < 20:
    current_time = time.time()
    frame = math.floor((current_time - start_time) * 60)
    if current_frame == frame:
        continue
    current_frame = frame
    frame_processed += 1
    
    sender.register_map.frame = current_frame
    sender.register_map.CTRL.AP_START = 1
    while sender.register_map.CTRL.AP_DONE == 0:
        pass

video_finalize(vdma, fbuf0, fbuf1, fbuf2)
frame_processed