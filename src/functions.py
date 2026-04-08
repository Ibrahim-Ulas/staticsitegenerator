import re
import os
import shutil
import pathlib

from .textnode import TextType, TextNode
from .htmlnode import LeafNode, ParentNode
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


def text_to_children(text):
    html_nodes = []
    text_node = text_to_textnodes(text)
    for node in text_node:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes
    

def markdown_to_html_node(markdown):
    page = []
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.P:
            replaced = block.replace("\n", " ")
            parent = ParentNode("p", text_to_children(replaced))
            page.append(parent)
        if block_type == BlockType.Q:
            quoteless = ""
            splitted = block.split("\n")
            for item in splitted: 
                stripped = item.removeprefix("> ")
                quoteless += stripped
            page.append(ParentNode("blockquote", text_to_children(quoteless)))
        if block_type == BlockType.UL:
            list_items = []
            splitted = block.split("\n")
            for items in splitted:
                stripped = items.removeprefix("- ")
                parent = ParentNode("li", text_to_children(stripped))
                list_items.append(parent)
            page.append(ParentNode("ul", list_items))
        if block_type == BlockType.OL:
            list_items = []
            splitted = block.split("\n")
            counter = 1
            for items in splitted:
                stripped = items.removeprefix(f"{counter}. ")
                counter += 1
                parent = ParentNode("li", text_to_children(stripped))
                list_items.append(parent)
            page.append(ParentNode("ol", list_items))
        if block_type == BlockType.H:
            level = len(block) - len(block.lstrip("#"))
            page.append(ParentNode(f"h{level}", text_to_children(block[level + 1:])))
        if block_type == BlockType.C:
            prefix_stripped = block.removeprefix("```")
            suffix_stripped = prefix_stripped.removesuffix("```").lstrip("\n")
            page.append(ParentNode("pre", [LeafNode("code", suffix_stripped)]))
    return ParentNode("div",page)

def extract_title(markdown):
    blocks = markdown_to_blocks(markdown)
    for block in blocks:
        splitted = block.split("\n")
        for line in splitted:
            if line.startswith("# "):
                return line.lstrip("# ")
        raise Exception("There is no header1")

def copy_all_contents(source_directory, destination_directory):
        if os.path.exists(destination_directory):
                shutil.rmtree(destination_directory)
        os.mkdir(destination_directory)
        file_list = os.listdir(source_directory)
        for file in file_list:
                full_source_path = os.path.join(source_directory, file)
                full_dest_path = os.path.join(destination_directory, file)
                if os.path.isfile(full_source_path):
                        shutil.copy(full_source_path, full_dest_path)
                else:
                        copy_all_contents(full_source_path, full_dest_path)
        return destination_directory

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path, "r") as f:
        md = f.read()
    
    with open(template_path, "r") as t:
        template = t.read()
    html= markdown_to_html_node(md).to_html()
    title = extract_title(md)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html)

    dir_path = os.path.dirname(dest_path)
    os.makedirs(dir_path, exist_ok = True)

    with open(dest_path, "w") as d:
        d.write(template)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dirs = os.listdir(dir_path_content)
    for file in dirs:
        joined_path = os.path.join(dir_path_content, file)
        joined_dest_path = os.path.join(dest_dir_path, file)
        if os.path.isfile(joined_path):
            joined_dest_html = pathlib.Path(joined_dest_path).with_suffix(".html")
            generate_page(joined_path, template_path, joined_dest_html)
        else:
            generate_pages_recursive(joined_path, template_path, joined_dest_path)


            
    

