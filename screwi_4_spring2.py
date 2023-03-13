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
    l = 40
    rg = 10 - 0.2
    ra = 5
    f = 2
    if z < 0:
        return False
    phi = math.atan2(y, x)
    r = (x**2 + y**2)**0.5
    if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra:
        return False
    if z > l:
        return False
    rg = rg + l - z - f if z > l - f else rg
    rg = rg + z - f if z < f else rg
    ang = -math.atan2(y,x)
    r = (x**2 + y**2)**0.5

    if z > 10 and z < l-10:
        r += 6*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi))-1.2
        if r < rg:
            return True
        return False
    else:
        r += 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi))
        if r < rg:
            return True
    return False

render.renderAndSave(f, 'screwi_4_spring2.stl', 0.1)
