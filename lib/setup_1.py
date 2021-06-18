from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import random

b = 20
S = [1, 3, 4, 5, 8, 9]

def init():
    G = PairingGroup('SS512')
    p = G.order()
    g = G.random(G1)
    a = random.getrandbits(int(p).bit_length())
    while int(a) >= int(p) or int(a) < 2**128 :
        a = random.getrandbits(int(p).bit_length())
    return G, p, g, a

def calculate_gi(g, a, b, p):
    gi = [g]
    exponent = int(a)
    for i in range(1, 2*b+1):
        gi.append(g ** exponent)
        exponent = (exponent * a) % int(p)
    return gi

def calculate_s(g):
    gamma = random.getrandbits(int(p).bit_length())
    while int(gamma) >= int(p) or int(gamma) < 2**128 :
        gamma = random.getrandbits(int(p).bit_length())

    s = g ** gamma
    return gamma, s

def calculate_private_key(gi, gamma, b):
    di = [None]
    for i in range(1, b+1):
        di.append(gi[i] ** gamma)
    return di

def calculate_c1(b, gi, s, S, t):
    tmp = s
    for j in S:
        tmp = tmp * gi[b+1-j]
    return tmp ** t

def calculate_t_K_Hdr(G, g, p, b, gi, s, S):
    t = random.getrandbits(int(p).bit_length())
    while int(t) >= int(p) or int(t) < 2**128 :
        t = random.getrandbits(int(p).bit_length())
   
    K = G.pair_prod(gi[b+1], g) 
    K2 = G.pair_prod(gi[b], gi[1])
    assert K == K2, "pairing" 

    c0 = g ** t
    c1 = calculate_c1(b, gi, s, S, t)
    Hdr = (c0, c1)

    return t, K, Hdr


if __name__ == '__main__':
    G, p, g, a = init()
    gi = calculate_gi(g, a, b, p)       # access g_k by gi[k]
    gamma, s = calculate_s(g)
    di = calculate_private_key(gi, gamma, b)   # access d_k by di[k] 
    t, K, Hdr = calculate_t_K_Hdr(G, g, p, b, gi, s, S)

    ''' todo: Change the following print into write in file '''

    # public
    print("G = ", G)
    print("p = ", p)
    print("g = ", g)
    print("gi = ", gi) # Important : remember to remove gi[b+1]
    print("s = ", s)

    # user
    print("di = ", di)

    #server
    print("Hdr =", Hdr)

    #private
    print("a = ", a)
    print("gamma = ", gamma)
    print("t = ", t)
    print("K = ", K)


