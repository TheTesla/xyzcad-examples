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
def screwprofile4(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)

@jit
def screw(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg

@jit
def screw4(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile4((4*(2*math.pi/6*1*z/4+ang+1.25*math.pi))%(2*math.pi)) + (x**2 + y**2)**0.5
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
def f(x,y,z):
    w = 90
    w2 = w + 10
    wguide = 60
    lbase = 30
    lguide = 120
    hbase = 30
    hclamp = 30
    lclamp = lbase + 13
    hdist = 2
    rg = 10.1
    ra = rg*1.3
    rg4 = 10.1
    rguide = 10
    re = 3
    sguide = 30
    d = sguide
    dguide = 5
    fguide = 0.2
    tol = 0.2

    if z < 0:
        return False

    if z > lbase + lguide:
        return False

    if screw(x,y,z,rg):
        return False

    if ra**2 > ((x+d/2)%d-d/2)**2 + (y-d)**2 + (z-d/2)**2:
        return False

    if screw4(z-sguide/2,y-d,-x-d/2,rg4):
        return False

    if z < lclamp - 3:
        if screw4((x+sguide/2)%sguide-sguide/2,y-d,z,rg4):
            return False

    if screw4((x+sguide/2)%sguide-sguide/2,-z+sguide/2,y-hbase/2,rg4):
        if y > hbase/4*3:
            return False


    wprof = (math.cos(2*math.pi*y*fguide) - 1)/2 * dguide
    wprof = wprof if y < hclamp/2 - 1/fguide else 0
    hprof = (math.cos(2*math.pi*x*fguide) - 1)/2 * dguide
    hprof = hprof if abs(x) > wguide/2 - sguide/2 else 1

    lbar = lclamp - (math.cos(2*math.pi*x*fguide) + 1)/2 * \
                    (math.cos(2*math.pi*y*fguide) - 1)/4 * dguide \
                    * (1 if y > hbase/2 else 0) * (1 if z > lbase/2 else 0)
    if block((x,y-hbase/2-hclamp/2-tol/2-hprof/4,z-lbar/2), \
             (w,hclamp-tol-hprof/2,lbar),re):
        return True
    if block((x,y-hclamp/2-hdist/2,z-lbase/2), \
             (wguide-sguide-tol-wprof,hbase+hclamp-hdist,lbase),re):
        return True


    return False

render.renderAndSave(f, f'vicecaddy.stl', 0.1)

