import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode, text_node_to_html
from textnode import TextNode, TextType


class TestHTMLNode(unittest.TestCase):
    def test_html_values(self):
        node = HTMLNode("p", "value test", None, {"key": "value"})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "value test")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {"key": "value"})

    def test_html_empty_prop(self):
        node = HTMLNode(props={})
        self.assertEqual(node.props_to_html(), "")

    def test_html_props_to_html(self):
        node = HTMLNode(props={"key": "value"})
        self.assertEqual(node.props_to_html(), " key=\"value\"")

    def test_html_repr(self):
        node = HTMLNode("p", "other value", None, {"key": "other value"})
        self.assertEqual(node.__repr__(), "HTMLNode(p, other value, None, {'key': 'other value'})")

    def test_leaf_empty_values(self):
        with self.assertRaises(ValueError):
            LeafNode("p", None).to_html()
        node = LeafNode(None, "some text")
        self.assertEqual(node.to_html(), "some text")

    def test_leaf_repr(self):
        node = LeafNode("p", "value test")
        self.assertEqual(node.__repr__(), "LeafNode(p, value test, None)")

    def test_leaf_taged(self):
        node = LeafNode("b", "bold text")
        self.assertEqual(node.to_html(), "<b>bold text</b>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "value test", {"href": "http://nowhere.org/"})
        self.assertEqual(node.to_html(), "<a href=\"http://nowhere.org/\">value test</a>")

    def test_parent_empty_values(self):
        with self.assertRaises(ValueError):
            ParentNode("", [LeafNode("a", "some value")]).to_html()
            ParentNode("p", None).to_html()

    def test_parent_minimal(self):
        node = ParentNode("p", [LeafNode("b", "bold text")])
        self.assertEqual(node.to_html(), "<p><b>bold text</b></p>")

    def test_parent_multileaf(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(
            node.to_html(),
            "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        )

    def test_parent_nested(self):
        grandchild_node1 = LeafNode("i", "italic text")
        grandchild_node2 = LeafNode("a", "linky", {"href": "http://nowhere.org/"})
        child_node = ParentNode("span", [grandchild_node1, grandchild_node2])
        node = ParentNode("div", [child_node])
        self.assertEqual(
            node.to_html(),
            "<div><span><i>italic text</i><a href=\"http://nowhere.org/\">linky</a></span></div>"
        )

    def test_text_to_html_conv_normal(self):
        node = text_node_to_html(TextNode("normal text", TextType.TEXT))
        self.assertEqual(node.to_html(), "normal text")

    def test_text_to_html_conv_bold(self):
        node = text_node_to_html(TextNode("bold text", TextType.BOLD))
        self.assertEqual(node.to_html(), "<b>bold text</b>")

    def test_text_to_html_conv_code(self):
        node = text_node_to_html(TextNode("code text", TextType.CODE))
        self.assertEqual(node.to_html(), "<code>code text</code>")

    def test_text_to_html_conv_image(self):
        node = text_node_to_html(TextNode("alt text", TextType.IMAGE, "/images/1.png"))
        self.assertEqual(node.to_html(), "<img src=\"/images/1.png\" alt=\"alt text\"></img>")

    def test_text_to_html_conv_url(self):
        node = text_node_to_html(TextNode("anchor text", TextType.LINK, "http://nowhere.org/"))
        self.assertEqual(node.to_html(), "<a href=\"http://nowhere.org/\">anchor text</a>")


if __name__ == "__main__":
    unittest.main()
