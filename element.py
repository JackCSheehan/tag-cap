
# This class is returned in a list from the TagCap get function. Used for organizing information about
# captured elements.
class Element:
    def __init__(self, tagName, attributes, HTML, innerHTML, text, selfClosing):
        self.tagName = tagName          # Name of captured tag
        self.attributes = attributes    # Attributes of captured tag
        self.HTML = HTML                # HTML inside tags AND the tags themselves
        self.innerHTML = innerHTML      # HTML inside of captured tag ONLY
        self.text = text                # Text inside of captured tag
        self.selfClosing = selfClosing  # Bool indicating if the tag is self closing or not