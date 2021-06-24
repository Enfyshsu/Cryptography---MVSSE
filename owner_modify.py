from lib.json_function import read_json, write_json
from lib.encrypt_document import decryptContent, encryptContent
from lib.rsaAccumulator import cipher_to_prime, accumulate, cipher_to_prime_list
from lib.aesCipher import AESCipher

DOCUMENT_PATH = "./Document.json"
KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"
OWNER_INFO_PATH = "./owner_info.json"
ACCU_PATH = "Accu.json"

# Reference: https://www.techiedelight.com/extended-euclidean-algorithm-implementation/
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

def modify(document_id, new_content):
    print("doc is ", new_content)
    print(len(new_content))
    #data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)
    owner_info = read_json(OWNER_INFO_PATH)
    cipher = read_json(CIPHERTEXT_PATH, is_binary=True)
    accu = read_json(ACCU_PATH)

    ke = owner_info['ke']
    n = owner_info['N']
    q = owner_info['q']
    p = owner_info['p']
    A_c = accu["A_c"]
    A_i = accu["A_i"]
    new_keywords = []

    # Find new keyword list
    for w in keyword:
        if w in new_content:
            new_keywords.append(w)

    # Build new document
    new_doc = {}
    new_doc["id"] = str(document_id)
    new_doc["content"] = new_content
    new_doc['keywords'] = new_keywords
    
    inverse_X = None
    phi_n = (q-1) * (p-1)
    for i in range(len(cipher)):
        if cipher[i]["id"] == document_id :
            X = cipher_to_prime(cipher[i]) 
            gcd, inverse_X, _ = egcd(X, phi_n)
            assert gcd == 1
            inverse_X %= phi_n
            #print((X * inverse_X) % n)
    
            AES = AESCipher(ke)
            new_cipher = {}
            new_cipher["id"] = new_doc["id"]
            new_cipher['ciphertext'] = AES.encrypt(new_doc['content'])
            _X = cipher_to_prime(new_cipher)
            d = _X * inverse_X
            _A_c = accumulate([d], A_c, n)

            # Update Cipher and A_c
            cipher[i]['ciphertext'] = new_cipher['ciphertext']
            accu['A_c'] = _A_c
            
    '''
    for d in data:
        if d["id"] == document_id:
            d["content"] = new_content
            d["keywords"] = new_keywords
            break
    write_json(DOCUMENT_PATH, data, is_G=True)
    '''

    #cipher = encryptContent(data, ke)
    write_json(CIPHERTEXT_PATH, cipher, is_binary=True)
    write_json(ACCU_PATH, accu)


def main():
    document_id = input("Please enter the document id you want to modify: ")
    new_content = input("Please enter the new content of document %s: " % document_id)

    modify(document_id, new_content)
    '''
    cipher = read_json(CIPHERTEXT_PATH, is_binary=True)
    A_C = read_json("./Accu.json")["A_c"]
    prime_list, nonce = cipher_to_prime_list(cipher)
    public_info = read_json("./public_info.json", is_G=True)
    _A_C = accumulate(prime_list, public_info['v'], public_info['N'])
    print(_A_C)
    print(A_C)
    '''

if __name__ == "__main__":
    main()
