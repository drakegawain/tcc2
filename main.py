import math
import matplotlib.pyplot as plt

def main():

    N = 1000
    damp = 2000
    k = 20000000
    m = 50
    kf = 2000000000
    fn = 119
    zeta = 0.026
    wn = fn*2*math.pi 

    G = []


    for i in range(N):
        G.append(real_part(wn, i, zeta))
    
    wc = range(N)

    plt.plot(wc, G)
    plt.ylabel("Real Part")
    plt.xlabel("frequency [Hz]")
    plt.show()

    i = int(wn)+1 
    a_vec = []
    n_vec = []


    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax = create_curves(kf, wn, i, zeta, i, N, 20, ax)
    ax.grid(True)
    ax.set_xlabel('Spindle speed[rev/min]')
    ax.set_ylabel('Alim[mm]')
    plt.show()

    


    return

def calc_text_loc(n_vec):

    return n_vec[0]+10



def create_curves(kf, wn, wc, zeta, i, N, k, ax):

    j = 1
    buffer = 0

    while j <= k:

        print("k: {}".format(j))
        lab = "k={}".format(j)
        a_vec, n_vec = create_vecs(kf, wn, wc, zeta, i, N, j)
        ax.plot(n_vec, a_vec, color="blue")
        if j < k and buffer != 0:
            if buffer[0] - n_vec[0] > 70:

                ax.text(calc_text_loc(n_vec), .005, lab)

        else:

            ax.text(calc_text_loc(n_vec), .005, lab)

        buffer = n_vec

        j = j + 1

    ax.axis([0, 1400, 0, 0.3])
        
    return ax



def create_vecs(kf, wn, wc, zeta, i, N, k):

    a_vec = []
    n_vec = []

    while i < N:

        wc = i
        h = imaginary_part(wn, wc, zeta)
        g = real_part(wn, wc, zeta)
        e = 2*phi(h,g) + 3*math.pi
        a = alim(kf, g)
        n = spindle_speed(k, e, i/(2*math.pi))
        a_vec.append(a*1000)
        n_vec.append(n)

        i = i + 1

    return a_vec, n_vec





def spindle_speed(k, e, fc):

    T = ((2*k*math.pi) + e)/(2*math.pi*fc)
    n = 60/T

    return n


def real_part(wn, w, zeta):

    up = (wn*wn) - (w*w)
    down = math.pow((wn*wn)-(w*w), 2) + ((math.pow(2*zeta*wn, 2))*math.pow(w, 2))

    return up/down

def imaginary_part(wn, w, zeta):

    up = -2*zeta*wn*w 
    down = math.pow((wn*wn)-(w*w), 2) + ((math.pow(2*zeta*wn, 2))*math.pow(w, 2))

    return up/down



def phi(h, g):

    if g > 0 and h < 0:
        return -math.atan(h/g)
    if g<0 and h < 0:
        return -math.pi + math.atan(h/g)
    if g < 0 and h > 0:
        return -math.pi - math.atan(h/g)
    if g > 0 and h < 0:
        return -2*math.pi + math.atan(h/g)


    return





def alim(kf, g):

    return -1/(2*kf*g)



if __name__ == "__main__":
    main()
