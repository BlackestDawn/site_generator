import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_prop(self):
        node = str(HTMLNode(value="value test"))
        test_val = "HTMLNode(None, value test, None, None)"
        self.assertEqual(node, test_val)

    def test_empty_prop(self):
        node = str(HTMLNode(props={}))
        test_val = "HTMLNode(None, None, None, None)"
        self.assertEqual(node, test_val)

    def test_props_to_html(self):
        node = HTMLNode(props={"key": "value"}).props_to_html()
        test_val = " key=\"value\""
        self.assertEqual(node, test_val)


if __name__ == "__main__":
    unittest.main()
