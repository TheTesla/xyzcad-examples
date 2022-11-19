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
def screw(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg

@jit
def f(x,y,z):

    li = 100
    wi = 32
    h = 40
    d = 10
    lp = 5
    lg = 50
    lf = 15

    rg = 10.1

    if x > li/2 + lf:
        return False

    if x > 0:
        if screw(z-h/2,y,-x,rg):
            return False


    if z < 0:
        return False
    if z > h:
        return False
    if y < -wi/2-d:
        return False
    if y > wi/2+d:
        return False
    if x > li/2 + d:
        xs = x -li/2-d
        if y > wi/2 + d - xs:
            return False
        if y < -wi/2 - d + xs:
            return False
        if z < 0 + xs:
            return False
        if z > h - xs:
            return False

        return True

    if x < -li/2-d:
        return False
    if x > li/2+d:
        return False
    if x > -li/2 and x < li/2 and y > -wi/2 and y < wi/2:
        return False
    if x > -li/2 + lp and x < li/2 - lg and y > -wi/2-d and y < wi/2:
        return False


    return True





render.renderAndSave(f, 'heatingclamp.stl', 0.1)


