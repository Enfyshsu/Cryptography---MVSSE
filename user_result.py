from lib.json_function import write_json, read_json
from lib.rsaAccumulator import cipher_to_prime_list, accumulate, cipher_to_prime, _hash, _hash_to_prime
from lib.encrypt_document import decryptContent
import sys, os

def main():
    if len (sys.argv) != 2 :
        print("Usage: python user_result <User ID>")
        sys.exit (1)
    Id = str(sys.argv[1])

    result_path = "result.json"
    try:
        result = read_json(result_path, is_binary=True)
    except:
        print("No result from server.")
        sys.exit(0)
    accu_path = "Accu.json"
    accu = read_json(accu_path)
    
    public_info_path = "public_info.json"
    public_info = read_json(public_info_path)

    query_path  = "user_query"
    query = read_json(query_path, is_G=True)
    
    USER_DIR = "users/user%s" % (Id)
    USER_INFO = "user%s_info.json" % (Id)
    user_info_path = os.path.join(USER_DIR, USER_INFO)
    user_info = read_json(user_info_path)

    pad = query['pad']
    label = query['label']
    cipher = result['rev_cipher']
    N = public_info['N']
    ke = user_info['ke'] 

    # Output ans
    ans_list = []
    for c in cipher:
        ans_list.append(c['id'])

    #print("Searching result is ", ans_list)    
    
    # Verigy A_c
    A_c = int(accu["A_c"])
    pi_c = int(result["pi_c"])
        
    cipher_prime_list, nonce = cipher_to_prime_list(cipher)

    _A_c = accumulate(cipher_prime_list, pi_c, N)
    
    if _A_c != A_c:
        print("Invalid completeness")
        sys.exit(0)

    
    
    # Verify A_i
    A_i = int(accu["A_i"])
    pi_i = int(result['pi_i'])
    
    ans_id = []
    for c in cipher:
        ans_id.append(int(c['id']))
    l_index_prime_list = []
    for j in range(len(pad)):
        k = 1 if j in ans_id else 0
        prime, nonce= _hash_to_prime(_hash(label=label, k=j, m=(k^int(pad[j]))))
        l_index_prime_list.append(prime)
    
    _A_i = accumulate(l_index_prime_list, pi_i, N)
    if _A_i != A_i:
        print("Invalid correctness")
        sys.exit(0)

    # Decrypt search result

    doc_list = decryptContent(cipher, ke)
    SEARCHING_RESULT = "searching_result.json"
    write_json(os.path.join(USER_DIR, SEARCHING_RESULT), doc_list)

if __name__ == '__main__':
    main()
