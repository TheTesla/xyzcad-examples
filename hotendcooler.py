#!/usr/bin/env python3

from xyzcad import render
from numba import jit
import math
import numpy as np

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
    hh = 25
    hr = 10.5
    hri = hr -0.5
    hch = 0.5
    wt = 2
    hd = 7
    cd = 15

    coz = 12
    coh = 20
    cow = 16
    cgw = 5

    cw = 16
    cl = 45 + cd -2
    cfz = 5 + (coz - coh/2)
    cfr = 4.5/2


    if y < cgw/2 and y > -cgw/2 and z < coh/2 +coz:
        return False

    if cfr**2 > (z - cfz)**2 + (x - cl)**2 and y < cw/2 and y > -cw/2:
        return True

    if z < 0:
        return False

    if (hr if z > hch else hri )**2 > x**2 + y**2:
        return False

    if y < cow/2 and y > -cow/2 and z < coh/2+coz and z > -coh/2+coz and x > 0:
        return False


    if block((x-cfr/2-cl/2,y,z-cfz/2-cfr/2),(cl+cfr,cw+2*wt,cfz+cfr),cfr):
        return True

    if z > hh:
        return False

    if x < -hd:
        return False

    if ((hr+(-(wt+z-hh)**2+wt**2)**0.5)**2 if z> hh -wt else \
        ((hr+wt)**2 if z>wt else \
        (hr+(-(wt-z)**2+wt**2)**0.5)**2)) > x**2 + y**2:
        return True


    if not block((x-cd/2,y,z-hh/2),(cd,cw+2*wt,hh),cfr):
        return False



    return True

render.renderAndSave(f, 'hotendcooler.stl', 0.1)

