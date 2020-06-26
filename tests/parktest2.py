# Test of tagcap/BS4 with an OpenStreetMap export of the northern half of central park
import time

# Start of TagCap test
start = time.time()
import tagcap

t = tagcap.TagCap("park.osm")

n = t.get("relation", attributes = {"id" : "11212767", "changeset" : "86790695"})
print("%s seconds" % (time.time() - start))

# Start of BS4 Test
start = time.time()
from bs4 import BeautifulSoup

soup = BeautifulSoup(open("park.osm", encoding = "utf8"), "lxml")

n = soup.find_all("node", {"id" : "11212767", "changeset" : "86790695"})
print("%s seconds" % (time.time() - start))