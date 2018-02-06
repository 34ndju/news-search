from bs4 import BeautifulSoup as bs
from universal import Universal
import urllib2
import urllib
import os
import math
import time

from collections import Counter
import metapy

from authentication import Secrets
from pymongo import MongoClient
import lyricwikia #https://github.com/enricobacis/lyricwikia
universe = Universal()
secrets = Secrets()

links = []
links.append("https://www.azlyrics.com/lyrics/fountainsofwayne/stacysmom.html")
links.append("https://www.azlyrics.com/lyrics/logic/18002738255.html")
links.append("https://www.azlyrics.com/lyrics/panicatthedisco/ladevotee.html")

def get_lyrics(link):
    html = urllib2.urlopen(link)
    soup = bs(html, "html5lib")
    return soup.find("pre", {"id":"lyric-body-text"}).text

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

def write_file(filename, contents):
    file = open(filename, "w")
    file.write(str(contents))
    file.close()

#also does tf idf weighting
def write_dicts(genre, links):

    req_timeout = 3 #seconds
    raw_counts_dir_name = universe.raw_counts_dir_name
    normalized_dir_name = universe.normalized_dir_name
    delimiter = universe.delimiter

    if not os.path.exists(normalized_dir_name):
        os.mkdir(normalized_dir_name)

    if not os.path.exists(raw_counts_dir_name):
        os.mkdir(raw_counts_dir_name)

    doc_freqs = Counter()
    doc_count = 0
    for link in links:
        link = urllib.unquote(link)
        id = link[link.rfind("/")+1:].lower().replace("+","_").replace("'", "")
        filename = id + ".txt"

        if filename in os.listdir(raw_counts_dir_name):
            print "found " + filename
            file = open(raw_counts_dir_name + "/" + filename, "r")
            contents = file.read().split(delimiter)
            file.close()
            genre = contents[0] #do something
            result = eval(contents[-1])
        else:
            print "creating " + filename
            result = parse_and_count(link)
            out = genre + delimiter + str(result)
            write_file(raw_counts_dir_name + "/" + filename, out)
            time.sleep(req_timeout)

        for token in result:
            doc_freqs[token] += 1
        doc_count += 1

    for filename in os.listdir(raw_counts_dir_name):
        file = open(raw_counts_dir_name + "/" + filename, "r")
        contents = file.read().split(delimiter)
        file.close()

        genre = contents[0]
        result = eval(contents[-1])

        for token in result:
            log_int = doc_count / float(doc_freqs[token])
            idf = math.log(log_int)
            result[token] *= idf

        out = genre + delimiter + str(result)
        write_file(normalized_dir_name + "/" + filename, out)

if __name__ == "__main__":
    links = []
    links.append("https://www.lyrics.com/lyric/32381346/Panic%21+At+the+Disco/La+Devotee")
    links.append("https://www.lyrics.com/lyric/13945900/Panic%21+At+the+Disco/Nine+in+the+Afternoon")

    write_dicts(links)


'''
client = MongoClient('mongodb://' + secrets.USERNAME + ':' + secrets.PASSWORD + '@ds117858.mlab.com:17858/news-search')
b = client["articles"]
'''
