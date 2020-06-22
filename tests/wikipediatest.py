from tagcap import *

# Create Tag Cap object for the Python Wikipedia page
tagCap = TagCap("https://en.wikipedia.org/wiki/Python_(programming_language)")

# Grab all the links in the contents box
contents = tagCap.get("span", attributes = {"class" : "toctext"})

print(contents)

