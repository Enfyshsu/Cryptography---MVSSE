import hmac
import hashlib
import binascii
from .prime import gen_large_prime

# Reference: https://stackoverflow.com/questions/39767297/how-to-use-sha256-hmac-in-python-code
def prf1(key, m, p):
    mod_length = p.bit_length()
    sha256 = hashlib.sha256()
    
    H = ""
    byte_key = binascii.unhexlify(key)
    m = m.encode()
    while len(H) <= mod_length:
        H += hmac.new(byte_key, m, hashlib.sha256).hexdigest()
        sha256.update(byte_key)
        byte_key = sha256.digest()
        #print(byte_key)
    
    return int(H, 16) % p

def main():
    p = gen_large_prime(1024)
    prf1("E49756B4C8FAB4E48222A3E7F3B97CC3", "This is test", p)

if __name__ == "__main__":
    main()


