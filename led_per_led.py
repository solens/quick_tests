#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Copyright (c) 2017-18 Richard Hull and contributors
# See LICENSE.rst for details.


import re
import time
import argparse
import os
import sys
import numpy as np

from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.virtual import viewport
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT, LCD_FONT


vent1 = [
     [1,1,0,0,0,0,0,1],
     [0,1,1,0,0,0,1,1],
     [0,0,1,1,0,1,1,0],
     [0,0,0,1,1,1,0,0],
     [0,0,1,1,1,0,0,0],
     [0,1,1,0,1,1,0,0],
     [1,1,0,0,0,1,1,0],
     [1,0,0,0,0,0,1,1]
     ]

vent2 = [
     [0,1,1,0,0,0,0,0],
     [0,0,1,1,0,0,0,1],
     [0,0,0,1,0,0,1,1],
     [0,0,0,1,1,1,1,0],
     [0,1,1,1,1,0,0,0],
     [1,1,0,0,1,0,0,0],
     [1,0,0,0,1,1,0,0],
     [0,0,0,0,0,1,1,0]
     ]

vent3 = [
     [0,0,1,1,0,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,0,1,0,0,1],
     [0,1,1,1,1,0,1,1],
     [1,1,0,1,1,1,1,0],
     [1,0,0,1,0,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,0,1,1,0,0]
     ]

vent4 = [
     [0,0,0,0,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,0,0,0,0],
     [1,1,0,1,1,1,1,0],
     [0,1,1,1,1,0,1,1],
     [0,0,0,0,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,0,0,0,0]
     ]

vent5 = [
     [0,0,0,0,0,1,1,0],
     [1,0,0,0,1,1,0,0],
     [1,1,0,0,1,0,0,0],
     [0,1,1,1,1,0,0,0],
     [0,0,0,1,1,1,1,0],
     [0,0,0,1,0,0,1,1],
     [0,0,1,1,0,0,0,1],
     [0,1,1,0,0,0,0,0]
     ]

light1 = [
     [0,0,0,1,1,0,0,0],
     [0,0,1,0,0,1,0,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,0,1,0,0,1,0,0],
     [0,0,1,0,0,1,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,1,0,0,0]
     ]

light2 = [
     [0,0,0,1,1,0,0,0],
     [0,0,1,1,1,1,0,0],
     [0,1,1,1,1,1,1,0],
     [0,1,1,1,1,1,1,0],
     [0,0,1,1,1,1,0,0],
     [0,0,1,1,1,1,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,1,0,0,0]
     ]

door1 = [
     [0,1,1,1,1,1,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,1,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0]
     ]

door2 = [
     [0,1,1,0,0,0,0,0],
     [0,1,0,1,1,0,0,0],
     [0,1,0,0,0,1,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,0,1,0],
     [0,1,0,0,0,1,1,0],
     [0,1,0,0,0,0,1,0]
     ]

a = [
     [0,0,1,1,1,1,0,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,1,1,1,1,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,0,0,1,1,0]
     ]

l = [
     [0,0,0,0,0,1,1,1],
     [0,0,0,0,0,1,1,0],
     [0,0,0,0,0,1,1,0],
     [0,0,0,0,0,1,1,0],
     [0,0,0,0,0,1,1,0],
     [0,0,0,0,0,1,1,0],
     [0,1,1,0,0,1,1,0],
     [0,1,1,1,1,1,1,0]
     ]

dark = [
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0],
        [0,0,0,0,0,0,0,0]
        ]
vent = [vent1,vent2,vent3,vent4,vent5,dark]
light = [light1,light2,light1,light2,dark]
door = [door1,door2,door1,door2,dark]
all_screen = [a,dark,l,dark,l,dark]

def demo(n, block_orientation, rotate,x):
    # create matrix device
    serial = spi(port=0, device=0, gpio=noop())
    device = max7219(serial, cascaded=n or 1, block_orientation=block_orientation, rotate=rotate or 0)

    device.contrast(16)

    time.sleep(1)
    for screen_drawing in vent:
        for i in range(5):
            with canvas(device) as draw:
                for pos in bin_to_position(screen_drawing):
                    draw.point(pos,fill = "white")
                time.sleep(0.1)

def bin_to_position(bin_matrix):
    pos_matrix = np.argwhere(zip(*bin_matrix))
    return pos_matrix

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='matrix_demo arguments',
        formatter_class=argparse.ArgumentDefaultsHelpFormatter)

    parser.add_argument('--cascaded', '-n', type=int, default=1, help='Number of cascaded MAX7219 LED matrices')
    parser.add_argument('--block-orientation', type=int, default=90, choices=[0, 90, -90], help='Corrects block orientation when wired vertically')
    parser.add_argument('--rotate', type=int, default=0, choices=[0, 1, 2, 3], help='Rotate display 0=0°, 1=90°, 2=180°, 3=270°')
    parser.add_argument('--symbol', type=int, default=3, help='Symbol to print between 0 and 255')

    args = parser.parse_args()

    try:
        demo(args.cascaded, args.block_orientation, args.rotate,args.symbol)
    except KeyboardInterrupt:
        pass