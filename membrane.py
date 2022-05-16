#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np



@jit
def profile(x,pn,ph,pxmin,pxmax):
    return ph*(1-math.cos(pn*(x-pxmin)*math.pi*2/(pxmax-pxmin)))/2


@jit
def f(x,y,z):
    d = 1
    n = 2
    ri = 20 /2
    rim = 25 /2
    rom = 45 /2
    ro = 50 /2
    h = 5
    #if x < 0:
    #    return False
    if z < 0:
        return False
    if z > 10:
        return False

    r = (x**2 + y**2)**0.5
    if r > ro:
        return False
    if r < ri:
        return False
    zp = 0
    if r < rom and r > rim:
        zp = profile(r,n,h,rim,rom)
        zp_d = (profile(r+0.001,n,h,rim,rom) - zp)/0.001

    if z > zp + d/2: #*(1+zp_d**2)**0.5:
        return False
    if z < zp - d/2:
        return False


    return True

render.renderAndSave(f, 'membrane1.stl', 0.1)

