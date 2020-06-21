
import time


start = time.time()
from tag_cap import *
t = TagCap("https://en.wikipedia.org/wiki/Main_Page")


print("--- %s seconds ---" % (time.time() - start))

