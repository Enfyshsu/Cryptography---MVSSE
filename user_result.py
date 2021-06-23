from lib.json_function import read_json
from lib.rsaAccumulator import cipher_to_prime_list, accumulate, cipher_to_prime, _hash, _hash_to_prime

def main():
    result_path = "result.json"
    result = read_json(result_path, is_binary=True)
    
    accu_path = "Accu.json"
    accu = read_json(accu_path)
    
    public_info_path = "public_info.json"
    public_info = read_json(public_info_path)

    query_path  = "user_query"
    query = read_json(query_path, is_G=True)

    pad = query['pad']
    label = query['label']
    cipher = result['rev_cipher']
    N = public_info['N']
    
    
    # Verigy A_c
    A_c = int(accu["A_c"])
    pi_c = int(result["pi_c"])
        
    cipher_prime_list, nonce = cipher_to_prime_list(cipher)

    _A_c = accumulate(cipher_prime_list, pi_c, N)
    if _A_c != A_c:
        print("Invalid completeness")

    
    
    # Verift A_i
    A_i = int(accu["A_i"])
    pi_i = int(result['pi_i'])
    pad = pad[:245]
    
    ans_id = []
    for c in cipher:
        ans_id.append(int(c['id']))
    l_index_prime_list = []
    for j in range(len(pad)):
        k = 1 if j in ans_id else 0
        prime, nonce= _hash_to_prime(_hash(label=label, k=j, m=(k^int(pad[j]))))
        l_index_prime_list.append(prime)
    
    #print(l_index_prime_list)
    _A_i = accumulate(l_index_prime_list, pi_i, N)
    print(_A_i)
    print(A_i)

if __name__ == '__main__':
    main()
