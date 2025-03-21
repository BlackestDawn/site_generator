import re
from textnode import TextType, TextNode


def extract_markdown_images(text):
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def extract_markdown_links(text):
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_lst = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            out_lst.append(node)
            continue
        new_nodes = []
        splits = node.text.split(delimiter)
        if len(splits) % 2 == 0:
            raise Exception("Invalid Markdown syntax: delimiter '{delimiter}' not closed")
        for i in range(len(splits)):
            if splits[i] == "":
                continue
            if i % 2 == 0:
                new_nodes.append(TextNode(splits[i], TextType.TEXT))
            else:
                new_nodes.append(TextNode(splits[i], text_type))
        out_lst.extend(new_nodes)

    return out_lst


def split_nodes_image(old_nodes):
    out_lst = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            out_lst.append(node)
            continue
        line = node.text
        image_list = extract_markdown_images(line)
        if len(image_list) == 0:
            out_lst.append(node)
            continue
        for image in image_list:
            split = line.split(f"![{image[0]}]({image[1]})", 1)
            if len(split) != 2:
                raise Exception("Invalid Markdown syntax: image section not closed")
            if split[0] != "":
                out_lst.append(TextNode(split[0], TextType.TEXT))
            out_lst.append(TextNode(image[0], TextType.IMAGE, image[1]))
            line = split[1]
        if line != "":
            out_lst.append(TextNode(line, TextType.TEXT))
    return out_lst


def split_nodes_link(old_nodes):
    out_lst = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT.value:
            out_lst.append(node)
            continue
        line = node.text
        image_list = extract_markdown_links(line)
        if len(image_list) == 0:
            out_lst.append(node)
            continue
        for image in image_list:
            split = line.split(f"[{image[0]}]({image[1]})", 1)
            if len(split) != 2:
                raise Exception("Invalid Markdown syntax: link section not closed")
            if split[0] != "":
                out_lst.append(TextNode(split[0], TextType.TEXT))
            out_lst.append(TextNode(image[0], TextType.LINK, image[1]))
            line = split[1]
        if line != "":
            out_lst.append(TextNode(line, TextType.TEXT))
    return out_lst


def text_to_textnodes(text):
    out_lst = [TextNode(text, TextType.TEXT)]
    out_lst = split_nodes_delimiter(out_lst, "**", TextType.BOLD)
    out_lst = split_nodes_delimiter(out_lst, "*", TextType.ITALIC)
    out_lst = split_nodes_delimiter(out_lst, "_", TextType.ITALIC)
    out_lst = split_nodes_delimiter(out_lst, "`", TextType.CODE)
    out_lst = split_nodes_image(out_lst)
    out_lst = split_nodes_link(out_lst)
    return out_lst
