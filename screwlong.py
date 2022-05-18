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
    l = 100
    rg = 6
    if z < 0:
        return False
    if z < 35:
        r = (x**2 + y**2)**0.5
        if  rg - 0.1 > r:
            return True

    if z < 10:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        if  3*(4+math.cos(phi*5)) > r:
            return True
        else:
            return False
    if z > l:
        r = (x**2 + y**2)**0.5
        if r > rg - (z-l):
            return False

    if z > l+3:
        return False
    ang = -math.atan2(y,x)
    r = screwprofile((3*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True


    return False

render.renderAndSave(f, 'screwlong.stl', 0.1)

