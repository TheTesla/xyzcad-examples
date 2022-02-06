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
    ang = -math.atan2(y,x)
    r = screwprofile((3*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    if r < 10.1:
        return False
    if z < 0:
        return False
    if z < 1:
        r = (x**2 + y**2)**0.5
        if r < 10 -(z-1):
            return False
    if z > 9:
        r = (x**2 + y**2)**0.5
        if r < 10 +(z-9):
            return False
    if z < 10:
        r = (x**2 + y**2)**0.5
        phi = math.atan2(y, x)
        if r * math.cos(((phi*180/math.pi) %60 -30)/180*math.pi) < 15:
            return True
        else:
            return False
    return False

render.renderAndSave(f, 'nut.stl', 0.1)

