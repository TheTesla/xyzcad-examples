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
    l = s[0] - 2*r
    w = s[1] - 2*r
    h = s[2] - 2*r
    return r**2 > (x - ((x if x < l/2 else l/2) if x > -l/2 else -l/2))**2\
                 +(y - ((y if y < w/2 else w/2) if y > -w/2 else -w/2))**2\
                 +(z - ((z if z < h/2 else h/2) if z > -h/2 else -h/2))**2



@jit
def bar(x,y,z,d,xp,yp,zp,xs,ys,zs,r=3):
    xp = xp - xs/2
    yp = yp - ys/2
    zp = zp - zs/2
    return block((x-xp*d,y-yp*d,z-zp*d),(xs*d,ys*d,zs*d),r)


@jit
def f(x,y,z):
    rg = 10.1
    ra = rg*1.3
    d = 2*15
    w = 2
    l = 2
    h = 1
    if ra**2 > (x%d-d/2)**2 + (y%d-d/2)**2 + (z%d-d/2)**2:
        return False
    if screw(x%d-d/2,y%d-d/2,z,rg):
        return False
    if screw(x%d-d/2,z%d-d/2,-y,rg):
        return False
    if screw(z%d-d/2,y%d-d/2,-x,rg):
        return False


    if bar(x,y,z,d,0,0,0,5,1,2):
        return True
    if bar(x,y,z,d,0,0,0,5,2,1):
        return True

    return False

render.renderAndSave(f, f'screwbar45_L_2_2_5.stl', 0.1)

