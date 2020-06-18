from bs4 import BeautifulSoup

f = open("map.osm")

soup = BeautifulSoup(f, "lxml")

tag = soup.find("node", {"id" : "81742688"})
print(tag)