from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import hmac
import hashlib
import binascii
import time
from .prime import gen_large_prime
from .aesCipher import AESCipher
from .json_function import read_json

order_of_G = PairingGroup('SS512').order()

# Reference: https://stackoverflow.com/questions/39767297/how-to-use-sha256-hmac-in-python-code
'''
param:
    key: str
    m: str
    p: int
    This function will map (key, m) to a integer in Zp
'''
def prf1(key, m, p):
    mod_length = p.bit_length()
    sha256 = hashlib.sha256()
    
    H = ""
    #byte_key = binascii.unhexlify(key)
    byte_key = key.encode()
    m = m.encode()
    while len(H) <= mod_length:
        H += hmac.new(byte_key, m, hashlib.sha256).hexdigest()
        sha256.update(byte_key)
        byte_key = sha256.digest()
        #print(byte_key)
    
    return int(H, 16) % p

'''
param:
    key: str
    m: str
   
'''
def prf2(key, m):
    byte_key = key.encode()
    encoded_m = m.encode()
    H = hmac.new(byte_key, encoded_m, hashlib.sha256).hexdigest()
    return H
    
def prf3(key, x):
    h = prf1(key, key, order_of_G)
    return (x * h) % order_of_G

def main():
    key = "abcde"
    data = "applebanana"
    '''
    p = gen_large_prime(1024)
    h1 = prf1(key, data, p)
    h2 = prf2(key, data)
    
    print(h1)
    print(h2)
    '''
    K = 21
    k1 = "wvnjeronvjeorvneorve"
    k3 = "vrewhovbejrbviheorbvjwqbvhieofbuvew"
    keyword_list = read_json('keyword_list.json')
    keyword_num = len(keyword_list)
    print(keyword_num)
    #print(keyword_list)
    start = time.time()
    for i in range(keyword_num):
        for j in range(i, keyword_num):
            w1 = keyword_list[i]
            w2 = keyword_list[j]
            print(w1, w2, w1+w2)
            token = prf1(k1, w1+w2, order_of_G)
            r = prf3(k3, token)
            print("token", token)
            print("r", r)
            print((K**((token * r) % 37)) % order_of_G)
    end = time.time()
    print(end-start)
    
        

if __name__ == "__main__":
    main()


