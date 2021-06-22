from lib.json_function import read_json, write_json

def main():
    Id = input("User id: ")

    Index_path = "Index.json"
    Index = read_json(Index_path, is_G=True)
    
    Cipher_path = "Cipher.json"
    Cipher = read_json(Cipher_path, is_binary=True)

    query_path = "user%s_query" % (Id)
    query = read_json(query_path, is_G=True)

    label = query['label']
    print("label is ", label)
    for i in Index:
        #print(type(i["label"]))
        if i["label"] == label:
            print(i)

if __name__ == "__main__":
    main()
