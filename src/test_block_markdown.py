import unittest
from src.block_markdown import *

class TestMarkdownToBlocks(unittest.TestCase):
    def test_markdown_to_blocks(self):
        # Scenario 1: Standard usage with different block types
        md = """
# This is a heading

This is a paragraph of text. It has some **bold** and _italic_ words inside of it.

- This is the first list item in a list block
- This is a list item
- This is another list item
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and _italic_ words inside of it.",
                "- This is the first list item in a list block\n- This is a list item\n- This is another list item",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        # Scenario 2: Excessive newlines between blocks should be ignored
        md = """
This is a paragraph.


This is another paragraph.


"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is a paragraph.",
                "This is another paragraph.",
            ],
        )

    def test_markdown_to_blocks_whitespace(self):
        # Scenario 3: Blocks with only whitespace (tabs/spaces) should be removed
        md = "Block 1\n\n          \n\nBlock 2"
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "Block 1",
                "Block 2",
            ],
        )

    def test_markdown_to_blocks_single(self):
        # Scenario 4: A single block should return a list with one item
        md = "   Just a single paragraph with some spaces around it.   "
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            ["Just a single paragraph with some spaces around it."]
        )

class TestBlockToBlock(unittest.TestCase):
    def test_block_to_block_types(self):
        # Heading
        self.assertEqual(block_to_block_type("# heading"), BlockType.HEADING)
        # Code
        self.assertEqual(block_to_block_type("```\ncode\n```"), BlockType.CODE)
        # Quote
        self.assertEqual(block_to_block_type("> line 1\n> line 2"), BlockType.QUOTE)
        # Unordered
        self.assertEqual(block_to_block_type("- item 1\n- item 2"), BlockType.UNORDERED_LIST)
        # Ordered
        self.assertEqual(block_to_block_type("1. first\n2. second"), BlockType.ORDERED_LIST)
        # Paragraph
        self.assertEqual(block_to_block_type("just a normal paragraph"), BlockType.PARAGRAPH)

    def test_ordered_list_fail(self):
        # Scenario: Starts at 2 instead of 1
        block = "2. wrong\n3. numbers"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_list_fail(self):
        # Scenario: List item missing the space after the hyphen
        block = "- item1\n-item2"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)
        
if __name__ == "__main__":
    unittest.main()