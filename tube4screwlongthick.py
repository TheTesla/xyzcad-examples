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
    rg = 10.0
    d = 3
    h = 10
    r = (x**2 + y**2)**0.5
    if r < rg:
        return False
    if r > rg + d:
        return False
    if z < 0:
        return False
    if z > h:
        return False
    return True

render.renderAndSave(f, 'tube4screwlongthick.stl', 0.1)

