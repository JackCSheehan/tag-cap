# useful RE: <h1\s+.*(class\s*=\s*\"headers\"\s*)\s*(id\s*=\s*\"Main Header\"\s*).*>.*<\/h1>
# <span\s+.*(?=class\s*=\s*\"note\"\s*).*?>
# <div\s+.*(?=.*class\s*=\s*\"mw-body-content\").*(?=.*id\s*=\s*\"siteNotice\").*?>
# <[/]*node.*>
import re
import urllib.request
from urllib.parse import urlparse
from element import *

# Regex search strings and search string templates
TAG_WITHOUT_ATTRIBUTES_REGEX_TEMPLATE = "<%s.*?>"                                # Regex templates for seraching for opening tags without attributes
ATTRIBUTE_REGEX_TEMPLATE = "^(?=.*%s\\s*=\\s*\\\"%s\\\")"                       # Regex template for finding individual attributes
GET_ATTRIBUTES_REGEX_SEARCH = "([a-zA-z0-9-]+\s*=\s*\"[a-zA-Z0-9-:.()_ ]*\")"   # Regex search string for collecting attributes from found tags 
SPECIFIC_TAG_REGEX_TEMPLATE = "<[/]{0,1}%s.*?>"                                      # Regex template for finding opening and closing tags of a specific name
TEXT_SEARCH = ">.*?<"                                                           # Regex search string to get the text inside an element
SELF_CLOSING_TAG_SEARCH = "/\s*>"                                               # Regex search to check for self-closing slash in tag

# kwargs key names
ATTRIBUTES_KWARG = "attributes"
SOURCE_KWARG = "source"

