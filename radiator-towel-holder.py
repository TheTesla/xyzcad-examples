#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np

@jit
def f(x,y,z):
    if z < 0:
        return False
    if z > 20:
        return False
    r = (x**2 + y**2)**0.5
    if x < 0 and r > 26/2 and r < 26/2+11:
        return True
    r = (x**2 + (y-37)**2)**0.5
    if x > 0 and r > 26/2 and r < 26/2+11:
        return True
    r = (x**2 + y**2)**0.5
    phi = math.atan2(y, x)/3.14159*180
    if phi > 90 and phi < 110  and r > 26/2 +26 +11 and r < 26+26/2+11*2:
        return True
    r = (x**2 + (y-37)**2)**0.5
    phi = math.atan2(y-37, x)/3.14159*180
    if phi < -70 and phi > -90 and r > 26/2 +26 +11 and r < 26+26/2+11*2:
        return True


    return False

render.renderAndSave(f, 'radiator-towel-holder.stl', 1)

