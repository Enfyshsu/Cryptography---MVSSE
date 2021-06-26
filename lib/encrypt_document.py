from .aesCipher import AESCipher
from .json_function import read_json
import hashlib
# from Crypto.Hash import MD5

KEY_PATH = "./owner/masterkey"

def read_masterkey(key_path=KEY_PATH):
    master_key = open(key_path).read().strip()
    return master_key

def gen_key_pair():
    master_key = read_masterkey()
    h = hashlib.sha256(master_key.encode()).hexdigest()
    h += hashlib.sha256(h.encode()).hexdigest()
    h += hashlib.sha256(h.encode()).hexdigest()
    length = len(h)
    #print(h)
    #print(length)
    sep = length // 6
    return h[:sep], h[sep:2*sep], h[2*sep:3*sep], h[3*sep:4*sep], h[4*sep:]

def encryptContent(documentList, k):
    master_key = k
    AES = AESCipher(master_key)
    
    encryptList = []
    for doc in documentList:
        cipher = {}
        cipher["id"] = doc["id"]
        cipher['ciphertext'] = AES.encrypt(doc['content'])
        encryptList.append(cipher)

    return encryptList
    
def decryptContent(cipherList, k):
    master_key = k
    AES = AESCipher(master_key)

    decryptList = []
    for c in cipherList:
        d = {}
        d["id"] = c["id"]
        d["content"] = AES.decrypt(c['ciphertext'])
        decryptList.append(d)

    return decryptList    

def main():
    
    data = read_json("./Document.json")
    cipher = encryptContent(data)
    data_decrypted = decryptContent(cipher)

    for d in data_decrypted:
        if d['content'] == data[int(d['id'])]["content"]:
            print("ture")
        else:
            print("flase")
    '''
    master_key = read_masterkey()
    AES = AESCipher(master_key)
    for c in encryptList:
        print(AES.decrypt(c['ciphertext']))
    #read_masterkey()
    '''

if __name__ == '__main__':
    main()
