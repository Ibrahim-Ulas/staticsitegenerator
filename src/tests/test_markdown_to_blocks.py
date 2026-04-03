import unittest

from ..functions import markdown_to_blocks, block_to_block_type
from .. block_type import BlockType

class TestMarkdownToBlocks(unittest.TestCase):
        def test_markdown_to_blocks(self):
            md = """
This is **bolded** paragraph

This is another paragraph with _italic_ text and `code` here
This is the same paragraph on a new line

- This is a list
- with items
"""
            blocks = markdown_to_blocks(md)
            self.assertEqual(
                blocks,
                [
                    "This is **bolded** paragraph",
                    "This is another paragraph with _italic_ text and `code` here\nThis is the same paragraph on a new line",
                    "- This is a list\n- with items",
                ],
            )

        def test_markdown_block_to_block_type_header(self):
            markdown = "# This is a Header"
            block_type = block_to_block_type(markdown)
            self.assertEqual(block_type, BlockType.H)

        def test_markdown_block_to_block_type_code(self):
            markdown = "```This is a code```"
            block_type = block_to_block_type(markdown)
            self.assertEqual(block_type, BlockType.C)
        
        def test_markdown_block_to_block_type_quote(self):
            markdown = ">This is a quote"
            block_type = block_to_block_type(markdown)
            self.assertEqual(block_type, BlockType.Q)
        
        def test_markdown_block_to_block_type_unordered_list(self):
            markdown = "- This is a unordered list line\n- This is a unordered list line2"
            block_type = block_to_block_type(markdown)
            self.assertEqual(block_type, BlockType.UL)

        def test_markdown_block_to_block_type_unordered_list_not_eq(self):
            markdown = "- This is a unordered list line\n- This is a unordered list line2\nThis should break the list"

            block_type = block_to_block_type(markdown)
            self.assertNotEqual(block_type, BlockType.UL)

        def test_markdown_block_to_block_type_ordered_list(self):
            markdown = "1. This is a ordered list line\n2. This is a ordered list line2\n3. This is a ordered list line3"
            block_type = block_to_block_type(markdown)
            self.assertEqual(block_type, BlockType.OL)
        
        def test_markdown_block_to_block_type_ordered_list_not_eq(self):
            markdown = "1. This is a ordered list line\n2. This is a ordered list line2\nThis is a corrupt ordered list line3"    
            block_type = block_to_block_type(markdown)
            self.assertNotEqual(block_type, BlockType.OL)

if __name__ == "__main__":
    unittest.main()