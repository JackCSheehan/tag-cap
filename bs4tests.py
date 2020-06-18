from bs4 import BeautifulSoup

f = open("map.osm")

soup = BeautifulSoup(f, "lxml")


n = soup.find("div", {"class" : "js-vote-count grid--cell fc-black-500 fs-title grid fd-column ai-center"})
print(n.text)