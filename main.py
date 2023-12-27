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


    return


def G(wn, wc, zeta):


    transient = (wn*wn) - (wc*wc)
    res = transient / ((transient*transient) + ((2*zeta*wn)*(2*zeta*wn))*(wc*wc))


    return res


def calc_cartesian(wc_range, wn, zeta):

    res = []
    wc_vector = []

    for wc in range(wc_range):
        res.append(G(wn, wc, zeta)) 
        wc_vector.append(wc)
        
    return res, wc_vector



def velocity(T):

    res = 60/T

    return res



def T_vector(wc, n, phi):

    pi = math.pi
    response = []

    for number in range(n):
        transient = (2*number*pi)+(3*pi)+(2*phi)
        transient = transient/wc
        response.append(transient)

    return response


if __name__ == "__main__":
    main()
