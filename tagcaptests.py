
import time


start = time.time()
from tag_cap import *
t = TagCap("https://en.wikipedia.org/wiki/Main_Page")

mainDiv = t.get("div", attributes = {"id" : "mp-tfa"})[0].innerHTML

featuredArticleTitle = t.get("a", source = mainDiv)[1]

print("--- %s seconds ---" % (time.time() - start))

print(featuredArticleTitle.attributes["title"])
