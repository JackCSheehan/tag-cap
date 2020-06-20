# useful RE: <h1\s+.*(class\s*=\s*\"headers\"\s*)\s*(id\s*=\s*\"Main Header\"\s*).*>.*<\/h1>
# <span\s+.*(?=class\s*=\s*\"note\"\s*).*?>
# <div\s+.*(?=.*class\s*=\s*\"mw-body-content\").*(?=.*id\s*=\s*\"siteNotice\").*?>
# <[/]*node.*>
import re
import urllib.request
from urllib.parse import urlparse
from element import *

# Regex search strings and search string templates
TAG_WITH_ATTRIBUTES_REGEX_TEMPLATE = "<%s\\s+.*%s.*?>"                      # Regex template for searching for opening tag
TAG_WITHOUT_ATTRIBUTES_REGEX_TEMPLATE = "<%s.*>"                            # Regex templates for seraching for opening tags without attributes
ATTRIBUTE_REGEX_TEMPLATE = "^(?=.*%s\\s*=\\s*\\\"%s\\\")"                        # Regex template for finding individual attributes
GET_ATTRIBUTES_REGEX_SEARCH = "[a-zA-z0-9-]+=\\\"[a-zA-Z0-9-:.()_ ]*\\\""   # Regex search string for collecting attributes from found tags 
SPECIFIC_TAG_REGEX_TEMPLATE = "<[/]*%s.*>"                                  # Regex template for finding opening and closing tags of a specific name
TEXT_SEARCH = ">.*?<"                                                       # Regex search string to get the text inside an element

# kwargs key names
SELF_CLOSING_KWARG = "selfClosing"
ATTRIBUTES_KWARG = "attributes"

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
    # signature str : str. Returns a list of element objects. Also takes a boolean indicating
    # whether or not a tag is self closing. If not given selfClosing defaults to False and
    # attributes defaults to an empty dict
    def get(self, tagName, **kwargs):
        # Default argument values
        selfClosing = False
        attributes = {}

        # Check for user-given values for the optional parameters
        if SELF_CLOSING_KWARG in kwargs:
            selfClosing = kwargs[SELF_CLOSING_KWARG]
        
        if ATTRIBUTES_KWARG in kwargs:
            attributes = kwargs[ATTRIBUTES_KWARG]

        elements = []           # List of element objects read from source

        # Find all elements of the given tag name
        tags = re.findall("<%s.*>" % tagName, self.source)

        attributesRegex = ""    # Regex string to search for attributes

        # Iterate through attributes dict to build regex
        for count, key in enumerate(attributes):
            # Create the regex to search for the current attribute
            currentAttributeRegex = ATTRIBUTE_REGEX_TEMPLATE % (key, attributes[key])

            attributesRegex += currentAttributeRegex

            # If this is not the last attribute, add a .*? so that attributes in between target attributes don't interrupt search
            if count != len(attributes) - 1:
                attributesRegex += ".*?"

        # Find same-named tags with the correct attributes
        for tag in tags:

            # If the attributes search finds the correct attributes, then capture the rest of the data to put into an Element object
            if len(re.findall(attributesRegex, tag)) >= 1:
                print(tag)
            else:
                continue
                
            

        return elements