from lib.json_function import read_json, write_json
from bitstring import BitArray

def main():
    Index_path = "Index.json"
    Index = read_json(Index_path, is_G=True)
    
    Cipher_path = "Cipher.json"
    Cipher = read_json(Cipher_path, is_binary=True)

    query_path = "user_query"
    query = read_json(query_path, is_G=True)

    label = query['label']
    pad = query['pad']
    #print("label is ", label)
    rev_doc_id = []
    for i in Index:
        #print(type(i["label"]))
        if i["label"] == label:
            #print(i)
            index_bar = i['index_bar']
            doc_length = len(index_bar)
            index = (BitArray(bin=index_bar) ^ BitArray(bin=pad[:doc_length])).bin
            for i in range(len(index)):
                if index[i] == '1':
                    rev_doc_id.append(i)

    rev_doc = []
    print("Result contains docment id, ", rev_doc_id)
    for i in rev_doc_id:    
        rev_doc.append(Cipher[i])

    result_path = "result.json"
    write_json(result_path, rev_doc, is_binary=True)

if __name__ == "__main__":
    main()
