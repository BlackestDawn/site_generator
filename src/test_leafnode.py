import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_empty_value(self):
        with self.assertRaises(ValueError):
            LeafNode("").to_html()

    def test_repl(self):
        node = str(LeafNode("value test"))
        test_val = "LeafNode(None, value test, None)"
        self.assertEqual(node, test_val)

    def test_with_tag(self):
        node = LeafNode("value test", "a")
        test_val = "<a>value test</a>"
        self.assertEqual(node.to_html(), test_val)

    def test_with_prop(self):
        node = LeafNode("value test", "a", {"href": "http://nowhere.org/"})
        test_val = "<a href=\"http://nowhere.org/\">value test</a>"
        self.assertEqual(node.to_html(), test_val)


if __name__ == "__main__":
    unittest.main()
