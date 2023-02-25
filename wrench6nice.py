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
    l = 120
    lh = 80
    ra = 10 +0.1
    rr = 14
    ro = 15
    hh = 15
    rh = 20
    ah = 2
    fh = 20
    fs = 2
    if z < 0:
        return False
    if z > hh+l:
        return False
    if z > l:
        r = (x**2 + y**2)**0.5
        if r < rr - ((hh+l) - z):
            return False
        phi = math.atan2(y, x)
        if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < ra:
            return False


    if z > lh and (rh + lh - z) > 0 and (rh + lh - z)**2 > x**2 + y**2:
        return True




    if z < lh:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        a = ah * (z/fs if z < fs else ((lh-z)/fs if z > lh - fs else 1))
        if  rh + a * (1+math.cos(phi*fh)/2) > r:
            return True
        else:
            return False



    if ro**2 < x**2 + y**2:
        return False

    return True

render.renderAndSave(f, 'wrench6nice.stl', 0.1)

