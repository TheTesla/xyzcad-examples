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
def honeycomb(x,y,z,s,d,ang=0):
    k = math.cos(30/180*math.pi)
    c = math.tan(30/180*math.pi)
    xd = d/c+s/k+s*c

    yh = y % (2*s+2*d) -s -d
    xh = x % (2*xd) - xd
    r = (xh**2 + yh**2)**0.5
    phi = math.atan2(yh, xh)
    if r * math.cos(((phi*180/math.pi+ang) %60 -30)/180*math.pi) < s:
        return True

    yh = (y+d+s) % (2*s+2*d) -s -d
    xh = (x+xd) % (2*xd) - xd
    r = (xh**2 + yh**2)**0.5
    phi = math.atan2(yh, xh)
    if r * math.cos(((phi*180/math.pi+ang) %60 -30)/180*math.pi) < s:
        return True

    return False


@jit
def f(x,y,z):
    h = 10
    h1 = 5
    w = 30
    l = 40
    s = 2
    s1 = 1.5
    d = 1/3
    co = math.tan(30/180*math.pi)
    xo = (d+s)*co
    k = math.cos(30/180*math.pi)
    c = math.tan(30/180*math.pi)
    xd = d/c+(s/3-d)/k+(s/3-d)*c

    if z < 0:
        return False
    if z > h:
        return False
    if x > l/2:
        return False
    if x < -l/2:
        return False
    if y > w/2:
        return False
    if y < -w/2:
        return False


    if z < h1:
        #if not honeycomb(x,y,z,s/3-d,d):
        if honeycomb(x,y,z,s-d/2,d/2,30):
            return False


    if honeycomb(x,y,z,s-d,d):
        return False


#    s1 = s1*z/h
#    if honeycomb(x+xo,y+d+s,z,s1,d+s-s1,30):
#        return True
#    if honeycomb(x-xo,y+d+s,z,s1,d+s-s1,30):
#        return True

#    d2 = d*(1-z/h1)

#    if z < h1:
#        if honeycomb(x,y,z,s+d-d2,d2) and honeycomb(x+xo,y+d+s,z,s+d2,d-d2):
#            return False
#        return True
#    return False




#    if x % s < d:
#        return True
#    if (y*math.cos(60/180*math.pi) + x*math.sin(60/180*math.pi)) % s < d:
#        return True


    return True

render.renderAndSave(f, 'print-sieve.stl', 0.1)

