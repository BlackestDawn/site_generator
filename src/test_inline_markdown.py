import unittest

from textnode import TextNode, TextType
from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)


class TestInlineMarkdown(unittest.TestCase):
    def test_delim_no_formatting(self):
        input = [TextNode("normal text", TextType.TEXT)]
        testing = split_nodes_delimiter(input, "*", TextType.ITALIC)
        expected = [TextNode("normal text", TextType.TEXT)]
        self.assertListEqual(expected, testing)

    def test_delim_simple(self):
        input = [TextNode("normal text *italic text* normal text", TextType.TEXT)]
        testing = split_nodes_delimiter(input, "*", TextType.ITALIC)
        expected = [
            TextNode("normal text ", TextType.TEXT),
            TextNode("italic text", TextType.ITALIC),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertListEqual(expected, testing)

    def test_delim_double(self):
        input = [TextNode("some text with **bold text** and other text with **more bold** words", TextType.TEXT)]
        testing = split_nodes_delimiter(input, "**", TextType.BOLD)
        expected = [
            TextNode("some text with ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode(" and other text with ", TextType.TEXT),
            TextNode("more bold", TextType.BOLD),
            TextNode(" words", TextType.TEXT),
        ]
        self.assertListEqual(expected, testing)

    def test_delim_start_with_formatted(self):
        input = [TextNode("`code text` normal text", TextType.TEXT)]
        testing = split_nodes_delimiter(input, "`", TextType.CODE)
        expected = [
            TextNode("code text", TextType.CODE),
            TextNode(" normal text", TextType.TEXT),
        ]
        self.assertListEqual(expected, testing)

    def test_delim_mixed_nodes(self):
        input = [
            TextNode("This is *italic text* and some **bold text**", TextType.TEXT),
            TextNode("this is a line with **bold words**", TextType.TEXT),
        ]
        testing = split_nodes_delimiter(input, "**", TextType.BOLD)
        expected = [
            TextNode("This is *italic text* and some ", TextType.TEXT),
            TextNode("bold text", TextType.BOLD),
            TextNode("this is a line with ", TextType.TEXT),
            TextNode("bold words", TextType.BOLD),
        ]
        self.assertListEqual(expected, testing)

    def test_image_extraction(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        testing = extract_markdown_images(text)
        expected = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        self.assertListEqual(expected, testing)

    def test_link_extraction(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        testing = extract_markdown_links(text)
        expected = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        self.assertListEqual(expected, testing)

    def test_image_node(self):
        input = [TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)", TextType.TEXT)]
        testing = split_nodes_image(input)
        expected = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
            TextNode(" and ", TextType.TEXT),
            TextNode("obi wan", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
        ]
        self.assertListEqual(expected, testing)

    def test_image_only(self):
        input = [TextNode("![image](https://i.imgur.com/aKaOqIh.gif)", TextType.TEXT)]
        testing = split_nodes_image(input)
        expected = [
            TextNode("image", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
        ]
        self.assertListEqual(expected, testing)

    def test_link_node(self):
        input = [TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT)]
        testing = split_nodes_link(input)
        expected = [
            TextNode("This is text with a link ", TextType.TEXT),
            TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            TextNode(" and ", TextType.TEXT),
            TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),
        ]
        self.assertListEqual(expected, testing)

    def test_mixed_text(self):
        input = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        testing = text_to_textnodes(input)
        expected = [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with an ", TextType.TEXT),
            TextNode("italic", TextType.ITALIC),
            TextNode(" word and a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" and an ", TextType.TEXT),
            TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
            TextNode(" and a ", TextType.TEXT),
            TextNode("link", TextType.LINK, "https://boot.dev"),
        ]
        self.assertListEqual(expected, testing)


if __name__ == "__main__":
    unittest.main()
