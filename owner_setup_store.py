from lib.json_function import read_json, write_json
from lib.encrypt_document import read_masterkey, encryptContent, gen_key_pair, decryptContent
from lib.setup_1 import init, calculate_gi, calculate_s, calculate_private_key, calculate_t_K_Hdr
from lib import rsaAccumulator
from lib.prf import prf1, prf2, prf3

from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

from bitstring import BitArray

DOCUMENT_PATH = "./Document.json"
KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"
MASTER_KEY_PATH = "./masterkey"

b = 20 # Maxinum number of users
S = [1, 2, 3, 4, 5, 6] # Number of current users

def build_Index(doc_list, keyword_list, K, k1, k2, k3):
    Index = []
    keyword_length = len(keyword_list)
    doc_length = len(doc_list)
    cnt = 0
    
    keyword_index = []
    for w in keyword_list:
        index = 0
        for d in doc_list:
            index *= 2
            if w in d["keywords"]:
                index += 1
        keyword_index.append(BitArray(uint=index, length=doc_length))
    
    for i in range(keyword_length):
        for j in range(i, keyword_length):
            wi = keyword_list[i]
            wj = keyword_list[j]
            l = str(wi) + str(wj)

            index = keyword_index[i] & keyword_index[j]
            
            # Calculate index_bar
            token_l = prf1(k1, l)
            r_l = prf3(k3, token_l)
            pad = BitArray(hex=prf2(k2, l))[:doc_length]
            index_bar = index ^ pad
            
            # Calculate label = K^(token*r)
            label_l = K ** (token_l * r_l)

            # Append to Index
            Index.append(dict({
                                "id": cnt, 
                                "label": label_l, 
                                "index_bar": str(index_bar.bin)
                                }))
            cnt += 1

    write_json("Index.json", Index, is_G=True)            

def owner_setup():

    # Setup bilinear group and broadcast encryption
    G, p, g, a = init()
    gi = calculate_gi(g, a, b, p)  
    gamma, s = calculate_s(g, p)
    di = calculate_private_key(gi, gamma, b) 
    t, K, Hdr = calculate_t_K_Hdr(G, g, p, b, gi, s, S)
  
    # Set up RSA accumulator
    n, v = rsaAccumulator.setup()

    to_public = {}  # Information that will be public
    to_user = []    # Information that will to sent to users
    to_server = {}  # Information that will be sent to server

    # Key generation
    k1, k2, k3, k4, ke = gen_key_pair() 

    # Public Information
    to_public["N"] = n
    to_public["v"] = v
    to_public["p"] = p
    if int(gi[b+1]["id"]) == b + 1: 
        gi[b + 1]["element"] = None # Remove g_b+1
    to_public["gi"] = gi
    to_public["s"] = s

    # Users' information
    to_user.append(None)
    for u in S:
        user_info = {}
        user_info["id"] = str(u)
        user_info["k1"] = k1
        user_info["k2"] = k2
        user_info["ke"] = ke
        user_info["di"] = di[u]

        to_user.append(user_info)        
    
    # Server's information
    to_server["k3"] = k3
    to_server["Hdr"] = Hdr

    # Write to file system
    write_json("./public_info.json", to_public, is_G=True)
    write_json("./server_info.json", to_server, is_G=True)
    for u in S:
        write_json("./user%s_info.json" % (to_user[u]["id"]), to_user[u], is_G=True)

    return K, k1, k2, k3, ke, v, n

def owner_store(K, k1, k2, k3, ke, v, n):
    # Read the documents and keywords list
    doc_list = read_json(DOCUMENT_PATH)
    keyword_list = read_json(KEYWORD_PATH)

    # Encrypt the documents and write to file system
    cipher_list = encryptContent(doc_list, ke)
    write_json(CIPHERTEXT_PATH, cipher_list, is_binary=True)

    # Build the Index matrix
    build_Index(doc_list, keyword_list, K, k1, k2, k3)

    # Compute Accumulator value (A_c, A_i)
    A_c, A_i, A_c_nonce, A_i_nonce = rsaAccumulator.compute_acc(doc_list, cipher_list, v, n)
    print("AC is ", A_c)
    print("AI is ", A_i)
    #cipher_list = None
    #cipher_list = read_json(CIPHERTEXT_PATH, is_binary=True)
    
    #decrypt_data = decryptContent(cipher_list, ke)

    Accu = dict({"A_c": A_c, "A_i": A_i})
    Accu_path = "Accu.json"
    write_json(Accu_path, Accu)
    
    nonce_path = "Accu_nonce"
    Accu_nonce = dict({"A_c_nonce": A_c_nonce, "A_i_nonce": A_i_nonce})
    write_json(nonce_path, Accu_nonce)

    '''
    for d in decrypt_data:
        if d['content'] == data[int(d['id'])]['content']:
            print("true")
        else:
            print("Flase")
    '''

def main():
    K, k1, k2, k3, ke, v, n = owner_setup()
    owner_store(K, k1, k2, k3, ke, v, n)

if __name__ == "__main__":
    main()           
