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
def f(x,y,z):
    l = 50
    h = 15
    w = 15
    iw = 2
    ri = 6
    ro = 9
    dz = 0.015
    dy = 0.1
    a = 0.5
    f = 3
    re = 3
    if z < 0:
        return False
    if z > l:
        return False
    xp = a*math.sin((y+h/2-ri)*f)
    if x > xp-iw/2 -z*dz +y*dy and x < xp+iw/2 +z*dz -y*dy and y > -h/2:
        return False
    if ri**2 > x**2 + (y+h/2)**2:
        return False
    if (ro + ((-re+(re**2-(re-z)**2)**0.5) if z < re else
        ((-re+(re**2-(re-(l-z))**2)**0.5) if z > l-re else 0)))**2 > x**2 + (y+h/2)**2:
        return True

    return block((x,y,z-l/2),(w,h,l),re)
    if x > w/2:
        return False
    if x < -w/2:
        return False
    if y > h/2:
        return False
    if y < -h/2:
        return False

    return True

render.renderAndSave(f, 'clipout.stl', 0.1)

