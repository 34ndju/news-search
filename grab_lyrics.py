from bs4 import BeautifulSoup as bs
import urllib2

import metapy
from authentication import Secrets
from pymongo import MongoClient
import lyricwikia #https://github.com/enricobacis/lyricwikia
secrets = Secrets()


link = "https://www.azlyrics.com/lyrics/fountainsofwayne/stacysmom.html"
link = "https://www.azlyrics.com/lyrics/panicatthedisco/thisisgospel.html"

def get_lyrics(link):
    out = ""
    html = urllib2.urlopen(link)
    soup = bs(html, "html5lib")
    for x in soup.find_all("br"):
        try:
            string = str(x.next_sibling.encode('utf-8'))
            if len(string.strip()) > 1 and string.find("<br/>") == -1:
                out += string.strip() + " "
        except:
            continue

    return out

def tokenize(lyrics):
    doc = metapy.index.Document()
    doc.content(lyrics)

    tok = metapy.analyzers.ICUTokenizer()
    tok.set_content(lyrics)
    tokens = [token for token in tok]
    print tokens

lyrics = get_lyrics(link)
print lyrics
tokenize(lyrics)












'''
client = MongoClient('mongodb://' + secrets.USERNAME + ':' + secrets.PASSWORD + '@ds117858.mlab.com:17858/news-search')
b = client["articles"]
'''
