from tag_cap import *

t = TagCap("https://stackoverflow.com/questions/29751230/regex-pattern-catastrophic-backtracking")

answerCountElement = t.get("h2", {"class" : "mb0"})

answerCount = answerCountElement[0].attributes
print(answerCount)


