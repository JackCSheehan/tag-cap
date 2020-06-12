# useful RE: <h1\s+.*(class\s*=\s*\"headers\"\s*)\s*(id\s*=\s*\"Main Header\"\s*).*>.*<\/h1>
import re
import urllib.request

REGEX_TEMPLATE = "<%s\s+.*%s.*>.*<\/%s>?"    # Regex template for searching through a page source

# Class that has all of the web scraping functionality
class TagCap:
    # Takes a URL to the webpage that the user wants to scrape and gets its source
    def __init__(self, url):
        self.url = url
        self.source = urllib.request.urlopen(url).read()
        
    # This function finds the given tag name in the page source with the given attributes.
    # Tag name is expected to be a string while attributes is expected to be a dict of
    # signature str : str.
    def get(self, tagName, attributes):
        attributesRegex = ""    # Regex string to search for given attributes

        # Iterate through attributes dict to build regex
        for count, key in enumerate(attributes):
            # Create the regex to search for the current attribute
            currentAttributeRegex = "(%s\\s*=\\s*\\\"%s\\\"\\s*)" % (key, attributes[key])

            # Append the generate regex to the attributes regex string
            attributesRegex += currentAttributeRegex

            # If this is not the last attribute, add a \s* in between so that whitespace between attributes is till found
            if count != len(attributes) - 1:
                attributesRegex += "\\s*"

        # Use regex tememplate and attributes regex to form regex search string
        regexSearchString = REGEX_TEMPLATE % (tagName, attributesRegex, tagName)

        # Search page source using generated regex search string
        searchResults = re.search(regexSearchString, str(self.source), re.DOTALL)
