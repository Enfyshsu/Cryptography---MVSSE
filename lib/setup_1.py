from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import secrets


def init():
    G = PairingGroup('SS512')
    p = G.order()
    g = G.random(G1)
    a = secrets.randbits(int(p).bit_length())
    while int(a) >= int(p) or int(a) < 2**128 :
        a = secrets.randbits(int(p).bit_length())
    return G, p, g, a

def calculate_gi(g, a, b, p):
    gi = []
    gi.append(dict({"id": "0", "element": g}))
    exponent = int(a)
    for i in range(1, 2*b+1):
        gi.append(dict({"id": str(i), "element": g ** exponent}))
        exponent = (exponent * a) % int(p)
    return gi

def calculate_s(g, p):
    gamma = secrets.randbits(int(p).bit_length())
    while int(gamma) >= int(p) or int(gamma) < 2**128 :
        gamma = secrets.randbits(int(p).bit_length())

    s = g ** gamma
    return gamma, s

def calculate_private_key(gi, gamma, b):
    di = [None]
    for i in range(1, b+1):
        di.append(gi[i]["element"] ** gamma)
    return di

def calculate_c1(b, gi, s, S, t):
    tmp = s
    for j in S:
        tmp = tmp * gi[b+1-j]["element"]
    return tmp ** t

def calculate_t_K_Hdr(G, g, p, b, gi, s, S):
    t = secrets.randbits(int(p).bit_length())
    while int(t) >= int(p) or int(t) < 2**128 :
        t = secrets.randbits(int(p).bit_length())
   
    K = G.pair_prod(gi[b+1]["element"], g) 
    K2 = G.pair_prod(gi[b]["element"], gi[1]["element"])
    assert K == K2, "pairing property" 

    c0 = g ** t
    c1 = calculate_c1(b, gi, s, S, t)
    Hdr = (c0, c1)

    return t, K, Hdr


def main():
    b = 20
    S = [1, 2, 3, 4, 5, 6]
    G, p, g, a = init()
    gi = calculate_gi(g, a, b, p)       # access g_k by gi[k]
    gamma, s = calculate_s(g, p)
    di = calculate_private_key(gi, gamma, b)   # access d_k by di[k] 
    t, K, Hdr = calculate_t_K_Hdr(G, g, p, b, gi, s, S)

    ''' todo: Change the following print into write in file '''

    # public
    print("G = ", G)
    print("p = ", p)
    print("g = ", g)
    print("gi = ", gi) # Important : remember to remove gi[b+1]
    print("S = ", S)
    print("b = ", b)
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


if __name__ == '__main__':
    main()
