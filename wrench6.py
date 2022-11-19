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
    l = 50
    ra = 10 +0.1
    rr = 14
    ro = 15
    hh = 15
    hhn = 20
    rhn = 25
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


    if z > hhn and (rhn + hhn - z) > 0 and(rhn + hhn - z)**2 > x**2 + y**2:
        return True

    if z < hhn:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        if  6*(6+math.cos(phi*5)) > r:
            return True

    if ro**2 < x**2 + y**2:
        return False

    return True

render.renderAndSave(f, 'wrench6.stl', 0.2)

