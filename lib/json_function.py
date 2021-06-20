import json

def read_json(file_name, to_binary=False):
    with open(file_name) as f:
        data = json.load(f)
        if to_binary:
            for d in data:
                if "ciphertext" in d.keys():
                    d["ciphertext"] = d["ciphertext"].encode()
    return data

def write_json(file_name, doc, to_binary=False):
    encoder_cls = None
    if to_binary:
        encoder_cls = MyEncoder
    with open(file_name, "w") as outfile:
        json.dump(doc, outfile, indent=4, cls=encoder_cls, separators=(',', ': ')) 

class MyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, bytes):
            return obj.decode();
        return json.JSONEncoder.default(self, obj)
