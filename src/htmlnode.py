

class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        stringed = ""
        if self.props is None:
            return stringed
        for prop in self.props:
            stringed += (" " + prop + "=" + '"' + self.props[prop] + '"')
        return stringed
    
    def __repr__(self):
        print(f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props:{self.props_to_html}")