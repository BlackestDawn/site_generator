from textnode import TextType, TextNode


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    out_lst = []
    for node in old_nodes:
        if node.text_type == TextType.TEXT.value:
            out_lst.append(node)
            continue
        line = node.text
        new_nodes = []
        start = 0
        delim_count = 0
        while True:
            split_point = line.find(delimiter, start)
            if delim_count % 2 == 1:
                new_nodes.append(TextNode(line[start:split_point], text_type))
                delim_count += 1
                if split_point == len(line) - len(delimiter):
                    break
            else:
                if split_point != -1:
                    new_nodes.append(TextNode(line[start:split_point], TextType.TEXT))
                    delim_count += 1
                else:
                    new_nodes.append(TextNode(line[start:], TextType.TEXT))
                    break
            start = split_point + len(delimiter)
        out_lst.extend(new_nodes)
        if delim_count % 2 == 1:
            raise Exception("Invalid Markdown syntax: delimiter not closed")

    return out_lst
