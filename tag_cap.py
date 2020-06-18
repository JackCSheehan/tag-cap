# useful RE: <h1\s+.*(class\s*=\s*\"headers\"\s*)\s*(id\s*=\s*\"Main Header\"\s*).*>.*<\/h1>
# <span\s+.*(?=class\s*=\s*\"note\"\s*).*?>
# <div\s+.*(?=.*class\s*=\s*\"mw-body-content\").*(?=.*id\s*=\s*\"siteNotice\").*?>
import re
import urllib.request
from urllib.parse import urlparse
from element import *

# Regex search strings and search string templates
TAG_REGEX_TEMPLATE = "<%s\\s+.*%s.*?>"                              # Regex template for searching for opening tag
ATTRIBUTE_REGEX_TEMPLATE = "(?=.*%s\\s*=\\s*\\\"%s\\\")"        # Regex template for finding individual attributes\
GET_ATTRIBUTES_REGEX_SEARCH = "[a-zA-z0-9-]+=\\\"[a-zA-Z0-9-:.()_ ]*\\\""    # Regex search string for collecting attributes from found tags
TAG_NAME_REGEX_SEARCH = "<((?:/|)[a-zA-Z0-9-._]+).*>"               # Regex search string for finding the names of tags   
SPECIFIC_TAG_REGEX_TEMPLATE = "(<%s.*?>|</\\s*%s>)"                 # Regex template for finding opening and closing tags of a specific name
TEXT_SEARCH = "(?<=>).*?(?=<)"                                      # Regex search string to get the text inside an element

# Class that has all of the web scraping functionality
class TagCap:
    # Takes an HTML or XML source in the form of either a URL or a file path
    def __init__(self, dataLocation):
        self.dataLocation = dataLocation

        # Differentiate URLs from local files using url.parse
        if urlparse(dataLocation).netloc != "":
            # Fetch source from given URL
            request = urllib.request.urlopen(dataLocation)
            self.source = request.read().decode("utf8")
            request.close()
        # If data location is a file, open the file and read its contents into self.source
        else:
            file = open(dataLocation, "r")
            self.source = file.read()
            file.close()

    # This function finds the given tag name in the page source with the given attributes.
    # Tag name is expected to be a string while attributes is expected to be a dict of
    # signature str : str. Returns a list of element objects.
    def get(self, tagName, attributes):
        elements = []           # List of element objects read from source
        attributesRegex = ""    # Regex string to search for attributes

        # Iterate through attributes dict to build regex
        for count, key in enumerate(attributes):
            # Create the regex to search for the current attribute
            currentAttributeRegex = ATTRIBUTE_REGEX_TEMPLATE % (key, attributes[key])

            attributesRegex += currentAttributeRegex

            # If this is not the last attribute, add a .* so that attributes in between target attributes don't interrupt search
            if count != len(attributes) - 1:
                attributesRegex += ".*"

        # Create the regex to find open tags that match the given tag name and attributes
        openTagSearch = TAG_REGEX_TEMPLATE % (tagName, attributesRegex)

        # Find opening tags and iterate through each one to process it
        for tag in re.finditer(openTagSearch, self.source):
            # Capture attributes from found tag
            capturedAttributes = re.findall(GET_ATTRIBUTES_REGEX_SEARCH, tag.group())

            # Turn captured attributes into dict for easy access
            attributesDict = {}
            for attribute in capturedAttributes:
                # Remove any quotes in the attributes
                attribute = attribute.replace("\"", "")

                # Split current attribute at = and use the result to form the dict
                splitAttribute = attribute.split("=")
                attributesDict[splitAttribute[0]] = splitAttribute[1]

            # Capture the inner HTML of the element by first getting the rest of the document after the current tag
            remainingDocument = self.source[tag.start():]

            # Create regex search string for finding opening and closing tags with a specific name
            specificTagSearch = SPECIFIC_TAG_REGEX_TEMPLATE % (tagName, tagName)

            # Keep track of the opening and closing tags
            openingTagCount = 0
            closingTagCount = 0

            # Keep track of starting and ending index of closing tag in source
            startOfClosingTag = 0
            endOfClosingTag = 0

            # Find each tag with the same name and iterate through them to find when the tags balance
            for sameNameTag in re.finditer(specificTagSearch, remainingDocument):
                # If the current tag is an opening tag, increment opening tag count
                if sameNameTag.group().startswith("<" + tagName):
                    openingTagCount += 1
                # If the current tag is a closing tag, increment closing tag count
                else:
                    closingTagCount += 1

                # If opening and closing tags are balanced, the closing tag of the current tag has been found
                if (openingTagCount == closingTagCount) and openingTagCount != 0:
                    # Get the start and end index of the same name tag
                    startOfClosingTag = tag.start() + sameNameTag.start()
                    endOfClosingTag = tag.start() + sameNameTag.end()
                    break
                
            # Get the captured HTML (HTML inside tags AND the tags themselves)
            capturedHTML = self.source[tag.start() : endOfClosingTag].strip()

            # Get the captured inner HTML (HTML inside tags ONLY)
            capturedInnerHTML = self.source[tag.end() : startOfClosingTag].strip()

            # Get data from inner HTML that might be text
            possibleText = re.findall(">.*?<", capturedInnerHTML, re.MULTILINE)

            # If no text found, innerHTML will be considered the text, since, in this case, the innerHTML IS the text
            if len(possibleText) == 0:
                capturedText = capturedInnerHTML
            # If text is found with regex search, iterate through it
            else:
                # Get the text inside the current element and cleanse the captured text
                capturedText = []
                for text in possibleText:

                    # If the current text is only brackets, it shouldn't be added to the captured text
                    if text == "><":
                        continue

                    # Remove brackets from text
                    capturedText.append(text.replace(">", "").replace("<", ""))

            # Add current element to elements list
            elements.append(Element(tagName, attributesDict, capturedHTML, capturedInnerHTML, capturedText, False))

        return elements


