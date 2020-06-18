from bs4 import BeautifulSoup

f = open("map.osm")

soup = BeautifulSoup(f, "lxml")

tag = soup.find("node", {"visible" : "true", "id" : "81553135"})
print(tag)