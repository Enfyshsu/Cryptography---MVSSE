from lib.json_function import read_json, write_json
from lib.encrypt_document import decryptContent, encryptContent
from lib.rsaAccumulator import cipher_to_prime, accumulate, cipher_to_prime_list, _hash_to_prime, _hash
from lib.aesCipher import AESCipher
from lib.prf import prf2
from bitstring import BitArray

KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"
OWNER_INFO_PATH = "./owner_info.json"
ACCU_PATH = "Accu.json"
INDEX_PATH = "./Index.json"

# Reference: https://www.techiedelight.com/extended-euclidean-algorithm-implementation/
def egcd(a, b):
    if a == 0:
        return b, 0, 1
    else:
        gcd, x, y = egcd(b % a, a)
        return gcd, y - (b // a) * x, x

def modify(document_id, new_content):
    #data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)
    owner_info = read_json(OWNER_INFO_PATH)
    cipher = read_json(CIPHERTEXT_PATH, is_binary=True)
    doc_length = len(cipher)
    accu = read_json(ACCU_PATH)
    Index = read_json(INDEX_PATH, is_G=True)

    ke = owner_info['ke']
    k2 = owner_info['k2']
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
    
    # Modify cipher and A_c
    inverse_X = None
    phi_n = (q-1) * (p-1)
    for i in range(len(cipher)):
        if int(cipher[i]["id"]) == int(document_id):
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
            
            break
            
    # Update A_i
    keyword_length = len(keyword)
    cnt = 0
    for i in range(keyword_length):
        for j in range(i, keyword_length):
            #print("cnt is ", cnt)
            wi = keyword[i]
            wj = keyword[j]
            l = str(wi) + str(wj)

            label = Index[cnt]['label']
            index_bar = Index[cnt]['index_bar']
            index_bar_id = int(index_bar[document_id])
            #print(label)
            #print(index_bar)
            #print(int(index_bar[document_id]))

            pad = BitArray(hex=prf2(k2, l))[:doc_length].bin
            pad_id = int(pad[document_id])
            if wi in new_keywords and wj in new_keywords:
                new_index_id = pad_id ^ 1
            else:
                new_index_id = pad_id ^ 0
            #print(new_index_id)
            if new_index_id != index_bar_id:
                Y, nonce= _hash_to_prime(_hash(label=label, k=document_id, m=index_bar_id))
                #print(cnt, document_id, index_bar_id)
                #print(Y)
                gcd, inverse_Y, _ = egcd(Y, phi_n)
                assert gcd == 1
                inverse_Y %= phi_n
                
                _Y, nonce= _hash_to_prime(_hash(label=label, k=document_id, m=new_index_id))
                #print(_Y)
                d = _Y * inverse_Y
                A_i = accumulate([d], A_i, n)
                index_bar = list(index_bar)
                index_bar[document_id] = str(new_index_id)
                index_bar = ''.join(index_bar)
                Index[cnt]['index_bar'] = index_bar

            #else:    
            #    print("Same")


            cnt += 1
           
    accu['A_i'] = A_i
    
    
    #cipher = encryptContent(data, ke)
    write_json(CIPHERTEXT_PATH, cipher, is_binary=True)
    write_json(ACCU_PATH, accu)
    write_json(INDEX_PATH, Index, is_G=True)


def main():
    document_id = input("Please enter the document id you want to modify: ")
    new_content = input("Please enter the new content of document %s: " % document_id)

    modify(int(document_id), new_content)
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
