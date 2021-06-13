import hashlib
from .prime import gen_large_prime, gen_two_large_prime
from .generator import generators
import time
import random


# Reference: https://github.com/oleiba/RSA-accumulator
'''
p, q are 512 bits safe prime
N = p*q
v = 
'''
SAFE_PRIME_P = 3897905084791485435679018241725955863839264880076276641438166361665067393589461636507194799807972292904524315477069113706553182713061050518933782432177067
SAFE_PRIME_Q = 606223194186276537666306594388855936281143220688229008170872654528545826992040969384414188105471643244737173125502614496393070063279978450512383976343603

v = 2

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

def hashFn(m):
    # lambda = 128
    return hashlib.md5(m.encode('utf-8')).hexdigest()

def main():
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
    

if __name__ == '__main__':
    main()
