from tag_cap import TagCap

t = TagCap("https://en.wikipedia.org/wiki/Main_Page")

wrapperDiv = t.get("div", attributes = {"id" : "mp-tfa"})[0]
featuredArticleTitle = t.get("a", source = wrapperDiv.innerHTML)[1].attributes["title"]

blurb = t.get("p", source = wrapperDiv.innerHTML)
print(blurb[0].text)