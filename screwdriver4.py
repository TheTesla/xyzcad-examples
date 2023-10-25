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
    l = 170
    ra = 5
    ha = 140
    rr = 14
    ro = 1
    hhn = 100
    rhn = 15
    grip = 2
    wi = 7.6
    if z < 0:
        return False
    if z > l:
        return False

    if x + y < wi/2 and x + y > -wi/2 and x - y < wi/2 and x - y > -wi/2:
        return True

    if z > ha:
        return False

    if ra**2 > x**2 + y**2:
        return True



    if z > hhn and (rhn + hhn - z) > 0 and(rhn + hhn - z)**2 > x**2 + y**2:
        return True

    if z < hhn:
        a = 1
        if z > hhn-5:
            a = (hhn - z)/5
        if z < 5:
            a = z/5
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        if  rhn+grip*a*math.cos(phi*15) > r:
            return True

    if ro**2 < x**2 + y**2:
        return False

    return True

render.renderAndSave(f, 'screwdriver4.stl', 0.3)

