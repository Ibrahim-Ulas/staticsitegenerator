import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_prop_html_eq(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    def test_prop_html_None(self):
        node = HTMLNode(None, None,None,None)
        self.assertEqual(node.props_to_html(), '')
    
    def test_prop_html_multiple(self):
        node = HTMLNode("i", None, None, {"href": "https://www.google.com", "target": "_blank", "modern": "True", })
        self.assertEqual(node.props_to_html(),' href="https://www.google.com" target="_blank" modern="True"')

    if __name__ == "__main__":
        unittest.main()