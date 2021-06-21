import hashlib
import hmac
from bitstring import BitArray
from .prime import gen_large_prime, gen_two_large_prime, is_prime
from .generator import generators
from .json_function import read_json
from .encrypt_document import encryptContent
import time
import random
import secrets

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
# test
# Reference: https://github.com/oleiba/RSA-accumulator

'''
p, q are 512 bits safe prime
N = p*q
v = 
'''
SAFE_PRIME_P = 3897905084791485435679018241725955863839264880076276641438166361665067393589461636507194799807972292904524315477069113706553182713061050518933782432177067
SAFE_PRIME_Q = 606223194186276537666306594388855936281143220688229008170872654528545826992040969384414188105471643244737173125502614496393070063279978450512383976343603
LAMBDA = 128
RSA_PRIME_SIZE = 1024

v = 2


def setup(prime_size=RSA_PRIME_SIZE, n=None, g=None):
    # Setup for RSA accumulator.
    # For owner purpose, it is necessary to randomly generate two primes, q and p, to compute n = q * p. Next generate a 
    # g under Zn
    # For client purpose, since both n and g are public in our scheme, there is no need to re-generate n and g.

    if n == None and g == None:
        p, q = gen_two_large_prime(prime_size)
        n = q * p
        g = secrets.randbelow(n)
    
    return n, g

def cipher_to_prime(cipher):
    # Hash (i, C_i) to a prime number, for example (3, "This is cipher") -> 31
    
    prime, nonce= _hash_to_prime(_hash(k=cipher['id'], m=_hash(m=cipher['ciphertext'])))
    return prime

def cipher_to_prime_list(cipher_list):
    # Hash a list of (i, C_i) to a list of prime number
    
    #print(cipher_list)
    rev = []
    for cipher in cipher_list:
        prime, nonce= _hash_to_prime(_hash(k=cipher['id'], m=_hash(m=cipher['ciphertext'])))
        rev.append(prime)
    return rev

def label_index_to_prime_list(l_i_list, n):
    # Hash a label_index to a list of prime number

    rev = []
    for l in l_i_list:
        label = l['label']
        for k in range(0, n):
            index_bar = l['index_bar'][k]
            prime, nonce= _hash_to_prime(_hash(label=label, k=n, m=index_bar))
            rev.append(prime)
    return rev

def accumulate(primeList, N):
    # Given a list of prime number, calculator its accumulating value module N
    
    acc = 1
    # exp = 1
    for prime in primeList:
        acc *= pow(v, prime, N)
        # exp *= prime
    # acc = pow(v, exp, N)
    return acc

def verify(piJ, j, accE, N):
    # To verify if j belongs to set E
    
    if pow(piJ, j, N) == accE:
        return True
    return False

def _hash_to_length(x, bit_length):
    # Hash integer x into another integer of length bit_length
    # Note that there might be some 0s in the head of return value, 
    # so its bit length will be a little smaller than bit_length

    block_size = hashlib.sha256().block_size

    H = BitArray('')
    cnt = 0
    while cnt * block_size * 4 < bit_length:
        tmp = hashlib.sha256(str(x + cnt).encode()).digest()
        H += BitArray(bytes=tmp)
        cnt += 1
    
    return int(H.bin[:bit_length], 2)

def _hash_to_prime(x, bit_length=3*LAMBDA, nonce=0):
    # Hash integer x into a prime number of length 3 * LAMBDA, where LAMBDA is a secure parameter
    # Note that there might be some 0s in the head of return value, 
    # so its bit length will be a little smaller than 3 * LAMBDA
    
    while True:
        num = _hash_to_length(x+nonce, bit_length)
        if is_prime(num) == True:
            return num, nonce
        nonce += 1
    return hashlib.md5(m.encode('utf-8')).hexdigest()

def _hash(label=None, k=None, m=None, bit_length=LAMBDA):
    # Hash function for our RSA accumulator, LAMBDA is a secure parameter
    # To calculate the value of AC, use _hash(k=..., m=...) and _hash(m=...)
    # To calculate the value of AI, use _hash(label=..., k=..., m=...)
    
    G = PairingGroup('SS512')
    g = G.random(G1)

    m_to_hash = ""
    if type(label) == str:
        m_to_hash += str(label)
    elif type(label) ==  type(g):
        m_to_hash += G.serialize(label).decode()
    m_to_hash += str(k) if k != None else ""
    m_to_hash += str(m) if m != None else ""    
    #print("m to hash ", m_to_hash) 
    if m_to_hash == '':
        return None
    
    h = BitArray(hex=hashlib.sha256(m_to_hash.encode()).hexdigest())
    #print(h)
    if len(h.bin) > bit_length:
        h = h.bin[len(h.bin) - bit_length:]
        #print(h)
        return int(h, 2)
    
    return int(h.bin, 2)

'''
Below are testing functions
'''

def _test_hash():
    n = 77433679007597074886484182587337503627048155142748346917153456826556117128
    h, nonce = _hash_to_prime(x=_hash(m="xu3rmp4m3", bit_length=1024), bit_length=1024)
    print(h, nonce)
    h, nonce = _hash_to_prime(x=_hash(label="xu3", m="rmp4m3", bit_length=1024), bit_length=1024)
    print(h, nonce)
    h, nonce = _hash_to_prime(x=_hash(label="xu", k=3, m="rmp4m3", bit_length=1024), bit_length=1024)
    print(h, nonce)
    
    G = PairingGroup('SS512')
    g  = G.random(G1)
    g1 = g**2
    g2 = g + g
    print("g1 == g2 ", g1 == g2)
    h1 = _hash(label=g1, k=234, m=1)
    h2 = _hash(label=g2, k=234, m=1)
    print("h1 is ", h1)
    print("h2 is ", h2)
    print(h1 == h2)

def _test():
    p, q = gen_two_large_prime(128)
    N = p*q
    E = [random.randint(1, N) for i in range(10)]
    accE = accumulate(E, N)
    #accE = accumulate([2,5,7], N)
    #for i in E:
    #    print(i)
    print("accE is ", accE)
    piJ = accumulate([E[i] for i in range(10) if i != 7], N)
    print("piJ is ", piJ)
    ver = verify(piJ, E[7], accE, N)
    print(ver)

def _test_cipher():
    data = read_json("./Document.json")
    # cipher = encryptContent(data)
    n, g = setup()
    # cipher_prime_list = cipher_to_prime_list(cipher)
    label_index = read_json("./Index.json")
    label_index_prime_list = label_index_to_prime_list(label_index, len(data))
    # Ac = accumulate(cipher_prime_list, n)
    Ai = accumulate(label_index_prime_list, n)

    # print(Ac)
    print(Ai)
    l = len(cipher)
    for _ in range(5):
        Id = random.randint(1, l)
        print("prove id %d is in cipher list" % (Id))
        tmp_list = [cipher_prime_list[i] for i in range(l) if i != Id]
        pi = accumulate(tmp_list, n)
        print("pi is ", pi)
        id_prime = cipher_to_prime(cipher[Id])
        print("id prime is ", id_prime)
        print(verify(pi, id_prime, Ac, n))
        id_prime = cipher_to_prime({"id": str(Id), "ciphertext": "abcde"})
        print(verify(pi, id_prime, Ac, n))
        

def main():
    #_test()
    # _test_hash()
    _test_cipher()

if __name__ == '__main__':
    main()
