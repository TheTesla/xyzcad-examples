#!/usr/bin/env python3

from xyzcad import render
from numba import jit
from math import cos, sin
import numpy as np

@jit
def f(x,y,z):
    if x > -65 and x < +65 and y < 10 and y > -10:
        zv = 50 *1/(1+2**(-x/5))
        if z - 3 < zv and z +3 > zv:
            return True
    return False

@jit
def g(x,y,z):
    if z < 0:
        return False
    base = 3**2> (x - ((x if x < 200 else 200) if x > 30 else 30))**2 \
                 +(y - ((y if y <  10 else  10) if y > -10 else -10))**2 \
                 +(z - ((z if z < 1 else  1) if z > 0 else 13))**2
    if base:
        return True
    res = 5
    for i in range(30*res, 200*res):
        xp = i/res
        yp = 0.
        zp = 25./(1+2**(10*cos((xp/230*360)/180*3.14159)))
        if (3*(x - xp))**2 + (y - yp)**2 + (3*(z - zp))**2 < 9**2:
            return True
    return False

render.renderAndSave(g, 'furniture-handle.stl', 0.3)

