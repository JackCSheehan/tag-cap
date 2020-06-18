from tag_cap import *

t = TagCap("https://en.wikipedia.org/wiki/Main_Page")

featuredArticle = t.get("div", attributes = {"id" : "mp-welcome"})

print(featuredArticle[0].text)
