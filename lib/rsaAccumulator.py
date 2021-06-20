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
    if n == None and g == None:
        p, q = gen_two_large_prime(prime_size)
        n = q * p
        g = secrets.randbelow(n)
    
    return n, g

def cipher_to_prime(cipher):
    prime, nonce= _hash_to_prime(_hash(k=cipher['id'], m=_hash(m=cipher['ciphertext'])))
    return prime

def cipher_to_prime_list(cipher_list):
    #print(cipher_list)
    rev = []
    for cipher in cipher_list:
        prime, nonce= _hash_to_prime(_hash(k=cipher['id'], m=_hash(m=cipher['ciphertext'])))
        rev.append(prime)
    return rev

def accumulate(primeList, N):
    exp = 1
    for prime in primeList:
        exp *= prime
    accE = pow(v, exp, N)
    return accE 

def verify(piJ, j, accE, N):
    if pow(piJ, j, N) == accE:
        return True
    return False

def _hash_to_length(x, bit_length):
    block_size = hashlib.sha256().block_size

    H = BitArray('')
    cnt = 0
    while cnt * block_size * 4 < bit_length:
        tmp = hashlib.sha256(str(x + cnt).encode()).digest()
        H += BitArray(bytes=tmp)
        cnt += 1
    
    return int(H.bin[:bit_length], 2)

def _hash_to_prime(x, bit_length=3*LAMBDA, nonce=0):
    while True:    
        num = _hash_to_length(x+nonce, bit_length)
        if is_prime(num) == True:
            return num, nonce
        nonce += 1
    return hashlib.md5(m.encode('utf-8')).hexdigest()

def _hash(label=None, k=None, m=None, bit_length=LAMBDA):
    m_to_hash = ""
    m_to_hash += str(label) if label != None else ""
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
    data=read_json("./Document.json")
    #print(data)
    cipher = encryptContent(data)
    n, g = setup()
    cipher_prime_list = cipher_to_prime_list(cipher)
    #print(cipher_prime_list)

    Ac = accumulate(cipher_prime_list, n)
    print(Ac)
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
    #_test_hash()
    _test_cipher()

if __name__ == '__main__':
    main()
