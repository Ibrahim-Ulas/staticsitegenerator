import re

from .textnode import TextType, TextNode
from .htmlnode import LeafNode

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

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return matches

def split_nodes_image(old_nodes):
    