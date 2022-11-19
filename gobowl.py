#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np

from functools import partial

@jit
def screwprofile(x):
    x = x / (2*math.pi)
    return min(max(3*(x if x < 0.5 else 1-x), 0.3), 1.2)


@jit
def screw(x,y,z,rg):
    ang = -math.atan2(y,x)
    r = 2*screwprofile((1.5*z+ang+math.pi)%(2*math.pi)) + (x**2 + y**2)**0.5
    return r < rg



@jit
def ball(x,y,z, r=3):
    if r**2 > x**2 + y**2 + z**2:
        return True
    return False

@jit
def cylinder(x,y,z, r=3, height=10):
    if z < 0 or z > height: return False
    if r**2 > x**2 + y**2:
        return True
    return False


screw_radius = 37

@jit
def bowl(x,y,z):
    outer = lambda x,y,z: ball(x, y, z, 51)
    inner = lambda x,y,z: ball(x, y, z, 51-3.2)


    if abs(x) > 60: return False
    if abs(y) > 60: return False

    if abs(z) > 33: return False


    if z>=30:
      if screw(x, y, z, screw_radius + .1): return False


    return outer(x,y,z) and (z <= -31 or not inner(x, y, z))

@jit
def cap(x, y, z):
    outer = lambda x,y,z: ball(x, y, z, 51)
    inner = lambda x,y,z: ball(x, y, z, 51-3.2)

    if z < 25: return False
    if z > 55: return False

    a = (z <= 33 and screw(x, y, z, screw_radius)) or (z >= 33 and outer(x, y, z) and not inner(x, y, z+0.5))

    a = a and not cylinder(x, y, z, r=34, height=33)

    return a

resolution = 0.4
#resolution = 2.



render.renderAndSave(bowl, 'gobowl.stl', resolution)
render.renderAndSave(cap, 'gobowl_cap.stl', resolution)

