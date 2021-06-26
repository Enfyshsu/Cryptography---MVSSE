from lib.json_function import read_json, write_json
from lib.rsaAccumulator import setup, cipher_to_prime_list, label_index_to_prime_list, accumulate, compute_pi
from bitstring import BitArray
import os

INDEX_PATH = "./server/Index.json"
CIPHER_PATH = "./server/Cipher.json"

def main():
    Index_path = INDEX_PATH
    Index = read_json(Index_path, is_G=True)
    
    Cipher_path = CIPHER_PATH
    Cipher = read_json(Cipher_path, is_binary=True)

    query_path = "user_query"
    query = read_json(query_path, is_G=True)

    nonce_path = "Accu_nonce"
    nonce = read_json(nonce_path)

    public_info_path = "public_info.json"
    public_info = read_json(public_info_path, is_G=True)

    N = public_info["N"]
    v = public_info['v']
    label = query['label']
    pad = query['pad']
    rev_doc_id = []
    index = BitArray(len(pad)).bin
    l_ID = -1
    for i in Index:
        if i["label"] == label:
            index_bar = i['index_bar']
            doc_length = len(index_bar)
            index = (BitArray(bin=index_bar) ^ BitArray(bin=pad[:doc_length])).bin
            l_ID = i["id"]
            for i in range(len(index)):
                if index[i] == '1':
                    rev_doc_id.append(i)
            break
    
    if l_ID == -1:
        print("Invalid label or no result")
        os.exit(0)

    # compute_pi(pi_list, Cipher)
    rev_doc = []
    print("Result contains docment id, ", rev_doc_id)
    for i in rev_doc_id:    
        rev_doc.append(Cipher[i])


    pi_c, pi_i = compute_pi(v, N, Cipher, Index, l_ID, index, nonce)

    result = dict({"rev_cipher": rev_doc, "pi_c": pi_c, "pi_i": pi_i})
    result_path = "result.json"
    write_json(result_path, result, is_binary=True)

if __name__ == "__main__":
    main()
