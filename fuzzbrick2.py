#!/usr/bin/env python3

from xyzcad import render
from numba import njit
import math
import numpy as np


@njit
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


@njit
def fuzzblock(p,s):
    x = p[0]
    y = p[1]
    z = p[2]
    w = s[0]
    l = s[1]
    h = s[2]
    d = min(w-x, w+x, l-y, l+y, h-z, h+z)
    return d


@njit
def fuzzblockround(p,s):
    x = p[0]
    y = p[1]
    z = p[2]
    w = s[0]
    l = s[1]
    h = s[2]
    d = (min(w-x, w+x, 0)**2 + min(l-y, l+y, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d

@njit
def fuzzcylinderround(p,h,r):
    x = p[0]
    y = p[1]
    z = p[2]
    rc = (x**2 + y**2)**0.5
    d = (min(r-rc, r+rc, 0)**2 + min(h-z, h+z, 0)**2)**0.5
    return d



@njit
def roundChamfer(a, b):
    a = max(a,0)
    b = max(b,0)
    #return a + b - (2*a*b)**0.5
    return a + b + (2*a*b)**0.5
    #return max(a + b + (2*a*b)**0.5, a + b - (2*a*b)**0.5)

@njit
def f(x,y,z):
    a = fuzzblockround((x,y,z),(5,50,5))
    b = fuzzblockround((x,y,z),(10,10,50))
    c = fuzzblockround((x,y,z),(50,5,5))

    if 5 > roundChamfer(a-1,b-1) or 1 > a or 1 > b:
    #if 5**2 < (a-10)**2 + (b-10)**2 and 10 > a and 10 > b or (5 > a or 5 > b):
    #if 5**2 < (a-10)**2 + (b-10)**2 + (c-10)**2 \
    #        and 10 > a and 10 > b and 10 > c \
    #        or (5 > a or 5 > b or 5 > c):
        return True

    #if 1 > fuzzblockround((x,y,z),(10,50,10)):
    #    return True
    #if 1 > fuzzblockround((x,y,z),(10,10,50)):
    #    return True
    #if 130 > fuzzcylinderround((x,y,z-80),50,5) * fuzzblockround((x,y,z),(10,50,10)):
    #    return True

    return False

render.renderAndSave(f, f'fuzzbrick.stl', 0.5)

