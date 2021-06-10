import requests
from bs4 import BeautifulSoup
import os, time, json

# Reference: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
urls = ["https://en.wikipedia.org/wiki/Software-defined_networking", 
            "https://en.wikipedia.org/wiki/MD5", 
            "https://en.wikipedia.org/wiki/World_War_II", 
            "https://en.wikipedia.org/wiki/Copyright", 
            "https://en.wikipedia.org/wiki/Taiwan", 
            "https://en.wikipedia.org/wiki/SHA-2", 
            "https://en.wikipedia.org/wiki/Transmission_Control_Protocol", 
            "https://en.wikipedia.org/wiki/User_Datagram_Protocol", 
            "https://en.wikipedia.org/wiki/Internet_Protocol", 
            "https://en.wikipedia.org/wiki/Network_function_virtualization", 
            "https://en.wikipedia.org/wiki/Time_to_live", 
            "https://en.wikipedia.org/wiki/Transport_Layer_Security", 
            "https://en.wikipedia.org/wiki/5G_network_slicing", 
            "https://en.wikipedia.org/wiki/5G", 
            "https://en.wikipedia.org/wiki/LTE_(telecommunication)",
            ]
title_list = []

def find_text(url):
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    #print(soup)
    result = soup.findAll('p')
    for text in result:
        if text.string != None and len(text.string) > 10:
            return text.string
    
    return None
    #return str(result[3].string)

def build_document(url, n, doc):
    urlList = []
    urlList.append(url)
    
    r = requests.get(url)
    soup = BeautifulSoup(r.text, features="html.parser")
    allLinks = soup.find(id="bodyContent").find_all("a")

    urlBase = "https://en.wikipedia.org"
    cnt = 0
    for link in allLinks:
        try:
            if link['href'].find("/wiki/") == 0:
                if link['href'] not in title_list:
                    urlList.append(urlBase + link['href']) 
                    title_list.append(link['href'])
                    cnt += 1

            if cnt > 30:
                break
        except:
            continue
            
    for url in urlList:
        text = find_text(url)
        if text != None and len(text) > 200:
            #print(url)
            #print(text)
            doc.append(dict({"id": str(n), "content": text.strip()}))
            n += 1
    return n, doc

def main():
    doc = []
    n = 0
    for url in urls:
        print("Parse %s" % (url))
        time.sleep(1)
        n, doc = build_document(url, n, doc)

    with open("Document.json", "w") as outfile: 
        json.dump(doc, outfile, indent=4, separators=(',', ': '))
    #find_text("https://en.wikipedia.org/wiki/OpenFlow")

if __name__ == "__main__":
    main()
