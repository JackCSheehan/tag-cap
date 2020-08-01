import re
import urllib.request
from urllib.parse import urlparse
from tagcap.element import *
# (?<=>).*?(?=<) <= new text capture can remove the text loop
# <div.*?(?=.*(id)\s*=\s*\"(test-id)\").*?(?=.*(class)\s*=\s*\"(test class)\").*> <= can remove need for if (findall(attributes in current tag if-statement))
# Regex search strings and search string templates
_TAG_WITHOUT_ATTRIBUTES_REGEX_TEMPLATE = "<%s.*?>"                              # Regex templates for seraching for opening tags without attributes
_ATTRIBUTE_REGEX_TEMPLATE = "(?=.*(%s)\\s*=\\s*\\\"(%s)\\\")"                      # Regex template for finding individual attributes
_GET_ATTRIBUTES_REGEX_SEARCH = "([a-zA-z0-9-]+\s*=\s*\"[a-zA-Z0-9-:.()_ ]*\")"  # Regex search string for collecting attributes from found tags 
_SPECIFIC_TAG_REGEX_TEMPLATE = "<[/]{0,1}%s.*?>"                                # Regex template for finding opening and closing tags of a specific name
_TEXT_SEARCH = "(?<=>)(.*?)(?=<)"                                                          # Regex search string to get the text inside an element
_SELF_CLOSING_TAG_SEARCH = "/\\s*>"                                              # Regex search to check for self-closing slash in tag

_TAG_SEARCH_REGEX = "<%s.*?%s.*?>"

# kwargs key names
_ATTRIBUTES_KWARG = "attributes"
_SOURCE_KWARG = "source"

# HTML5 void tags (tags that self-close) given by the official w3 documentation. Ordered as best as possible most used -> least used for efficiency purposes
_HTML5_VOID_TAGS = ["meta", "img", "br", "input", "area", "base", "col", "command", "embed", "hr", "keygen", "link", "param", "source", "track", "wbr"]

# Class that has all of the parsing functionality
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
            file = open(dataLocation, "r", encoding = "utf8")
            self.source = file.read()
            file.close()

    # Make the regular expression used for finding the attributes of a tag
    def __makeAttributesRegex(self, attributes):
        attributesRegex = ""    # Regex string to search for attributes

        # Iterate through attributes dict to build regex
        for count, key in enumerate(attributes):

            # Create the regex to search for the current attribute
            currentAttributeRegex = _ATTRIBUTE_REGEX_TEMPLATE % (key, attributes[key])

            attributesRegex += currentAttributeRegex

            # If this is not the last attribute, add a .* so that attributes in between target attributes don't interrupt search
            if count != len(attributes) - 1:
                attributesRegex += ".*?"
        
        return attributesRegex

    # This function allows users to download files from the given URL. Takes the path to where
    # the file should be saved and the URL to download from.
    def download(self, URL, pathTo):
        urllib.request.urlretrieve(URL, pathTo)

    # This function finds the given tag name in the page source with the given attributes.
    # Tag name is expected to be a string while attributes is expected to be a dict of
    # signature str : str. Returns a list of element objects. Also takes an optional source
    # argument that is a string to parse tags from. If not given, source defaults to
    # self.source.
    def get(self, tagName, **kwargs):
        # Default argument values
        attributes = {}
        source = self.source

        # Check for user-given values for the optional parameters
        if _ATTRIBUTES_KWARG in kwargs:
            attributes = kwargs[_ATTRIBUTES_KWARG]

        if _SOURCE_KWARG in kwargs:
            source = kwargs[_SOURCE_KWARG]

        selfClosing = False     # Flag that indicates whether or not element is self closing
        elements = []           # List of element objects read from source
        
        # Create the attributes regex from the given attributes
        attributesRegex = self.__makeAttributesRegex(attributes)
        
        # Find all tags that have the same name as the given tag name
        for tag in re.finditer(_TAG_SEARCH_REGEX % (tagName, attributesRegex), source):
                    
            # Turn captured attributes into dict for easy access
            capturedAttributes = {}
            attributeCounter = 1
            while attributeCounter < len(tag.groups()):
                capturedAttributes[tag.group(attributeCounter)] = tag.group(attributeCounter + 1)
                attributeCounter += 2

            # Check for slash to indicate if the current tag is self-closing
            if re.findall(_SELF_CLOSING_TAG_SEARCH, tag.group()):
                selfClosing = True

            # Check to see if the given tag name is an HTML5 void tag
            elif any(voidTag in tagName for voidTag in _HTML5_VOID_TAGS):
                selfClosing = True

            # If the user indicates that the tag isn't self-closing, find the closing tag
            if selfClosing == False:

                # Capture the inner HTML of the element by first getting the rest of the document after the current tag
                remainingDocument = source[tag.start():]

                # Create regex search string for finding opening and closing tags with a specific name
                specificTagSearch = _SPECIFIC_TAG_REGEX_TEMPLATE % tagName

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
                    
                # Get the text from the current tag
                capturedText = re.findall(_TEXT_SEARCH, capturedInnerHTML)

                # If no text found, innerHTML will be considered the text, since, in this case, the innerHTML IS the text
                if len(capturedText) == 1:
                    capturedText = [capturedInnerHTML]

                # Add current element to elements list
                elements.append(Element(tagName, capturedAttributes, capturedHTML, capturedInnerHTML, capturedText, selfClosing))
            # If the tag is self closing, it will not have any inner HTML or inner text
            else:
                # Add current element to elements list
                elements.append(Element(tagName, capturedAttributes, tag.group(), None, None, selfClosing))

        # Return list of elements generated
        return elements