# HTML5 void tags (tags that self-close) given by the official w3 documentation. Ordered as best as possible most used -> least used for efficiency purposes
HTML5_VOID_TAGS = ["meta", "img", "br", "input", "area", "base", "col", "command", "embed", "hr", "keygen", "link", "param", "source", "track", "wbr"]

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

    # Make the regular expression used for finding the attribues of a tag
    def __makeAttributesRegex(self, attributes):
        attributesRegex = ""    # Regex string to search for attributes

        # Iterate through attributes dict to build regex
        for count, key in enumerate(attributes):

            # Create the regex to search for the current attribute
            currentAttributeRegex = ATTRIBUTE_REGEX_TEMPLATE % (key, attributes[key])

            attributesRegex += currentAttributeRegex

            # If this is not the last attribute, add a .* so that attributes in between target attributes don't interrupt search
            if count != len(attributes) - 1:
                attributesRegex += ".*"
        
        return attributesRegex

    # Make the captured attributes dictionary based on the attributes of the given tag. Returns the created
    # dictionary.
    def __makeCapturedAttributesDict(self, tag):
        # Turn captured attributes into dict for easy access
        capturedAttributes = {}
        for unparsedAttribute in re.findall(GET_ATTRIBUTES_REGEX_SEARCH, tag.group()):
            
            # Remove any quotes in the attributes
            unparsedAttribute = unparsedAttribute.replace("\"", "")

            # Split current attribute at = and use the result to form the dict
            splitAttribute = unparsedAttribute.split("=")
            capturedAttributes[splitAttribute[0]] = splitAttribute[1]
        
        return capturedAttributes

    # Gets the HTML and inner HTML of the given tag.
    def __getHTMLData(self, source, tag, tagName):
        # Capture the inner HTML of the element by first getting the rest of the document after the current tag
        remainingDocument = source[tag.start():]

        # Create regex search string for finding opening and closing tags with a specific name
        specificTagSearch = SPECIFIC_TAG_REGEX_TEMPLATE % tagName

        # Keep track of the opening and closing tags
        openingTagCount = 0
        closingTagCount = 0

        # Keep track of starting and ending index of closing tag in source
        startOfClosingTag = 0
        endOfClosingTag = 0

        #print(re.findall(specificTagSearch, remainingDocument))

        # Find each tag with the same name and iterate through them to find when the tags balance
        for sameNameTag in re.finditer(specificTagSearch, remainingDocument):

            # If the current tag is an opening tag, increment opening tag count
            if sameNameTag.group().startswith("<" + tagName):
                openingTagCount += 1
            # If the current tag is a closing tag, increment closing tag count
            else:
                closingTagCount += 1

            # If opening and closing tags are balanced, the closing tag of the current tag has been found
            if openingTagCount == closingTagCount and openingTagCount != 0:
 
                # Get the start and end index of the same name tag
                startOfClosingTag = tag.start() + sameNameTag.start()
                endOfClosingTag = tag.start() + sameNameTag.end()
                break

        #TODO: place catch here if both startOfClosingTag and endOfClosingTag are 0

        # Get the captured HTML (HTML inside tags AND the tags themselves)
        capturedHTML = source[tag.start() : endOfClosingTag].strip()

        # Get the captured inner HTML (HTML inside tags ONLY)
        capturedInnerHTML = source[tag.end() : startOfClosingTag].strip()

        return capturedHTML, capturedInnerHTML

    # Gets the text inside the current tag and returns it.
    def __getText(self, capturedInnerHTML):
        # Get data from inner HTML that might be text
        possibleText = re.finditer(TEXT_SEARCH, capturedInnerHTML)

        # If no text found, innerHTML will be considered the text, since, in this case, the innerHTML IS the text
        if sum(1 for _ in possibleText) == 0:
            capturedText = None

        # If text is found with regex search, iterate through it
        else:
            # Get the text inside the current element and cleanse the captured text
            capturedText = []
            for text in possibleText:

                # If the current text is only brackets, it shouldn't be added to the captured text
                if text.group() == "><":
                    continue

                # Remove brackets from text
                capturedText.append(text.group(1))

        return capturedText

    # This function finds the given tag name in the page source with the given attributes.
    # Tag name is expected to be a string while attributes is expected to be a dict of
    # signature str : str. Returns a list of element objects. Also takes a boolean indicating
    # whether or not a tag is self closing. If not given selfClosing defaults to False and
    # attributes defaults to an empty dict
    def get(self, tagName, **kwargs):
        # Default argument values
        attributes = {}
        source = self.source

        # Check for user-given values for the optional parameters
        if ATTRIBUTES_KWARG in kwargs:
            attributes = kwargs[ATTRIBUTES_KWARG]

        if SOURCE_KWARG in kwargs:
            source = kwargs[SOURCE_KWARG]

        selfClosing = False     # Flag that indicates whether or not element is self closing
        elements = []           # List of element objects read from source
        
        # Create the attributes regex from the given attributes
        attributesRegex = self.__makeAttributesRegex(attributes)

        # Find all tags that have the same name as the given tag name
        for tag in re.finditer(TAG_WITHOUT_ATTRIBUTES_REGEX_TEMPLATE % tagName, source):

            # If the user gave no attributes, function doesn't have to search for specific attributes
            if len(attributes) == 0:
                capturedHTML = tag.group()

            # If the user gave attributes, check for attributes
            else:

                # If the correct attributes are not found on this tag, skip the rest of the processing
                if not re.findall(attributesRegex, tag.group()):
                    continue
                    
            # Turn captured attributes into dict for easy access
            capturedAttributes = self.__makeCapturedAttributesDict(tag)

            # Check for slash to indicate if the current tag is self-closing
            if re.findall(SELF_CLOSING_TAG_SEARCH, tag.group()):
                selfClosing = True

            # Check to see if the given tag name is an HTML5 void tag
            elif any(voidTag in tagName for voidTag in HTML5_VOID_TAGS):
                selfClosing = True

            # If the user indicates that the tag isn't self-closing, find the closing tag
            if selfClosing == False:

                # Get HTML and inner HTML from current tag
                capturedHTML, capturedInnerHTML = self.__getHTMLData(source, tag, tagName)
                    
                # Capture the text from this tag
                capturedText = self.__getText(capturedInnerHTML)

                # Add current element to elements list
                elements.append(Element(tagName, capturedAttributes, capturedHTML, capturedInnerHTML, capturedText, selfClosing))
            # If the tag is self closing, it will not have any inner HTML or inner text
            else:
                # Add current element to elements list
                elements.append(Element(tagName, capturedAttributes, tag.group(), None, None, selfClosing))

        # Iterate through attributes dict to build regex
        return elements