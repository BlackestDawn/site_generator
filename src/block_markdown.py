from enum import Enum
from htmlnode import ParentNode, text_node_to_html
from inline_markdown import text_to_textnodes


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED = "unorded"
    ORDERED = "orded"


def markdown_to_blocks(markdown):
    out_lst = []
    for block in markdown.split("\n\n"):
        if block == "":
            continue
        out_lst.append(block.strip())
    return out_lst


def block_to_block_type(block):
    lines = block.split("\n")

    if block.startswith(("# ", "## ", "### ", "#### ", "##### ", "##### ", )):
        return BlockType.HEADING.value
    if len(lines) > 1 and lines[0].startswith("```") and lines[-1].startswith("```"):
        return BlockType.CODE.value
    if block.startswith("> "):
        for line in lines:
            if not line.startswith("> "):
                return BlockType.PARAGRAPH.value
        return BlockType.QUOTE.value
    if block.startswith("* "):
        for line in lines:
            if not line.startswith("* "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED.value
    if block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH.value
        return BlockType.UNORDERED.value
    if block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH.value
            i += 1
        return BlockType.ORDERED.value
    return BlockType.PARAGRAPH.value


def text_to_children(text):
    text_lst = text_to_textnodes(text)
    html_lst = []
    for node in text_lst:
        html_lst.append(text_node_to_html(node))

    return html_lst


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    node_lst = []
    for block in blocks:
        block_type = block_to_block_type(block)
        match block_type:
            case BlockType.PARAGRAPH.value:
                sub_nodes = text_to_children(block)
                node_lst.append(ParentNode("p", sub_nodes))
            case BlockType.HEADING.value:
                heading_level = block.find(" ")
                sub_nodes = text_to_children(block[heading_level + 1:])
                node_lst.append(ParentNode(f"h{heading_level}", sub_nodes))
            case BlockType.CODE.value:
                sub_nodes = text_to_children(block[3:-4].replace("\n", "<br />"))
                code_block = ParentNode("code", sub_nodes)
                node_lst.append(ParentNode("pre", [code_block]))
            case BlockType.QUOTE.value:
                sub_nodes = text_to_children(block.replace("> ", "").replace("\n", "<br />"))
                node_lst.append(ParentNode("blockquote", sub_nodes))
            case BlockType.UNORDERED.value:
                lines = block.split("\n")
                sub_nodes = []
                for line in lines:
                    sub_nodes.append(ParentNode("li", text_to_children(line[2:])))
                node_lst.append(ParentNode("ul", sub_nodes))
            case BlockType.ORDERED.value:
                lines = block.split("\n")
                sub_nodes = []
                for line in lines:
                    sub_nodes.append(ParentNode("li", text_to_children(line[3:])))
                node_lst.append(ParentNode("ol", sub_nodes))

    return ParentNode("div", node_lst)
