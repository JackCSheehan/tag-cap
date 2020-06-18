from tag_cap import *

t = TagCap("map.osm")

n = t.get("node", True, {"id" : "81553135", "visible" : "true"})

print(n[0].HTML)



