import time

start = time.time()
from lxml import etree

with open("map.osm", "rb") as f:
    xml = f.read()

root = etree.fromstring(xml)
nodes = root.findall(".//node")

print(len(nodes))

print("--- %s seconds ---" % (time.time() - start))