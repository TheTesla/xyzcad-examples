#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np



@jit
def f(x,y,z):
    r = 3
    if r**2 > x**2 + y**2 + z**2:
        return True
    return False

render.renderAndSave(f, 'ball.stl', 0.3)

