#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np
import sys

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
    l = s[0] - 2*r
    w = s[1] - 2*r
    h = s[2] - 2*r
    return r**2 > (x - ((x if x < l/2 else l/2) if x > -l/2 else -l/2))**2\
                 +(y - ((y if y < w/2 else w/2) if y > -w/2 else -w/2))**2\
                 +(z - ((z if z < h/2 else h/2) if z > -h/2 else -h/2))**2


w, l, h = sys.argv[1:]

w = float(w)
l = float(l)
h = float(h)

@jit
def f(x,y,z):
    rg = 10.1
    rb = rg - 0.6
    ra = rg*1.3
    d = 2*15
    #h = 1
    #l = 1
    #w = 1


    for xi in range(l):
        for yi in range(w):
            for zi in range(h):
                xg = (xi+0.5)*d
                yg = (yi+0.5)*d
                zg = (zi+0.5)*d
                if xi != 1:
                    if ra**2 > (x-xg)**2 + (y-yg)**2 + (z-zg)**2:
                        return False
    for xi in range(l):
        for yi in range(w):
            xg = (xi+0.5)*d
            yg = (yi+0.5)*d
            if xi == 1:
                if rb**2 > (x-xg)**2 + (y-yg)**2:
                    return False
            if screw(x-xg,y-yg,z,rg):
                return False
    for xi in range(l):
        for zi in range(h):
            xg = (xi+0.5)*d
            zg = (zi+0.5)*d
            if xi != 1:
                if screw(x-xg,z-zg,-y,rg):
                    return False
    for zi in range(h):
        for yi in range(w):
            zg = (zi+0.5)*d
            yg = (yi+0.5)*d
            if x < d or x > 2*d:
                if screw(z-zg,y-yg,-x,rg):
                    return False


    if not block((x-l*d/2,y-w*d/2,z-h*d/2),(l*d,w*d,h*d),3):
        return False


    return True

render.renderAndSave(f, f'screwbar4_45_bearing_{l:02.0f}_{w:02.0f}_{h:02.0f}.stl', 0.1)

