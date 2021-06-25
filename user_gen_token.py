from lib.prf import prf1, prf2
from lib.json_function import read_json, write_json
from bitstring import BitArray
import sys

def main():
    if len (sys.argv) != 4:
        print(len(sys.argv))
        print("Usage: python user_gen_token.py <User ID> <keyword w1> <keywork w2>")
        sys.exit (1)
    '''
    Id = input("User id: ")
    w1 = input("Keyword 1: ")
    w2 = input("Keyword 2: ")
    '''
    Id = str(sys.argv[1])
    w1 = str(sys.argv[2])
    w2 = str(sys.argv[3])

    if w2 < w1:
        tmp = w1
        w1 = w2
        w2 = tmp

    data_path = "user%s_info.json" % (Id)
    data = read_json(data_path, is_G=True)

    public_info = read_json("public_info.json", is_G=True)
    doc_length = public_info['doc_length']

    l = str(w1) + str(w2)
    k1 = data["k1"]
    k2 = data["k2"]
    token = prf1(k1, l)
    pad = BitArray(hex=prf2(k2, l)).bin[:doc_length]
    
    token_path = "user_token"
    with open(token_path, "w") as f:
        f.write(str(token))
    
    pad_path = "user_pad"
    with open(pad_path, "w") as f:
        f.write(pad)

if __name__ == '__main__':
    main()
