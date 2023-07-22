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
def screw(x,y,z,rg=9.8):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg


@jit
def f(x,y,z):
    ro = 15
    rg = 15
    rgi = 12
    ri = 12
    if x < -20:
        return False
    if x > 20:
        return False
    if y < -20:
        return False
    if y > 20:
        return False
    if z < -20:
        return False
    if z > 20:
        return False

    if ri**2 > x**2 + y**2:
        return False
    if rgi**2 > x**2 + z**2:
        return False
    if rgi**2 > z**2 + y**2:
        return False
    if ro**2 > x**2 + y**2:
        return True


    if screw(x,-z,y,rg):
        return True
    if screw(-z,y,x,rg):
        return True

    return False

render.renderAndSave(f, 'airmixer.stl', 0.3)

