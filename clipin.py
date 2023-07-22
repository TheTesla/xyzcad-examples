#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np


@jit
def f(x,y,z):
    l = 50
    h = 15
    w = 6
    iw = 2
    ri = 3
    ro = 4
    dz = 0.015
    dy = 0.1
    a = 0.5
    f = 3
    if z < 0:
        return False
    if z > l:
        return False
    xp = a*math.sin((y+h/2-ro)*f) if y > -h/2+ro else 0
    if x > xp-iw/2 and x < xp+iw/2 and y > -h/2:
        return False
    if ri**2 > x**2 + (y+h/2)**2:
        return False
    if ro**2 > x**2 + (y+h/2)**2:
        return True
    if x > xp+w/2 -z*dz -y*dy:
        return False
    if x < xp-w/2 +z*dz +y*dy:
        return False
    if y > h/2:
        return False
    if y < -h/2:
        return False

    return True

render.renderAndSave(f, 'clipin.stl', 0.1)

