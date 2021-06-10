import json

def read_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def main():
    words = {}
    file_name = 'Document.json'
    data = read_json(file_name)
    for d in data:
        tmp = d['content'].split()
        for w in tmp:
            if w. not in words.keys():
                words[w] = 0
            words[w] += 1    
    sorted(words.items(), key=lambda x: x[1])
    for w in words:
        print(w, words[w])
    
if __name__ == '__main__':
    main()
