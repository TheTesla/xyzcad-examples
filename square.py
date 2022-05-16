#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np



@jit
def f(x,y,z):
    if x < 3:
        if x > -1:
            if y < 1:
                if y > -1:
                    if z < 1:
                        if z > -1:
                            return True
    return False

render.renderAndSave(f, 'square.stl', 0.1)

