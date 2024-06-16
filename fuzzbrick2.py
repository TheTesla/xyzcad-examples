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
    d += max(min(abs(x),w)-w, min(abs(y),l)-l, min(abs(z),h)-h)
    return d

@njit
def fuzzblockround2(p,s):
    x, y, z = p
    w, l, h = s
    d = ((min(abs(x),w))**0.5 + (min(abs(y),l))**0.5 + (min(abs(z),h))**0.5)**2
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
    #return a + b + (2*a*b)**0.5 #correct
    #return a + b + (a*b)**0.5
    return (a**0.5 + b**0.5)**2
    #return max(a + b + (2*a*b)**0.5, a + b - (2*a*b)**0.5)

@njit
def f(x,y,z):
    a = fuzzcylinderround((x,y,z),70,1) - 5
    b = fuzzblockround((x,y,z),(7,20,7)) - 3
    c = fuzzblockround((x,y,z),(20,5,5)) - 3
    d = fuzzblockround((x,y,z),(2,2,30)) -4
    #d = 0

    #if (min(0,b)**2 + min(0,c)**2 + min(0,a-5)**2)**0.5 > 3:
    #rp = (max(0,b)**0.5 + max(0,c)**0.5 + max(0,d)**0.5)**2 -15
    rp = (max(0,b)**0.5 + max(0,c)**0.5)**2 - 5
    ##rl = (max(0,-c)**0.5 + max(0,-b)**0.5 + max(0,a)**0.5)**2 -6
    rl = (max(0,rp+2)**2 + (-min(0,d))**2)**0.5 - 2 if d < 0 else -1
    #rl = (rp+5)*abs(rp+5) + (d+5)*abs(d+5) - 97  if d < -1 else -1

    #if a > -1000 and (0 > rp or 0 > b or 0 > c):
    if rl < 0 and a > -100 and (0 > rp or 0 > b or 0 > c):

    #if 5.01 < roundChamfer(a,10-b) and (10 > b or 10 > c or 10 > roundChamfer(c-5,b-5)):
    #if 2 < fuzzblockround2((x,y,z),(10,50,10)):
        return True

    return False

@njit
def g(x,y,z):
    d = 30
    f = 3
    rh = 8
    r = d/2 -f
    #a = fuzzblockround(((x+d/2)%d-d/2,(y+d/2)%d-d/2,z),(r,r,3*d/2-f)) - f
    a = fuzzblockround((x,y,z),(r,r,3*d/2-f)) - f
    b = fuzzblockround((x-d,y,z),(r,r,3*d/2-f)) - f
    c = fuzzblockround((x,y-d,z),(r,r,3*d/2-f)) - f

    cx = fuzzcylinderround(((z+d/2)%d-d/2,(y+d/2)%d-d/2,x),5*d,0) - rh
    cy = fuzzcylinderround(((x+d/2)%d-d/2,(z+d/2)%d-d/2,y),5*d,0) - rh
    cz = fuzzcylinderround(((x+d/2)%d-d/2,(y+d/2)%d-d/2,z),5*d,0) - rh
    #cz = fuzzblockround((x,y,z),(0,5,200)) - 1
    #cy = fuzzblockround((x,y,z),(5,0,200)) - 1

    e = f *1.414
    solid = (max(0,e-a)**2 + max(0,e-b)**2 + max(0,e-c)**2)**0.5 - e
    if (max(0,f-solid)**2 + max(0,f-cz)**2 + max(0,f-cy)**2 + max(0,f-cx)**2)**0.5 - f < 0:
        return True
    #if max(-1, a) + max(-1, b) + max(-1, c) < 0:
    #    return True

    #if (max(0,a+f)**2 + max(0,-cz)**2 + max(0,-cy)**2)**0.5 < f:
    #    return True
    #if (max(0,b+f)**2 + (-min(0,cz))**2 + (-min(0,cy))**2)**0.5 < f:
    #    return True
    #if (max(0,c+f)**2 + (-min(0,cz) + (-min(0,cy))**2)**2)**0.5 < f:
    #    return True

    #if (max(0,a)**0.5 + max(0,b)**0.5 + max(0,c)**0.5)**2 < 4*f:
    #    return True
    #if (max(0,a)**0.5 + max(0,c)**0.5)**2 < f:
    #    return True
    #if (max(0,a)**0.5 + max(0,b)**0.5)**2 < f:
    #    return True

    return False

render.renderAndSave(g, f'fuzzbrick.stl', 0.5)

