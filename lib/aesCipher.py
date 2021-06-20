import base64
import hashlib
from Crypto import Random
from Crypto.Cipher import AES

# Reference: https://stackoverflow.com/questions/12524994/encrypt-decrypt-using-pycrypto-aes-256

class AESCipher(object):

    def __init__(self, key): 
        self.bs = AES.block_size
        self.key = hashlib.sha256(key.encode()).digest()

    def encrypt(self, raw):
        raw = self._pad(raw)
        iv = Random.new().read(AES.block_size)
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return base64.b64encode(iv + cipher.encrypt(raw.encode()))
        #return iv + cipher.encrypt(raw.encode())

    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        iv = enc[:AES.block_size]
        cipher = AES.new(self.key, AES.MODE_CBC, iv)
        return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')
        #return self._unpad(cipher.decrypt(enc[AES.block_size:])).decode('utf-8')

    def _pad(self, s):
        return s + (self.bs - len(s.encode()) % self.bs) * chr(self.bs - len(s.encode()) % self.bs)

    @staticmethod
    def _unpad(s):
        return s[:-ord(s[len(s)-1:])]

def main():
    obj = AESCipher("abc")  
    enObj = obj.encrypt("This is \n data \n hahaha\n")
    print(enObj)
    print(len(enObj))
    deObj = obj.decrypt(enObj)
    print(deObj)
    print(len(deObj))
    

if __name__ == '__main__':
    main()
