from Crypto.Cipher import AES
# from Crypto.Hash import MD5

KEY_PATH = "./masterkey"

def read_masterkey():
    master_key = open(KEY_PATH).read().strip()
    return master_key


def encryptContent(documentList):
    encryptList = []
    for document in documentList:
        pad = lambda s: s + (16 - len(s)%16) * chr(16 - len(s)%16)
        document = pad(document)
        cipher = AES.new(key, AES.MODE_ECB)
        cipheredDoc = cipher.encrypt(document)
        encryptList.append(cipheredDoc)
    return encryptList

def main():
    #documentList = ["apple banana", "cat cake", "dog"]
    #encryptList = encryptContent(documentList)
    #print(encryptList)   
    read_masterkey()
    

if __name__ == '__main__':
    main()
