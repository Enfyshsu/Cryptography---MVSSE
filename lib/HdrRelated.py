from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
from .setup_1 import *

def decrypt_Hdrbar(G, Hdrbar, I, gi, dI, b, S):
    C0, C1 = Hdrbar
    numerator = G.pair_prod(gi[I], C1)
    tmp = dI
    cnt = 1
    for j in S:
        if j != I:
            tmp = tmp * gi[b+1-j+I]
    denominator = G.pair_prod(tmp, C0)
    return numerator / denominator


if __name__ == '__main__':
    b = 20
    S = [1, 5, 6, 11, 14, 17]
    G, p, g, a = init()
    gi = calculate_gi(g, a, b, p)       # access g_k by gi[k]
    gamma, s = calculate_s(g, p)
    di = calculate_private_key(gi, gamma, b)   # access d_k by di[k] 
    t, K, Hdr = calculate_t_K_Hdr(G, g, p, b, gi, s, S)
   
    #server
    expo = 1234567 # rc * tokenc
    c0, c1 = Hdr
    Hdrbar = c0 ** expo, c1 ** expo

    #send Hdrbar to client

    # client decrypt with di[Index]
    Index = 6 # in S
    labelc =  decrypt_Hdrbar(G, Hdrbar, Index, gi, di[Index], b, S)
    
    assert labelc == K ** expo
    print("labelc = ", labelc)
    print("K ** (rc*tokenc) = ", K ** expo)





