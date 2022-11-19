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
    rg = 10.1
    ra = 12
    rr = 12
    h = 8
    hg = 10
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return False
    if z < 0:
        return False
#    if z < 1.5:
#        r = (x**2 + y**2)**0.5
#        if r < 10 -(z-1.5):
#            return False
#    if z > 9:
#        r = (x**2 + y**2)**0.5
#        if r < 10 +(z-9):
#            return False
    r = (x**2 + y**2)**0.5
    if z < h:
        phi = math.atan2(y, x)
        if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra:
            return True
    if z < hg:
        if r < rr:
            return True

    return False

render.renderAndSave(f, 'nut4screwlongthick8mmring.stl', 0.1)

