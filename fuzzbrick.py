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
def fuzzsphere(p,r=1):
    x = p[0]
    y = p[1]
    z = p[2]
    return x**2 + y**2 + z**2 - r**2

@jit
def fuzzblock(p,s):
    x = p[0]
    y = p[1]
    z = p[2]
    l = s[0]
    w = s[1]
    h = s[2]
    xd = x**2 - l**2
    yd = y**2 - w**2
    zd = z**2 - h**2
    return xd**2 + yd**2 + zd**2


@jit
def rSphere(x,y,z):
    if 0 > x*y+x*z+y*z:
        return 0
    return x+y+z+((x*y+x*z+y*z)/2)**0.5

@jit
def fuzzblock2(p,s):
    x,y,z = p
    l,w,h = s
    r1 = rSphere(x+l/2,y+w/2,z+h/2)
    r2 = rSphere(x+l/2,y+w/2,-z+h/2)
    r3 = rSphere(x+l/2,-y+w/2,z+h/2)
    r4 = rSphere(x+l/2,-y+w/2,-z+h/2)
    r5 = rSphere(-x+l/2,y+w/2,z+h/2)
    r6 = rSphere(-x+l/2,y+w/2,-z+h/2)
    r7 = rSphere(-x+l/2,-y+w/2,z+h/2)
    r8 = rSphere(-x+l/2,-y+w/2,-z+h/2)
    return min(r1,r2,r3,r4,r5,r6,r7,r8)


@jit
def bar(x,y,z,d,xp,yp,zp,xs,ys,zs,r=3):
    xp = xp - xs/2
    yp = yp - ys/2
    zp = zp - zs/2
    return block((x-xp*d,y-yp*d,z-zp*d),(xs*d,ys*d,zs*d),r)


@jit
def f(x,y,z):
    if 20 < fuzzblock2((x,y,z),(60,30,30)):
        return True

    return False

render.renderAndSave(f, f'fuzzbrick.stl', 0.5)

