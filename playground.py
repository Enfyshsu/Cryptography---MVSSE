from Crypto.Cipher import AES
# from Crypto.Hash import MD5

key = b'Q\xbd/\xddr c=\x12\xb9|\xd7%y\xe9\xbb\xdd6Q\xd5\x8a\xfc\x1f\x9d<s\x97r"\x178L'

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
    # documentList = ["apple banana", "cat cake", "dog"]
    # encryptList = encryptContent(documentList)
    # print(encryptList)   
    

if __name__ == '__main__':
    main()