import time

start = time.time()
from bs4 import BeautifulSoup
f = open("trashedmap.osm")
soup = BeautifulSoup(f, "lxml")

n = soup.find_all("node")
print("--- %s seconds ---" % (time.time() - start))

print(n[0])