from lib.json_function import read_json, write_json
from lib.encrypt_document import decryptContent, encryptContent
from lib.rsaAccumulator import cipher_to_prime, _hash, _hash_to_prime, accumulate #, accumulate, cipher_to_prime_list
from lib.aesCipher import AESCipher
from lib.prf import prf2
from bitstring import BitArray

KEYWORD_PATH = "./owner/keyword_list.json"
CIPHERTEXT_PATH = "./server/Cipher.json"
INDEX_PATH = "./server/Index.json"
OWNER_INFO_PATH = "./owner/owner_info.json"
ACCU_PATH = "./Accu.json"
NONCE_PATH = "./Accu_nonce"
PUBLIC_INFO_PATH = "./public_info.json"

def add(new_content):
    #print(new_content)
    #print(len(new_content))
    #data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)
    owner_info = read_json(OWNER_INFO_PATH)
    cipher = read_json(CIPHERTEXT_PATH, is_binary=True)
    Index = read_json(INDEX_PATH, is_G=True)
    accu = read_json(ACCU_PATH)
    nonce = read_json(NONCE_PATH)
    public_info = read_json(PUBLIC_INFO_PATH, is_G=True)

    ke = owner_info['ke']
    n = owner_info['N']
    k2 = owner_info['k2'] # need modify
    A_c = accu["A_c"]
    A_i = accu["A_i"]
    A_c_nonce = nonce['A_c_nonce']
    A_i_nonce = nonce["A_i_nonce"]
    new_keywords = []

    # Find new keyword list
    for w in keyword:
        if w in new_content:
            new_keywords.append(w)

    #print(new_keywords)

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

    # Compute Ai
    cnt = 0
    prime_list = []
    doc_length = len(cipher)
    document_id = doc_length - 1
    for i in range(len(keyword)):
        for j in range(i, len(keyword)):
            wi = keyword[i]
            wj = keyword[j]
            l = str(wi) + str(wj)
            
            pad_id = BitArray(hex=prf2(k2, l)).bin[document_id]
            index_id = 1 if wi in new_keywords and wj in new_keywords else 0
            index_bar_id = int(pad_id) ^ index_id
            Index[cnt]["index_bar"] += str(index_bar_id)

            # Record prime for Ai
            label = Index[cnt]['label']
            nonce_id = cnt * doc_length + document_id
            prime, new_nonce = _hash_to_prime(_hash(label=label, k=document_id, m=index_bar_id))
            A_i_nonce.insert(nonce_id, new_nonce)
            prime_list.append(prime)
            cnt += 1
    
    #print(prime_list)
    accu["A_i"] = accumulate(prime_list, A_i, n)

    # Compute A_c
    prime, new_nonce = _hash_to_prime(_hash(k=new_cipher['id'], m=_hash(m=new_cipher['ciphertext'])))
    accu["A_c"] = pow(A_c, prime, n)
    A_c_nonce.append(new_nonce)
    
    # Update nonce
    nonce['A_i_nonce'] = A_i_nonce
    nonce['A_c_nonce'] = A_c_nonce
    
    # Update doc length
    public_info['doc_length'] += 1

    write_json(CIPHERTEXT_PATH, cipher, is_binary=True)
    write_json(ACCU_PATH, accu)
    write_json(INDEX_PATH, Index, is_G=True)
    write_json(NONCE_PATH, nonce)
    write_json(PUBLIC_INFO_PATH, public_info, is_G=True)

def main():
    new_content = input("Please enter the content of new document: ").strip()

    add(new_content)

    # A_C = read_json("./Accu.json")["A_c"]
    # prime_list, nonce = cipher_to_prime_list(cipher)
    # public_info = read_json("./public_info.json", is_G=True)
    # _A_C = accumulate(prime_list, public_info['v'], public_info['N'])
    # print(_A_C)
    # print(A_C)
    

if __name__ == "__main__":
    main()
