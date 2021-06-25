from lib.json_function import read_json, write_json
from lib.encrypt_document import decryptContent, encryptContent
from lib.rsaAccumulator import cipher_to_prime #, accumulate, cipher_to_prime_list
from lib.aesCipher import AESCipher
from lib.prf import prf2
from bitstring import BitArray

KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"
INDEX_PATH = "./Index.json"
OWNER_INFO_PATH = "./owner_info.json"
ACCU_PATH = "Accu.json"

def add(new_content):
    print(new_content)
    print(len(new_content))
    #data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)
    owner_info = read_json(OWNER_INFO_PATH)
    cipher = read_json(CIPHERTEXT_PATH, is_binary=True)
    index = read_json(INDEX_PATH)
    accu = read_json(ACCU_PATH)

    ke = owner_info['ke']
    n = owner_info['N']
    k2 = "766e55532514b1ab2ede14e47bb92b5f" # need modify
    A_c = accu["A_c"]
    A_i = accu["A_i"]
    new_keywords = []

    # Find new keyword list
    for w in keyword:
        if w in new_content:
            new_keywords.append(w)

    print(new_keywords)

    # Build new document
    new_doc = {}
    new_doc["id"] = str(len(cipher))
    new_doc["content"] = new_content
    new_doc['keywords'] = new_keywords

    AES = AESCipher(ke)
    new_cipher = {}
    new_cipher["id"] = new_doc["id"]
    new_cipher['ciphertext'] = AES.encrypt(new_doc['content'])
    cipher.append(new_cipher)

    for i in range(len(keyword)):
        for j in range(i, len(keyword)):
            wi = keyword[i]
            wj = keyword[j]
            l = str(wi) + str(wj)
            new_pad = BitArray(hex=prf2(k2, l))[:len(cipher)]
            if (wi in new_doc['keywords'] and wj in new_doc['keywords']) ^ new_pad[len(cipher)-1]:
                index[i+j]["index_bar"] += '1'
            else:
                index[i+j]["index_bar"] += '0'

    accu["A_c"] = pow(accu["A_c"], cipher_to_prime(new_cipher), n)

    # write_json(CIPHERTEXT_PATH, cipher, is_binary=True)
    # write_json(ACCU_PATH, accu)
    # write_json(INDEX_PATH, index)


def main():
    new_content = input("Please enter the content of new document: ")

    add(new_content)

    # A_C = read_json("./Accu.json")["A_c"]
    # prime_list, nonce = cipher_to_prime_list(cipher)
    # public_info = read_json("./public_info.json", is_G=True)
    # _A_C = accumulate(prime_list, public_info['v'], public_info['N'])
    # print(_A_C)
    # print(A_C)
    

if __name__ == "__main__":
    main()
