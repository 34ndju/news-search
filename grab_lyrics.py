from bs4 import BeautifulSoup as bs
import urllib2
import os
import math

from collections import Counter
import metapy
from authentication import Secrets
from pymongo import MongoClient
import lyricwikia #https://github.com/enricobacis/lyricwikia
secrets = Secrets()

links = []
links.append("https://www.azlyrics.com/lyrics/fountainsofwayne/stacysmom.html")
links.append("https://www.azlyrics.com/lyrics/logic/18002738255.html")
links.append("https://www.azlyrics.com/lyrics/panicatthedisco/ladevotee.html")

def get_lyrics(link):
    out = ""
    html = urllib2.urlopen(link)
    soup = bs(html, "html5lib")
    for x in soup.find_all("br"):
        try:
            string = str(x.next_sibling.encode('utf-8'))
            if len(string.strip()) > 1 and string.find(">") == -1:
                out += string.strip() + " "
        except:
            continue

    return out

def parse_and_count(link):
    tag_suppression = True
    n = 1
    min_token_len = 4
    max_token_len = 30

    lyrics = get_lyrics(link)

    doc = metapy.index.Document()
    doc.content(lyrics)

    tok = metapy.analyzers.ICUTokenizer(suppress_tags= tag_suppression)
    tok = metapy.analyzers.LengthFilter(tok, min=min_token_len, max=max_token_len)
    tok = metapy.analyzers.ListFilter(tok, "lemur-stopwords.txt", metapy.analyzers.ListFilter.Type.Reject)
    tok = metapy.analyzers.Porter2Filter(tok)
    tok = metapy.analyzers.LowercaseFilter(tok)

    tok.set_content(lyrics)
    #tokens = [token for token in tok]

    ana = metapy.analyzers.NGramWordAnalyzer(n, tok)
    ngrams = ana.analyze(doc)

    return ngrams

#def tf_idf_normalize()

def write_file(filename, contents):
    file = open(filename, "w")
    file.write(str(contents))
    file.close()

def write_dicts(links):

    idf_num = 5

    doc_freqs = Counter()
    for link in links:
        id = link[link.rfind("/")+1:link.find(".html")]
        result = parse_and_count(link)

        for token in result:
            doc_freqs[token] += 1

        write_file("dicts/" + id + ".txt", result)

    for filename in os.listdir("dicts"):
        print filename
        file = open("dicts/" + filename, "r")
        contents = file.read()
        file.close()

        result = eval(contents)

        for token in result:
            log_int = idf_num / float(doc_freqs[token]) if token in doc_freqs else 1
            idf = math.log(log_int)
            result[token] *= idf

        write_file("dicts/" + filename, str(result))

    #write_file("dicts/doc_freqs_counter.txt", str(doc_freqs))

write_dicts(links)


'''
f = open("test.txt", "r")
contents = f.read()
print(eval(contents))
'''












'''
client = MongoClient('mongodb://' + secrets.USERNAME + ':' + secrets.PASSWORD + '@ds117858.mlab.com:17858/news-search')
b = client["articles"]
'''
