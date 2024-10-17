from textnode import TextNode, TextType
from htmlnode import HTMLNode
print("hello world")


def main():
    test_text = TextNode("Test text node", TextType.NORMAL, "http://nowhere.org/")
    print(test_text)
    test_html = HTMLNode(tag="a", props={"href": "http://nowhere.org/"})
    print(test_html)


if __name__ == "__main__":
    main()
