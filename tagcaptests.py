
import time


start = time.time()
from tag_cap import *
t = TagCap("map.osm")

n = t.get("node", attributes = {"changeset" : "3346612", "id" : "81588599"})
print("--- %s seconds ---" % (time.time() - start))