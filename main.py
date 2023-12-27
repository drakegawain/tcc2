import math
import matplotlib.pyplot as plt

def main():

    N = 2000 
    damp = 2000
    k = 20000000
    m = 50
    kf = 2000000000
    fn = 119
    zeta = 0.026
    wn = math.sqrt(k/m)

    G, wc = calc_cartesian(N, wn, zeta)

    plt.plot(wc, G)
    plt.ylabel("Real Part")
    plt.show()

    cwc = 650

    return

def R(wn, wc, zeta):

    delta_w = (wn*wn) - (wc*wc)
    delta_w = delta_w*delta_w
    zeta_part = (2*zeta*wn)
    zeta_part = zeta_part*zeta_part*wc*wc
    res = delta_w + zeta_part

    return res


def G(wn, wc, zeta):


    transient = (wn*wn) - (wc*wc)
    res = transient / R(wn, wc, zeta)


    return res


def H(wn, wc, zeta):

    transient = -2*zeta*wn*wc
    res = transient / R(wn, wc, zeta)

    return res



def calc_cartesian(wc_range, wn, zeta):

    res = []
    wc_vector = []

    for wc in range(wc_range):
        res.append(G(wn, wc, zeta)) 
        wc_vector.append(wc)
        
    return res, wc_vector


def phi(G, H):

    res = math.degrees(math.atan(H/G))

    return res


def velocity_vector(T):

    res = []
    for t in range(T):

        transient = 60/t
        res.append(transient)


    return res



def T_vector(wc, wn, zeta, n, phi):

    pi = math.pi
    G = G(wn, wc, zeta)
    H = H(wn, wc, zeta)
    phi = phi(G, H)
    response = []

    for number in range(n):
        transient = (2*number*pi)+(3*pi)+(2*phi)
        transient = transient/wc
        response.append(transient)

    return response


if __name__ == "__main__":
    main()
