
import time


start = time.time()
from tag_cap import *
t = TagCap("map.osm")

n = t.get("node")
print(len(n))
print("--- %s seconds ---" % (time.time() - start))
