import math
import matplotlib.pyplot as plt


def main():

    N = 2000 
    theta1 = math.pi/6
    theta2 = math.pi/4 
    k1 = 226000000 
    k2 = 213000000
    fn1 = 250 
    fn2 = 150 
    zeta1 = 0.012 
    zeta2 = 0.01
    wn1 = fn1*2*math.pi 
    wn2 = fn2*2*math.pi 


    print(real_part1(wn1, wn2, 250, zeta1, zeta2, k1, k2, theta1, theta2))
    G1 = []
    fr = []

    for i in range(N):
        G1.append(real_part1(wn1, wn2, i, zeta1, zeta2, k1, k2, theta1, theta2))
        fr.append(i/(2*math.pi))

    fig, ax = plt.subplots(figsize=(5, 2.7), layout='constrained')

    ax.plot(fr, G1, label="1")
    ax.grid(True)
    ax.set_xlabel('Frequency [Hz]')
    ax.set_ylabel('Real Part')
    plt.legend()
    plt.show()


    return





def real_part(wn1, wn2, w, zeta1, zeta2, k1, k2, theta1, theta2):

    up1 = (wn1*wn1) - (w*w)
    down1 = math.pow((wn1*wn1)-(w*w), 2) + ((math.pow(2*zeta1*wn1, 2))*math.pow(w, 2))
    down1 = down1*k1


    up2 = (wn2*wn2) - (w*w)
    down2 = math.pow((wn2*wn2)-(w*w), 2) + ((math.pow(2*zeta2*wn2, 2))*math.pow(w, 2))
    down2 = down2*k2


    t1 = math.pow(math.cos(theta1), 2)
    t2 = math.pow(math.cos(theta2), 2)

    t1 = t1*(up1/down1)
    t2 = t2*(up2/down2)
    res = t1+t2



    return res 



def real_part1(wn1, wn2, w, zeta1, zeta2, k1, k2, theta1, theta2):

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



def imaginary_part(wn, w, zeta, k, theta1, theta2):

    r = w/wn
    up = -2*zeta*r 

    down = k * (math.pow(up,2) + 4*zeta*zeta*r*r) 
    t1 = math.pow(math.cos(theta1), 2)
    t2 = math.pow(math.cos(theta2), 2)

    t1 = t1*(up/down)
    t2 = t2*(up/down)


    return t1+t2 





if __name__=="__main__":
    main()
