import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_prop_html_eq(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.props_to_html(), ' href="https://www.google.com" target="_blank"')

    if __name__ == "__main__":
        unittest.main()