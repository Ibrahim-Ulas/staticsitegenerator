import unittest

from ..functions import extract_title

class TestExractTitle(unittest.TestCase):
    def test_title_extraction(self):
        md = """
# This is a header
This is not a header
Just a line
"""
        title = extract_title(md)
        self.assertEqual(title, "This is a header")

    def test_no_header(self):
        md = """
This is a header
This is not a header aswell
Just a line
"""
        with self.assertRaises(Exception):
            extract_title(md)

    def test_only_h2(self):
        md = """
## This is a header2
This is not a header aswell
Just a line
"""
        with self.assertRaises(Exception):
            extract_title(md)

if __name__ == "__main__":
    unittest.main()

