from Crypto.Cipher import AES
from lib.json_function import read_json
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

def keywords_in_document(w1, w2, documents):
    contain_list = []
    for doc in documents:
        if w1 in doc['keywords'] and w2 in doc['keywords']:
            contain_list.append(doc['id'])
    return contain_list

def main():
    documents = read_json("./Document.json")
    w1 = input()
    w2 = input()
    contain_list = keywords_in_document(w1, w2, documents)
    print(contain_list)
    # documentList = ["apple banana", "cat cake", "dog"]
    # encryptList = encryptContent(documentList)
    # print(encryptList)   
    

if __name__ == '__main__':
    main()
