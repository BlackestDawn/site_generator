from htmlnode import HTMLNode


class LeafNode(HTMLNode):
    def __init__(self, value, tag=None, props=None):
        super().__init__(tag=tag, value=value, props=props)

    def to_html(self):
        if self.value is None or not self.value:
            raise ValueError("leafnodes must have a value")
        if self.tag is None:
            return str(self.value)
        props_line = self.props_to_html() or ""
        return f"<{self.tag}{props_line}>{self.value}</{self.tag}>"

    def __repr__(self):
        return f"LeafNode({self.tag}, {self.value}, {self.props_to_html()})"
