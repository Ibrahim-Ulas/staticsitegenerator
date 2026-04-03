import re

from .textnode import TextType, TextNode
from .htmlnode import LeafNode
from .block_type import BlockType

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
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_images(node.text)
        if extracted == []:
            new_nodes.append(node)
            continue
        remaining = node.text
        for part in extracted:
            splitted = remaining.split(f"![{part[0]}]({part[1]})", 1)
            if splitted[0] != "":
                new_nodes.append(TextNode(splitted[0], TextType.PLAIN))
            new_nodes.append(TextNode(part[0], TextType.IMAGE, part[1]))
            remaining = splitted[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.PLAIN))
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.PLAIN:
            new_nodes.append(node)
            continue
        extracted = extract_markdown_links(node.text)
        if extracted == []:
            new_nodes.append(node)
            continue
        remaining = node.text
        for part in extracted:
            splitted = remaining.split(f"[{part[0]}]({part[1]})", 1)
            if splitted[0] != "":
                new_nodes.append(TextNode(splitted[0], TextType.PLAIN))
            new_nodes.append(TextNode(part[0], TextType.LINK, part[1]))
        remaining = splitted[1]
        if remaining != "":
            new_nodes.append(TextNode(remaining, TextType.PLAIN))
    return new_nodes

def text_to_textnodes(text):
    nodes = [TextNode(text, TextType.PLAIN)]
    nodes = split_nodes_delimiter(nodes, "**", TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, "_", TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    new_blocks = []
    for block in blocks:
        stripped = block.strip()
        if stripped != "":
            new_blocks.append(stripped)
    return new_blocks

def block_to_block_type(markdown):
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.H
    if markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.C
    lines = markdown.split("\n")
    counter = 1
    if markdown.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.P
        return BlockType.Q
    
    if markdown.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.P
        return BlockType.UL

    if markdown.startswith("1. "):
        for line in lines:
            if not line.startswith(f"{counter}. "):
                return BlockType.P
            counter += 1
        return BlockType.OL
    return BlockType.P

    def markdown_to_html_node(markdown):
        blocks = markdown_to_blocks(markdown)

        for block in blocks:
            block_type = block_to_block_type(block)
            