import unittest

from block_markdown import (
    markdown_to_blocks,
    BlockType,
    block_to_block_type,
)


class TestBlockMarkdown(unittest.TestCase):
    def test_blocks_empty(self):
        input = ""
        testing = markdown_to_blocks(input)
        expected = []
        self.assertEqual(expected, testing)

    def test_blocks_simple(self):
        input = '''# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
'''
        testing = markdown_to_blocks(input)
        expected = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]
        self.assertEqual(expected, testing)

    def test_block_types(self):
        input = "# heading"
        testing = block_to_block_type(input)
        expected = BlockType.HEADING.value
        self.assertEqual(expected, testing)

        input = "```\ncode block\n```"
        testing = block_to_block_type(input)
        expected = BlockType.CODE.value
        self.assertEqual(expected, testing)

        input = "> quote line 1\n> quote line 2"
        testing = block_to_block_type(input)
        expected = BlockType.QUOTE.value
        self.assertEqual(expected, testing)

        input = "* unordered list\n* star character"
        testing = block_to_block_type(input)
        expected = BlockType.UNORDERED.value
        self.assertEqual(expected, testing)

        input = "- unordered list\n- dash character"
        testing = block_to_block_type(input)
        expected = BlockType.UNORDERED.value
        self.assertEqual(expected, testing)

        input = "1. ordered list\n2. second item"
        testing = block_to_block_type(input)
        expected = BlockType.ORDERED.value
        self.assertEqual(expected, testing)

        input = "simple text"
        testing = block_to_block_type(input)
        expected = BlockType.PARAGRAPH.value
        self.assertEqual(expected, testing)
