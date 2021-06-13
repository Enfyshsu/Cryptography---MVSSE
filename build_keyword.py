import json

def read_json(file_name):
    with open(file_name) as f:
        data = json.load(f)
    return data

def write_json(file_name, doc):
   with open(file_name, "w") as outfile:
        json.dump(doc, outfile, indent=4, separators=(',', ': ')) 

def main():
    words = {}
    keyword = []
    file_name = 'Document.json'
    data = read_json(file_name)
    for d in data:
        tmp = [i.strip().strip(',').strip('.').strip('(').strip(')') for i in d['content'].split()]
        for w in tmp:
            if w not in words.keys():
                words[w] = 0
            words[w] += 1    
    #words = sorted(words.items(), key=lambda x: x[1], reverse=False)
    cnt = 0
    for w in words:
        if words[w] >=5 and words[w] <= 10:
            keyword.append(w)
            cnt += 1
    keyword = read_json("keyword_list.json")
    for d in data:
        d['keywords'] = []
        for w in keyword:
            if w in d['content']:
                d['keywords'].append(w)
    keyword.sort()
    #write_json("keyword_list.json", keyword) 
    write_json(file_name, data)
    
if __name__ == '__main__':
    main()
