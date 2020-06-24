# Test of tagcap/BS4 with an OpenStreetMap export of the northern half of central park
import sys
import time
sys.path.append("../tagcap")

# Start of BS4 Test
start = time.time()
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("broadway.osm", encoding = "utf8"), "lxml")

soup.find_all("node")
print("%s seconds" % (time.time() - start))

# Start of TagCap test
start = time.time()
from tag_cap import TagCap

t = TagCap("broadway.osm")

n = t.get("node")
print("%s seconds" % (time.time() - start))

