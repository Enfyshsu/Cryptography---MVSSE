from .prime import gen_large_prime, gen_two_large_prime

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

def main():
    p, q = gen_two_large_prime(1024)
    N = p*q
    accE = accumulate([2,5,7], N)
    print(accE)
    piJ = accumulate([2,5], N)
    print(piJ)
    ver = verify(piJ, 7, accE, N)
    print(ver)

if __name__ == '__main__':
    main()
