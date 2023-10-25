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
    l = 30 -0.2
    rg = 10.1
    ri = rg - 0.6
    s = rg*2/3+0.2
    rh = 14.5 -3
    ah = 2
    fh = 20
    fs = 2
    if z < 0:
        return False
    if z > l:
        return False

    p = (0 if z < l-1 else 1+z-l) if z > 1 else 1-z

    if (ri + p)**2 > x**2 + y**2:
        if x>s+p:
            return True
        if x<-s-p:
            return True
        return False



    if z < l:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        a = ah * (z/fs if z < fs else ((l-z)/fs if z > l - fs else 1))
        if  rh + a * (1+math.cos(phi*fh)/2) > r:
            return True
        else:
            return False

    return True

render.renderAndSave(f, 'knurlflat.stl', 0.3)

