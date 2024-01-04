import math
import matplotlib.pyplot as plt
import avent.libs as lib


def main():

    
    N = 2000 
    kf = 1000000
    theta1 = math.pi/6
    theta2 = -math.pi/4 
    k1 = 226000000 
    k2 = 213000000
    fn1 = 250 
    fn2 = 150 
    zeta1 = 0.012 
    zeta2 = 0.01
    wn1 = fn1*2*math.pi 
    wn2 = fn2*2*math.pi 


    print(real_part(wn1, wn2, 250, zeta1, zeta2, k1, k2, theta1, theta2))
    G1 = []
    fr = []

    for i in range(N):
        G1.append(real_part(wn1, wn2, i, zeta1, zeta2, k1, k2, theta1, theta2))
        fr.append(i/(2*math.pi))

    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax.plot(fr, G1, label="1")
    ax.grid(True)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Real Part')
    plt.legend()
    plt.show()


    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax = create_curves(kf, wn1, wn2, zeta1, zeta2, k1, k2, theta1, theta2, N, 4, ax)
    ax.grid(True)
    ax.set_xlabel('Spindle speed[rev/min]')
    ax.set_ylabel('Alim[mm]')
    plt.legend()
    plt.show()

 
    return


def real_part(wn1, wn2, w, zeta1, zeta2, k1, k2, theta1, theta2):

    r1 = w/wn1
    up1 = 1-(math.pow(r1,2)) 
    down1 = k1 * (math.pow(up1,2) + math.pow(2*zeta1*r1, 2)) 

    r2 = w/wn2
    up2 = 1-(math.pow(r2,2)) 
    down2 = k2 * (math.pow(up2,2) + math.pow(2*zeta2*r2, 2)) 

    t1 = math.pow(math.cos(theta1), 2)
    t2 = math.pow(math.cos(theta2), 2)

    t1 = t1*(up1/down1)
    t2 = t2*(up2/down2)
    res = t1+t2

    return res 



def imaginary_part(wn1, wn2, w, zeta1, zeta2, k1, k2, theta1, theta2):

    r1 = w/wn1
    up1 = -2*zeta1*r1 
    down1 = k1 * ((1-(math.pow(r1,2))) + math.pow(2*zeta1*r1, 2)) 

    r2 = w/wn2
    up2 = -2*zeta2*r2 
    down2 = k2 * ((1-(math.pow(r2,2))) + math.pow(2*zeta2*r2, 2)) 


    t1 = math.pow(math.cos(theta1), 2)
    t2 = math.pow(math.cos(theta2), 2)

    t1 = t1*(up1/down1)
    t2 = t2*(up2/down2)

    return t1+t2 



def create_curves(kf, wn1, wn2, zeta1, zeta2, k1, k2, theta1, theta2, N, k, ax):

    j = 0 
    buffer1 = 0
    buffer2 = 0
    legend_counter = 0

    while j <= k:

        print("k: {}".format(j))
        lab = "k={}".format(j)
        a1_vec, n1_vec, a2_vec, n2_vec = create_vecs(kf, wn1, wn2, zeta1, zeta2, k1, k2, theta1, theta2, j, N)
        if legend_counter == 0:
            ax.plot(n1_vec, a1_vec, color="blue", label="250 Hz")
            ax.plot(n2_vec, a2_vec, color="red", label="150 Hz")
            legend_counter = 1
        else:
            ax.plot(n1_vec, a1_vec, color="blue")
            ax.plot(n2_vec, a2_vec, color="red")

        if j < k and buffer1!= 0:
            if buffer1[0] - n1_vec[0] > 70:

                ax.text(calc_text_loc(n1_vec), min(a1_vec)-0.01, lab)
        else:

            ax.text(calc_text_loc(n1_vec), min(a1_vec)-0.01, lab)


        if j < k and buffer2 != 0:
            if buffer2[0] - n2_vec[0] > 70:

                ax.text(calc_text_loc(n2_vec), min(a2_vec)-0.01, lab)

        else:

            ax.text(calc_text_loc(n2_vec), min(a2_vec)-0.01, lab)




        buffer1 = n1_vec
        buffer2 = n2_vec

        j = j + 1

    ax.axis([0, 15000, 0, 60])
        
    return ax



def create_vecs(kf, wn1, wn2, zeta1, zeta2, k1, k2, theta1, theta2, k, N):

    a1_vec = []
    n1_vec = []
    a2_vec = []
    n2_vec = []
    ch1, ch2 = calc_chatter_freq(N, wn1, wn2, zeta1, zeta2, k1, k2,theta1, theta2)
    


    for i in ch2:

        wc = i
        h = lib.H_ALTINTAS_2DOF(wn1, wc, zeta1, k1, theta1)
        g = lib.G_ALTINTAS_2DOF(wn1, wc, zeta1, k1, theta1)
        e = 2*lib.phi(h,g) + 3*(math.pi)
        a = lib.alim(kf, g)
        n = lib.spindle_speed(k, e, i/(2*math.pi))
        a1_vec.append(a)
        n1_vec.append(n)
        
    for i in ch1:

        wc = i
        h = lib.H_ALTINTAS_2DOF(wn2, wc, zeta2, k2, theta2)
        g = lib.G_ALTINTAS_2DOF(wn2, wc, zeta2, k2, theta2)
        e = 2*lib.phi(h,g) + 3*math.pi
        a = lib.alim(kf, g)
        n = lib.spindle_speed(k, e, i/(2*math.pi))
        a2_vec.append(a)
        n2_vec.append(n)


    return a1_vec, n1_vec, a2_vec, n2_vec


def calc_text_loc(n_vec):

    return n_vec[0]+10

def calc_chatter_freq(N, wn1, wn2, zeta1, zeta2, k1, k2, theta1, theta2):

    i = 0
    j = 0
    ch1 = []
    ch2 = []

    for i in range(N):

        G = real_part(wn1, wn2, i, zeta1, zeta2, k1, k2, theta1, theta2)

        if G < 0 and j != 2: 
            j = 1
            ch1.append(i)

        if j == 1 and G > 0:
            j = 2

        if j == 2 and G < 0:
            ch2.append(i)


    return ch1, ch2




if __name__=="__main__":
    main()
