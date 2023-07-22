#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np


@jit
def block(p, s, r=1):
    x = p[0]
    y = p[1]
    z = p[2]
    l = s[0] - 2*r
    w = s[1] - 2*r
    h = s[2] - 2*r
    return r**2 > (x - ((x if x < l/2 else l/2) if x > -l/2 else -l/2))**2\
                 +(y - ((y if y < w/2 else w/2) if y > -w/2 else -w/2))**2\
                 +(z - ((z if z < h/2 else h/2) if z > -h/2 else -h/2))**2


@jit
def fuzzblock(p,s):
    x = p[0]
    y = p[1]
    z = p[2]
    w = s[0]
    l = s[1]
    h = s[2]
    d = min(w-x, w+x, l-y, l+y, h-z, h+z)
    return d


@jit
def fuzzblockround(p,s):
    x = p[0]
    y = p[1]
    z = p[2]
    w = s[0]
    l = s[1]
    h = s[2]
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d

@jit
def fuzzcylinderround(p,h,r):
    x = p[0]
    y = p[1]
    z = p[2]
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d



@jit
def f(x,y,z):
    if 130 > fuzzcylinderround((x,y,z-80),50,5) * fuzzblockround((x,y,z),(10,50,10)):
        return True

    return False

render.renderAndSave(f, f'fuzzbrick.stl', 0.5)

