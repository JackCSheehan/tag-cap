import time

start = time.time()
from tag_cap import *
t = TagCap("map.osm")

nodes = t.get("node", attributes = {"id" : ""})
print(len(nodes))

print("--- %s seconds ---" % (time.time() - start))

