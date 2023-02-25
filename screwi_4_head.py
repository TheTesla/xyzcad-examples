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
    l = 38
    rg = 10
    ra = 5
    rr = 14
    rf = rg+3
    hh = 3
    hi = 20
    f = 2
    if z < 0:
        return False
    phi = math.atan2(y, x)
    r = (x**2 + y**2)**0.5
    if z < hi:
        if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra:
            return False
    if z < hh:
        r = (x**2 + y**2)**0.5
        if r < rr - (hh - z):
            return True
    if z > l:
        return False
    rg = rg + l - z - f if z > l - f else rg
    ang = -math.atan2(y,x)
    r = 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True


    return False

render.renderAndSave(f, 'screwi_4_head.stl', 0.1)

