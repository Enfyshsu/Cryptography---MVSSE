from .aesCipher import AESCipher
# from Crypto.Hash import MD5

KEY_PATH = "./masterkey"

def read_masterkey():
    master_key = open(KEY_PATH).read().strip()
    return master_key


def encryptContent(documentList):
    master_key = read_masterkey()
    AES = AESCipher(master_key)
    
    encryptList = []
    for doc in documentList:
        cipher = {}
        cipher["id"] = doc["id"]
        cipher['ciphertext'] = AES.encrypt(doc['content'])
        encryptList.append(cipher)

    return encryptList
    
    
def main():
    documentList = [{"id": "0", "content": "apple banana"}, {"id": "1", "content": "cat cake"}, {"id": "2", "content": "dog"}]
    encryptList = encryptContent(documentList)
    print(encryptList)  

    master_key = read_masterkey()
    AES = AESCipher(master_key)
    for c in encryptList:
        print(AES.decrypt(c['ciphertext']))
    #read_masterkey()
    

if __name__ == '__main__':
    main()
