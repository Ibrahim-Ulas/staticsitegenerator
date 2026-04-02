from textnode import TextType, TextNode


class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props
    
    def to_html(self):
        raise NotImplementedError("to_html not implemented")
    
    def props_to_html(self):
        stringed = ""
        if self.props is None:
            return stringed
        for prop in self.props:
            stringed += (" " + prop + "=" + '"' + self.props[prop] + '"')
        return stringed
    
    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Children: {self.children}, Props:{self.props_to_html}"

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)

    def to_html(self):
        if self.value is None:
            raise ValueError("Node has no value")
        if self.tag is None:
            return self.value
        return f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'

    def __repr__(self):
        return f"Tag: {self.tag}, Value: {self.value}, Props:{self.props_to_html}"

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        if self.tag is None:
            raise ValueError("Doesn't have a tag")
        if self.children is None:
            raise ValueError("Where are your children")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += child.to_html()
        return result + f"</{self.tag}>"

def text_node_to_html_node(text_node):

    match text_node.text_type:
        case TextType.PLAIN:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    splitted = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            splitted.append(node)
            continue
        parts = node.text.split(delimiter)
        if len(parts) % 2 == 0:
            raise ValueError("not a valid markdown syntax")
        for i, part in enumerate(parts):
            if part == "":
                continue
            if i % 2 == 0:
                splitted.append(TextNode(part, TextType.PLAIN))
            else:
                splitted.append(TextNode(part, text_type))
    return splitted
        

