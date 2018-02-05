from bs4 import BeautifulSoup as bs
import urllib2

from collections import Counter
import metapy
from authentication import Secrets
from pymongo import MongoClient
import lyricwikia #https://github.com/enricobacis/lyricwikia
secrets = Secrets()


link = "https://www.azlyrics.com/lyrics/fountainsofwayne/stacysmom.html"
link = "https://www.azlyrics.com/lyrics/logic/18002738255.html"

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
    print ngrams

    return ngrams


parse_and_count(link)












'''
client = MongoClient('mongodb://' + secrets.USERNAME + ':' + secrets.PASSWORD + '@ds117858.mlab.com:17858/news-search')
b = client["articles"]
'''
