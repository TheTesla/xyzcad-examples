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
    l = 45
    rg = 10 - 0.2
    ra = 5
    ra1 = 10
    rr = 14
    f2 = 2
    hh = 12
    h1 = 3
    h2 = 3
    if z < 0:
        return False
    if z < hh:
        r = (x**2 + y**2)**0.5
        if r < rr - (hh - z):
            return True
        phi = math.atan2(y, x)
        if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra1:
            return True
        else:
            return False
    phi = math.atan2(y, x)
    r = (x**2 + y**2)**0.5
    if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra and z < l-f2:
        return False
    if z > l:
        return False
    rg = rg + l - z - f2 if z > l - f2 else rg
    ang = -math.atan2(y,x)
    r = (x**2 + y**2)**0.5

    if z > hh + h1 and z < l-h2-f2:
        r += 6*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi))-1.2
        if r < rg:
            return True
        return False
    else:
        r += 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi))
        if r < rg:
            return True
    return False

render.renderAndSave(f, 'screw6_4_spring3.stl', 0.1)

