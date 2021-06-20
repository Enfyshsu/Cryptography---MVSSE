from lib.json_function import read_json, write_json
from lib.encrypt_document import read_masterkey, encryptContent, gen_key_pair, decryptContent

DOCUMENT_PATH = "./Document.json"
CIPHERTEXT_PATH = "./Cipher.json"
MASTER_KEY_PATH = "./masterkey"

def main():
    data = read_json(DOCUMENT_PATH)
    #print(data)
    k1, k2, k3, k4 = gen_key_pair() 

    cipher_list = encryptContent(data)
    write_json(CIPHERTEXT_PATH, cipher_list, to_binary=True)

    cipher_list = None
    cipher_list = read_json(CIPHERTEXT_PATH, to_binary=True)
    
    decrypt_data = decryptContent(cipher_list)
    for d in decrypt_data:
        if d['content'] == data[int(d['id'])]['content']:
            print("true")
        else:
            print("Flase")

    

if __name__ == "__main__":
    main()           
