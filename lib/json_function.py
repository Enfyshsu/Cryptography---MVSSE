import json
from charm.toolbox.pairinggroup import PairingGroup,ZR,G1,G2,GT,pair

G = PairingGroup('SS512')
g = G.random(G1)
G_CLASS_NAME = type(g)
del g

def read_json(file_name, is_binary=False, is_G=False):
    with open(file_name) as f:
        data = json.load(f)
        if is_binary:
            for d in data:
                if "ciphertext" in d.keys():
                    d["ciphertext"] = d["ciphertext"].encode()
        if is_G:
            if type(data) == dict:
                if "gi" in data.keys():
                    for d in data["gi"]:
                        if "element" in d.keys() and d["element"] != None:
                            d["element"] = G.deserialize(d["element"].encode())
                elif "Hdr" in data.keys():
                    for i in range(len(data["Hdr"])):
                        data["Hdr"][i] = G.deserialize(data["Hdr"][i].encode())
                elif "Hdr_bar" in data.keys():
                    for i in range(len(data["Hdr_bar"])):
                        data["Hdr_bar"][i] = G.deserialize(data["Hdr_bar"][i].encode())
                elif "di" in data.keys():
                    data["di"] = G.deserialize(data["di"].encode())
                elif "label" in data.keys():
                    data["label"] = G.deserialize(data["label"].encode())

            elif type(data) == list:
                for d in data:
                    if "label" in d.keys():
                        d["label"] = G.deserialize(d["label"].encode())

    return data

def write_json(file_name, doc, is_binary=False, is_G=False):
    encoder_cls = None
    if is_binary or is_G:
        encoder_cls = MyEncoder
    with open(file_name, "w") as outfile:
        json.dump(doc, outfile, indent=4, cls=encoder_cls, separators=(',', ': ')) 

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode();
        if isinstance(obj, G_CLASS_NAME):
            return G.serialize(obj).decode()
        return json.JSONEncoder.default(self, obj)
