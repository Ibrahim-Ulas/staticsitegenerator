import unittest

from ..functions import split_nodes_delimiter
from ..textnode import TextType, TextNode

class TestDelimiter(unittest.TestCase):
    def test_delimiter_bold(self):
        node = TextNode("This is text with a **bold** word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, 
        [
            TextNode("This is text with a ", TextType.PLAIN),
            TextNode("bold", TextType.BOLD),
            TextNode(" word", TextType.PLAIN)
        ])
    
    def test_delimiter_italic(self):
        node = TextNode("This is a text with a _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with a ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word", TextType.PLAIN)
        ])
    
    def test_delimiter_two_italic(self):
        node = TextNode("This is a text with _italic_ and _italic_ word", TextType.PLAIN)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [
            TextNode("This is a text with ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" and ", TextType.PLAIN),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word",TextType.PLAIN)
        ])

if __name__ == "__main__":
    unittest.main()