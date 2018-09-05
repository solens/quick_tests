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

x_drawing = [[1,0,0,0,0,0,0,1],
     [0,1,0,0,0,0,1,0],
     [0,0,1,0,0,1,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,1,0,0,1,0,0],
     [0,1,0,0,0,0,1,0],
     [1,0,0,0,0,0,0,1]]


vent1 = [
     [1,1,1,0,0,0,0,0],
     [0,1,1,0,0,0,0,0],
     [0,0,1,1,0,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,1,1,1,1],
     [0,0,1,1,0,0,1,1],
     [1,1,1,0,0,0,0,1],
     [1,1,0,0,0,0,0,0]
     ]

vent2 = [
     [0,1,1,1,0,0,0,0],
     [0,0,1,1,0,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,0,1,0,0,0],
     [0,0,0,1,1,1,0,0],
     [1,1,1,1,0,1,1,0],
     [1,1,0,0,0,0,1,1],
     [1,0,0,0,0,0,0,1]
     ]

vent3 = [
     [0,0,1,1,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,0,1,0,0,0],
     [0,0,0,0,1,0,0,0],
     [0,1,1,1,1,0,0,0],
     [1,1,1,0,1,1,0,0],
     [1,0,0,0,0,1,1,0],
     [0,0,0,0,0,1,1,1]
     ]

vent4 = [
     [0,0,0,1,1,1,0,0],
     [0,0,0,0,1,1,0,0],
     [1,0,0,0,1,0,0,0],
     [1,1,0,0,1,0,0,0],
     [1,1,1,1,1,0,0,0],
     [0,0,0,0,1,0,0,0],
     [0,0,0,0,1,1,0,0],
     [0,0,0,0,1,1,1,0]
     ]

vent5 = [
     [0,0,0,0,0,1,1,1],
     [1,0,0,0,0,1,1,0],
     [1,1,0,0,1,1,0,0],
     [1,1,1,0,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,0,1,0,0,0],
     [0,0,0,1,1,0,0,0],
     [0,0,0,1,1,1,0,0]
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

def draw_shape(shape_name):
    serial = spi(port=0, device=0, gpio=noop()) 
    device = max7219(serial, cascaded=1 or 1, block_orientation=90, rotate=0)

    device.contrast(16)

    shapes = {
        "door": door,
        "vent": vent,
        "light": light
    }

    if shape_name == "all":
        show_message(device, "ALL", fill="white", font=proportional(CP437_FONT),scroll_delay = 0.1)
    else:
        for screen_drawing in shapes[shape_name]:
            for i in range(5):
                with canvas(device) as draw:
                    for pos in bin_to_position(screen_drawing):
                        draw.point(pos,fill = "white")
                    time.sleep(0.1)


def bin_to_position(bin_matrix):
    pos_matrix = np.argwhere(zip(*bin_matrix))
    return pos_matrix

if __name__ == "__main__":

    try:
        draw_shape("all")
    except KeyboardInterrupt:
        pass