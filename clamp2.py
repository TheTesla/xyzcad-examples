#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np



@jit
def f(x,y,z):
    rc = 3
    rf = 10
    zf = 20
    zn = 5
    yf = 15
    w = 40
    rg = 6
    if x < -w:
        return False
    if x  > w:
        return False
    if y < -rc:
        return False
    if y > 20:
        return False
    ang = -math.atan2((z-zf),x)
    r = 0.3 + (x**2 + (z-zf)**2)**0.5
    if r < rg + 0.1:
        return False
    if (rf**2 > (z-zf)**2 + x**2):
        return True
    if y - abs(z-zn) > 0:
        return False
    if (1 > (z/(zf-rf))**2 + (x/(w/2))**2):
        return False
    if z > 0:
        if (1 > (z/(zf+rf))**2 + (x/w)**2):
            if y > -rc:
                if y < rc:
                    return True
#    if (rc**2 > z**2 + y**2):
#        return True
    return False

render.renderAndSave(f, 'clamp2.stl', 0.1)

