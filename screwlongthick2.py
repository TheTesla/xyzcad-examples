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
    l = 172
    lh = 20
    ld = 7
    ls = 30
    rg = 10 -0.2
    rf = rg+3
    rh = 20
    ah = 2
    fh = 20
    fs = 2
    if z < 0:
        return False
    if z < lh + ls + ld:
        r = (x**2 + y**2)**0.5
        if  rg - 0.6 > r:
            return True
    if z < lh + ld:
        r = (x**2 + y**2)**0.5
        if  rf > r:
            return True
    if z < lh:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        a = ah * (z/fs if z < fs else ((lh-z)/fs if z > lh - fs else 1))
        if  rh + a * (1+math.cos(phi*fh)/2) > r:
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
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < rg:
        return True


    return False

render.renderAndSave(f, 'screwlongthick2.stl', 0.1)

