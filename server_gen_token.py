from lib.prf import prf3
from lib.json_function import read_json, write_json



def main():
    data = read_json("server_info.json", is_G=True)
    k3 = data["k3"]
    
    token_path = "user_token"
    token = int(open(token_path, "r").read().strip())
    r = prf3(k3, token)
    print(r)

    c0 = data["Hdr"][0]
    c1 = data["Hdr"][1]
    power = r * token
    Hdr_bar = [c0**power, c1**power] 
    reply = dict({"r": str(r), "Hdr_bar": Hdr_bar})
    reply_path = "server_reply"
    write_json(reply_path, reply, is_G=True)

if __name__ == '__main__':
    main()
