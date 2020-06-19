from tag_cap import *

t = TagCap("map.osm")

n = t.get("node", attributes = {"id" : "6597521361", "version" : "3", "changeset" : "79285199"})

print(n[0].text)
