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
    ra = 5
    hhn = 20
    wi = 7.6
    if z < 0:
        return False
    if z > l:
        return False

    if x + y < wi/2 and x + y > -wi/2 and x - y < wi/2 and x - y > -wi/2:
        return True


    if z < hhn+1:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        rrel = math.cos(((phi*180/math.pi) %60 -30)/180*math.pi)
        morph = (hhn -z +1 if z>hhn else 1) if z > 1 else z
        rrel = rrel * morph + 1.2*(1-morph)
        if r * rrel < ra:
            return True




    return False

render.renderAndSave(f, 'screwbit4.stl', 0.1)

