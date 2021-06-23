from lib.json_function import read_json, write_json

DOCUMENT_PATH = "./Document.json"
KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"


def owner_modify(document_id, new_content, new_keyword_list):
    modify_document()
    modify_cipher()

def modify_document():


def modify_cipher():
    

def main():
    data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)

    document_id = int(input("Please enter the document id you want to modify: "))
    new_content = input("Please enter the new content of document %s: " % document_id)

    new_keyword_list = []
    for w in keyword:
        if w in new_content:
            new_keyword_list.append(w)

    owner_modify(document_id, new_content, new_keyword_list)

if __name__ == "__main__":
    main()