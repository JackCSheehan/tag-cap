from tag_cap import TagCap

t = TagCap("https://en.wikipedia.org/wiki/Main_Page")

wrapperDiv = t.get("div", attributes = {"id" : "mp-tfa"})[0]
#print(wrapperDiv.attributes)
#print(wrapperDiv.HTML)
#print(wrapperDiv.innerHTML)
#print(wrapperDiv.selfClosing)
print(len(wrapperDiv.text))
print(wrapperDiv.text)