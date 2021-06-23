from lib.json_function import read_json, write_json
from lib.encrypt_document import encryptContent

DOCUMENT_PATH = "./Document.json"
KEYWORD_PATH = "keyword_list.json"
CIPHERTEXT_PATH = "./Cipher.json"
ke = "632a0c4ac96376d35bb1060778c63d852299c64949a42e2e857ff2aa7fbbc563"

def modify(document_id, new_content):
    data = read_json(DOCUMENT_PATH)
    keyword = read_json(KEYWORD_PATH)

    new_keywords = []
    for w in keyword:
        if w in new_content:
            new_keywords.append(w)

    for d in data:
        if d["id"] == document_id:
            d["content"] = new_content
            d["keywords"] = new_keywords
    write_json(DOCUMENT_PATH, data, is_G=True)

    cipher = encryptContent(data, ke)
    write_json(CIPHERTEXT_PATH, cipher, is_binary=True)


def main():
    document_id = input("Please enter the document id you want to modify: ")
    new_content = input("Please enter the new content of document %s: " % document_id)

    modify(document_id, new_content)

if __name__ == "__main__":
    main()