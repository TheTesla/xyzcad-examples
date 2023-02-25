#!/usr/bin/env python3

from xyzcad import render
from numba import jit, prange
import math
import numpy as np

@jit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)

@jit
def f(x,y,z):
    ri = 10
    ro = 15
    rfi = 5/2
    rfo = 9/2
    lf = 30
    h = 15

    if z < 0:
        return False
    if z > h:
        return False
    rf = (z-h/2)**2 + x**2
    if ri**2 > x**2 + y**2:
        return False
    if y>0 and rfi**2 > rf:
        return False
    if y > 0 and rfo**2 > rf and y < lf:
        return True
    if ro**2 < x**2 + y**2:
        return False

    return True



render.renderAndSave(f, 'sodstr.stl', 0.1)

