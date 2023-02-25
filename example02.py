#!/usr/bin/env python3

from xyzcad import render
from numba import jit


@jit
def f(x,y,z):
    ho = 40
    ro = 13

    if z < 0:
        return False
    if z > ho:
        return False

    r = ro * (ho-z)/ho

    if r < (x**2 + y**2)**0.5:
        return False


    return True

render.renderAndSave(f, 'example02.stl', 0.5)

