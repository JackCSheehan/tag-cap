from tag_cap import *

t = TagCap("map.osm")

n = t.get("node", True, {"id" : "81553135"})

print(n[0].HTML)



