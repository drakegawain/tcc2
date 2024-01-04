
import math

def G_ALTINTAS_2DOF(wn,  w, zeta, k, theta):

    r = w/wn
    up = 1-(math.pow(r,2)) 
    down = k * (math.pow(up,2) + math.pow(2*zeta*r, 2)) 

    ang = math.pow(math.cos(theta), 2)

    res = ang*(up/down)

    return res 



def H_ALTINTAS_2DOF(wn,  w, zeta, k, theta):

    r = w/wn
    up = -2*zeta*r 
    ab = 1-(math.pow(r,2)) 
    down = k * (math.pow(ab,2) + math.pow(2*zeta*r, 2)) 

    ang = math.pow(math.cos(theta), 2)

    res = ang*(up/down)

    return res 



def spindle_speed(k, e, fc):

    T = ((2*k*math.pi) + e)/(2*math.pi*fc)
    n = 60/T

    return n


def phi(h, g):

    if g > 0 and h < 0:
        return -math.atan(h/g)
    if g < 0 and h < 0:
        return ((-math.pi) + math.atan(h/g))
    if g < 0 and h > 0:
        return ((-math.pi) - math.atan(h/g))
    if g > 0 and h > 0:
        return -2*math.pi + math.atan(h/g)


def alim(kf, g):

    return -1/(2*kf*g)

