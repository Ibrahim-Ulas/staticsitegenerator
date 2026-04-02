import unittest

from ..htmlnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_eq(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_to_html_eq_with_prop(self):
        node = LeafNode("a", "Google", {"href": "https://www.google.com", "target": "_blank"})
        self.assertEqual(node.to_html(), '<a href="https://www.google.com" target="_blank">Google</a>')

if __name__ == "__main__":
    unittest.main()
