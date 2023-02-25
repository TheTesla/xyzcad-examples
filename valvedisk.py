#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np

@jit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)


@jit
def f(x,y,z):
    ld = 3
    rg = 9.6
    rh = 13
    rp = 11
    rpp = 1
    if z < 0:
        return False
    if rg**2 > x**2 + y**2:
        return False
    if rpp**2 > (z-ld)**2 + ((x**2 + y**2)**0.5 - rp)**2:
        return True
    if z < ld:
        if rh**2 > x**2 + y**2:
            return True


    return False

render.renderAndSave(f, 'valvedisk.stl', 0.1)

