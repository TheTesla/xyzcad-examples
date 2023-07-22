#!/usr/bin/env python3

from numba import jit
from xyzcad import render
import math

@jit(nopython=True)
def f(x,y,z):
    if z < 0:
        return False
    if z > 150:
        return False
    rR = 10
    rL = 2
    ang = math.atan2(y,x)
    r = (x**2 + y**2)**0.5
    return rL**2 > (r-rR)**2 + ((z-42*ang/2/math.pi)%42-rR)**2

render.renderAndSave(f, 'meinDonut.stl', 0.3)

