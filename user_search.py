from lib.HdrRelated import decrypt_Hdrbar
from lib.json_function import read_json, write_json
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair
import sys

b = 20
S = [1, 2, 3, 4, 5, 6]

def main():
    if len (sys.argv) != 2 :
        print("Usage: python user_search.py <User ID>")
        sys.exit (1)

    Id = sys.argv[1]
    data_path = "user%s_info.json" % (Id)
    data = read_json(data_path, is_G=True)

    public_path = "public_info.json"
    public_info = read_json(public_path, is_G=True)

    reply_path = "server_reply"
    reply = read_json(reply_path, is_G=True)
    Hdr_bar = reply['Hdr_bar']

    gi = public_info["gi"]
    di = data["di"]
    G = PairingGroup('SS512')
    label = decrypt_Hdrbar(G, Hdr_bar, int(Id), gi, di, b, S)
    
    pad_path = "user_pad"
    pad = open(pad_path).read().strip()

    query = dict({"label": label, "pad": pad})
    query_path = "user_query"
    write_json(query_path, query, is_G=True)

if __name__ == '__main__':
    main()        
