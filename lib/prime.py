import secrets
from math import sqrt
from random import randrange

low_prime_list = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293, 307, 311, 313, 317, 331, 337, 347, 349, 353, 359, 367, 373, 379, 383, 389, 397, 401, 409, 419, 421, 431, 433, 439, 443, 449, 457, 461, 463, 467, 479, 487, 491, 499, 503, 509, 521, 523, 541, 547, 557, 563, 569, 571, 577, 587, 593, 599, 601, 607, 613, 617, 619, 631, 641, 643, 647, 653, 659, 661, 673, 677, 683, 691, 701, 709, 719, 727, 733, 739, 743, 751, 757, 761, 769, 773, 787, 797, 809, 811, 821, 823, 827, 829, 839, 853, 857, 859, 863, 877, 881, 883, 887, 907, 911, 919, 929, 937, 941, 947, 953, 967, 971, 977, 983, 991, 997]

def miller_rabin(n):

    # Find s and r such that n - 1 = r * 2^s
    s = 0
    r = n - 1
    while r & 1 == 0:
        # keep halving r until it is odd, and use s to count how many times we halve s
        r = r // 2
        s += 1
    
    # Do k times
    k = 5
    for _ in range(k): 
        a = randrange(2, n - 1)
        x = pow(a, r, n)
        if x != 1 and x != n - 1:
            i = 1
            while i < s and x != n - 1:
                x = pow(x, 2, n)
                if x == 1:
                    return False
                i += 1    
            if x != n - 1:
                return False

    return True

def is_prime(n):
    if n in low_prime_list:
        return True
    
    if n < 2 or n % 2 == 0:
        return False

    for prime in low_prime_list:
        if n % prime == 0:
            return False

    return miller_rabin(n)

def gen_large_prime(bits):
    #cnt = 0
    while True:
        num = secrets.randbelow(pow(2, bits))
        #cnt += 1
        if is_prime(num):
            #print("count is ", cnt)
            return num

def gen_two_large_prime(bits):
    while True: 
        p = gen_large_prime(bits)
        while True:
            q = gen_large_prime(bits)
            while q != p:
                return p, q

def gen_two_safe_prime(bits):
    while True: 
        p = gen_large_prime(bits)
        if is_prime((p-1)//2):
            while True:
                q = gen_large_prime(bits)
                if is_prime((q-1)//2):
                    while q != p:
                        return p, q

def main():
    bits = int(input())
    # p, q = gen_two_safe_prime(bits)
    # print(p)
    # print(q)
    

if __name__ == '__main__':
    main()
