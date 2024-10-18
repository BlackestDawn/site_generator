import unittest

from textnode import TextNode, TextType
from inline_markdown import split_nodes_delimiter


class TestInlineMarkdown(unittest.TestCase):
    def test_single_text(self):
        nodes = [TextNode("normal text", TextType.TEXT)]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), [TextNode("normal text", TextType.TEXT)])

    def test_simple_italic(self):
        nodes = [TextNode("normal text *italic text* normal text", TextType.ITALIC)]
        expe_ret = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), expe_ret)

    def test_simple_bold(self):
        nodes = [TextNode("normal text **bold text** normal text", TextType.CODE)]
        expe_ret = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expe_ret)

    def test_simple_code(self):
        nodes = [TextNode("normal text `code text` normal text", TextType.CODE)]
        expe_ret = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expe_ret)

    def test_start_formatted(self):
        nodes = [TextNode("`code text` normal text", TextType.CODE)]
        expe_ret = [
            TextNode("", TextType.TEXT),
            TextNode("code text", TextType.CODE),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "`", TextType.CODE), expe_ret)

    def test_end_formatted(self):
        nodes = [TextNode("normal text **bold text**", TextType.CODE)]
        expe_ret = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "**", TextType.BOLD), expe_ret)

    def test_multiple_nodes(self):
        nodes = [
            TextNode("start text1 *italic text* end text1", TextType.ITALIC),
            TextNode("start text2 *italic text* end text2", TextType.ITALIC),
            TextNode("start text3 *italic text* end text3", TextType.ITALIC),
        ]
        expe_ret = [
            TextNode("start text1 ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" end text1", TextType.TEXT),
            TextNode("start text2 ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" end text2", TextType.TEXT),
            TextNode("start text3 ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" end text3", TextType.TEXT),
        ]
        self.assertEqual(split_nodes_delimiter(nodes, "*", TextType.ITALIC), expe_ret)


if __name__ == "__main__":
    unittest.main()
