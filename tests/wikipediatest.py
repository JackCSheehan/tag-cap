from tagcap.tagcap import TagCap

# Create Tag Cap object for the Python Wikipedia page
t = TagCap("https://en.wikipedia.org/wiki/Python_(programming_language)")

# Grab all the links in the contents box
contents = t.get("span", attributes = {"class" : "toctext"})

for element in contents:
    print(element.text)

