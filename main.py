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

    real_part, wc = calc_cartesian(N, wn, zeta)

    plt.plot(wc, real_part)
    plt.ylabel("Real Part")
    plt.xlabel("frequency [Hz]")
    plt.show()

    cwc = 650
    
    g = G(wn, cwc, zeta)
    h = H(wn, cwc, zeta)
    fi = phi(g,h)
    a_l = a_lim(kf, g)
    T = T_vector(cwc, wn, zeta, 10)
    V = velocity_vector(T)
    print("wn: {}".format(wn))
    print("phi: {}".format(fi))
    print("alim: {}".format(a_l))
    print("T: {}".format(T))
    print("N: {}".format(V))
    NV, alim = a_lim_vector(kf, wn, zeta, T)

    print("NV: {}".format(NV))
    print("alim: {}".format(alim))

    plt.plot(NV, alim)
    plt.ylabel("A_lim[mm]")
    plt.xlabel("N[rev/min]")
    plt.plot()


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

    res = math.atan(H/G)

    return res


def velocity_vector(T:list):

    res = []
    for t in range(len(T)):


        transient = 60/T[t]
        res.append(transient)


    return res



def T_vector(wc, wn, zeta, n):

    pi = math.pi
    g = G(wn, wc, zeta)
    h = H(wn, wc, zeta)
    
    fi = phi(g, h)
    response = []

    for number in range(n):
        transient = (2*number*pi)+(3*pi)+(2*fi)
        transient = transient/wc
        response.append(transient)

    return response


def a_lim(kf, g):

    transient = 2*kf*g

    return -1/transient


def a_lim_vector(kf, wn, zeta, T_vector_calc):

    w = []
    g_vec = []
    a_lim_vec = []

    for t in T_vector_calc:
        w.append((1/t)*2*math.pi)

    for n in range(len(w)):
        g_vec.append(G(wn, w[n], zeta))

    for g in g_vec:
        a_lim_vec.append(a_lim(kf, g))

    vel = velocity_vector(T_vector_calc)

    return vel, a_lim_vec 



if __name__ == "__main__":
    main()
