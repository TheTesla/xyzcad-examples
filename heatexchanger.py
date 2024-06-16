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
    b = fuzzBlockRound((x,y,z),(55,55,90))
    c1 =cyl(x-25,y-25,z)-15
    c2 =cyl(x+25,y+25,z)-15
    if b - 20 < 0:
        g = gyroid(x/5+1,y/5,z/5) \
                + 2.3*max(min((sphere(x-25,y-25,z+100))/50,1),0) \
                - 2.3*max(min((sphere(x+25,y+25,z+100))/50,1),0) \
                + 2.3*max(min((sphere(x+25,y+25,z-100))/50,1),0) \
                - 2.3*max(min((sphere(x-25,y-25,z-100))/50,1),0)
        if g > 0.2 or g < -0.2:
            return False
        return True
    if (max(0,5+b-30)**2+max(0,5-b+20)**2+max(0,5-c1)**2+max(0,5-c2)**2)**0.5 -5 > 0:
        return False
    return True

render.renderAndSave(f, 'heatexchanger.stl', 0.7)

