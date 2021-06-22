from lib.prf import prf1, prf2
from lib.json_function import read_json, write_json
from bitstring import BitArray

def main():
    Id = input("User id: ")
    w1 = input("Keyword 1: ")
    w2 = input("Keyword 2: ")

    data_path = "user%s_info.json" % (Id)
    data = read_json(data_path, is_G=True)

    l = str(w1) + str(w2)
    k1 = data["k1"]
    k2 = data["k2"]
    token = prf1(k1, l)
    pad = BitArray(hex=prf2(k2, l)).bin
    
    token_path = "user_token"
    with open(token_path, "w") as f:
        f.write(str(token))
    
    pad_path = "user_pad"
    with open(pad_path, "w") as f:
        f.write(pad)

if __name__ == '__main__':
    main()
