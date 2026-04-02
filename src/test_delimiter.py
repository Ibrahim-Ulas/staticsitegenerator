import unittest

from htmlnode import split_nodes_delimiter
from textnode import TextType, TextNode

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

if __name__ == "__main__":
    unittest.main()