#!/usr/bin/env python3

from numba import jit
from xyzcad import render

@jit(nopython=True)
def f(x,y,z):
    rK = 10
    rZ = 5
    if rZ**2 > x**2 + y**2:
        return False
    return rK**2 > x**2 + y**2 + z**2

render.renderAndSave(f, 'meineKugel.stl', 1.3)

