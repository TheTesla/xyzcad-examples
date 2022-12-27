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
def screw(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((4*(2*math.pi/6*1*z/4+ang+1.25*math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg

@jit
def block(p, s, r=1):
    x = p[0]
    y = p[1]
    z = p[2]
    w = s[0] - 2*r
    l = s[1] - 2*r
    h = s[2] - 2*r
    return r**2 > (x - ((x if x < w/2 else w/2) if x > -w/2 else -w/2))**2\
                 +(y - ((y if y < l/2 else l/2) if y > -l/2 else -l/2))**2\
                 +(z - ((z if z < h/2 else h/2) if z > -h/2 else -h/2))**2


@jit
def f(x,y,z):
    rg = 10.1
    ra = rg*1.3
    d = 2*15
    h = 1
    l = 1
    w = 1
    for xi in range(l):
        for yi in range(w):
            for zi in range(h):
                xg = (xi+0.5)*d
                yg = (yi+0.5)*d
                zg = (zi+0.5)*d
                if ra**2 > (x-xg)**2 + (y-yg)**2 + (z-zg)**2:
                    return False
    for xi in range(l):
        for yi in range(w):
            xg = (xi+0.5)*d
            yg = (yi+0.5)*d
            if screw(x-xg,y-yg,z,rg):
                return False
    for xi in range(l):
        for zi in range(h):
            xg = (xi+0.5)*d
            zg = (zi+0.5)*d
            if screw(x-xg,z-zg,-y,rg):
                return False
    for zi in range(h):
        for yi in range(w):
            zg = (zi+0.5)*d
            yg = (yi+0.5)*d
            if screw(z-zg,y-yg,-x,rg):
                return False


    if not block((x-w*d/2,y-l*d/2,z-h*d/2),(w*d,l*d,h*d),3):
        return False

#    if z < 0:
#        return False
#    if y < 0:
#        return False
#    if x < 0:
#        return False
#    if z > h*d:
#        return False
#    if y > w*d:
#        return False
#    if x > l*d:
#        return False


    return True

render.renderAndSave(f, 'screwbar4_45_1_1.stl', 0.1)

