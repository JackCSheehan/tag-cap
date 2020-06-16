from tag_cap import *

t = TagCap("https://jackcsheehan.github.io/net-pad/index.html")

span = t.get("span", {"id" : "coding-options-dropdown"})

print(span.tagName)
print(span.attributes)
print(span.HTML)
print(span.innerHTML)
print(span.text)
print(span.selfClosing)