import time

start = time.time()
from bs4 import BeautifulSoup
f = open("map.osm")
soup = BeautifulSoup(f, "lxml")

n = soup.find_all("node")
print(len(n))
print("--- %s seconds ---" % (time.time() - start))
