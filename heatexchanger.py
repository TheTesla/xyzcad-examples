#!/usr/bin/env python3

from xyzcad import render
from numba import njit
from math import sin, cos
import numpy as np


@njit
def gyroid(x,y,z):
    return sin(x)*cos(y) + sin(y)*cos(z) + sin(z)*cos(x)

@njit
def fuzzBlockRound(p,s):
    x, y, z = p
    w, l, h = s
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    d += max(min(abs(x),w)-w, min(abs(y),l)-l, min(abs(z),h)-h)
    return d


@njit
def cone(x,y,z):
    return (x**2 + y**2)**0.5 + z

@njit
def sphere(x,y,z):
    return (x**2 + y**2 + z**2)**0.5

@njit
def cyl(x,y,z):
    return (x**2 + y**2)**0.5

@njit
def f(x,y,z):
    roe = 5
    tw = 5
    w = 25
    rh = 10
    rf = 2
    sh = 12
    l = 50
    dg = 3
    #if x > y:
    #    return False
    b = fuzzBlockRound((x,y,z),(w-roe,w-roe,l-tw))
    c1 =cyl(x-sh,y-sh,z)-rh
    c2 =cyl(x+sh,y+sh,z)-rh
    if b - roe < 0:
        g = gyroid(x/dg+1,y/dg,z/dg) \
                + 2.3*max(min((sphere(x-sh,y-sh,z+l))/25,1),0) \
                - 2.3*max(min((sphere(x+sh,y+sh,z+l))/25,1),0) \
                + 2.3*max(min((sphere(x+sh,y+sh,z-l))/25,1),0) \
                - 2.3*max(min((sphere(x-sh,y-sh,z-l))/25,1),0)
        if g > 0.2 or g < -0.2:
            return False
        return True
    if (max(0,rf+b-roe-tw)**2+max(0,rf-b+roe)**2+max(0,rf-c1)**2+max(0,rf-c2)**2)**0.5 -rf > 0:
        return False
    return True

render.renderAndSave(f, 'heatexchanger.stl', 0.2)

