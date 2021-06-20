from lib.json_function import read_json, write_json
from lib.encrypt_document import read_masterkey, encryptContent, gen_key_pair, decryptContent
from lib.setup_1 import init, calculate_gi, calculate_s, calculate_private_key, calculate_t_K_Hdr
from lib import rsaAccumulator

DOCUMENT_PATH = "./Document.json"
CIPHERTEXT_PATH = "./Cipher.json"
MASTER_KEY_PATH = "./masterkey"

b = 20 # Maxinum number of users
S = [1, 2, 3, 4, 5, 6] # Number of current users

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

    to_public["N"] = n
    to_public["v"] = v
    to_public["p"] = p
    to_public["gi"] = gi
    '''
    for k in to_public.keys():
        print(to_public[k])
    '''
    write_json("./public.json", to_public, is_G=True)

def main():
    owner_setup()
    '''
    data = read_json(DOCUMENT_PATH)
    #print(data)
    k1, k2, k3, k4 = gen_key_pair() 

    cipher_list = encryptContent(data)
    write_json(CIPHERTEXT_PATH, cipher_list, is_binary=True)

    cipher_list = None
    cipher_list = read_json(CIPHERTEXT_PATH, is_binary=True)
    
    decrypt_data = decryptContent(cipher_list)
    for d in decrypt_data:
        if d['content'] == data[int(d['id'])]['content']:
            print("true")
        else:
            print("Flase")
    '''

if __name__ == "__main__":
    main()           
