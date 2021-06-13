import hashlib
from .prime import gen_large_prime, gen_two_large_prime
from .generator import generators

'''
p, q are 512 bits safe prime
N = p*q
v = 
'''
p = 3897905084791485435679018241725955863839264880076276641438166361665067393589461636507194799807972292904524315477069113706553182713061050518933782432177067
q = 606223194186276537666306594388855936281143220688229008170872654528545826992040969384414188105471643244737173125502614496393070063279978450512383976343603

v = 2

def accumulate(primeList, N):
    exp = 1
    for prime in primeList:
        exp *= prime
    accE = v ** exp % N
    return accE 

def verify(piJ, j, accE, N):
    if piJ ** j % N == accE:
        return True
    return False

def hashFn(m):
    # lambda = 128
    return hashlib.md5(m.encode('utf-8')).hexdigest()

def main():
    # p, q = gen_two_large_prime(1024)
    # N = p*q
    # accE = accumulate([2,5,7], N)
    # print(accE)
    # piJ = accumulate([2,5], N)
    # print(piJ)
    # ver = verify(piJ, 7, accE, N)
    # print(ver)
    # m = hashFn("haha")
    # print(len(m), m)
    print(generators(p*q))

if __name__ == '__main__':
    main()
