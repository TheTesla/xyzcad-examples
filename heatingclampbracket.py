#!/usr/bin/env python3

from xyzcad import render
from numba import jit, prange
import math
import numpy as np

@jit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)


@jit
def screw(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg

@jit
def f(x,y,z):

    wi = 32 -0.1
    h = 40 +0.1
    d = 5
    lp = 5
    lg = 50
    lf = 15

    xc = 3
    rg = 10.1
    rgf = rg -4
    tgf = 10

    if (wi/2)**2 > x**2 + y**2:
        return False

    if rgf**2 > (z-h/2)**2 + y**2 and x > lg - tgf:
        return False

    if x < xc:
        return False
    if x > lg:
        return False
    if y < wi/2 + d and y > -wi/2 - d:
        if z > -d and z < 0:
            return True
        if z < h+d and z > h:
            return True

    if z < 0:
        return False
    if z > h:
        return False
    if y < -wi/2:
        return False
    if y > wi/2:
        return False


    return True





render.renderAndSave(f, 'heatingclampbracket.stl', 0.3)


