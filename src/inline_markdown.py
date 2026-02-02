import re
from src.textnode import TextNode, TextType

def split_nodes_delimiter(old_nodes, delimiter,text_type):
    new_nodes = []

    for node in old_nodes:
        # 1. Only split raw text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        # 2. Split the text
        parts = node.text.split(delimiter)

        # 3. Check for matching delimiters (must be an odd number of parts)
        # "text" -> 1 part (no split)
        # "text *bold* text" -> 3 parts (correct)
        # "text *bold" -> 2 parts (missing closing delimiter)
        if len(parts) % 2 == 0:
            raise ValueError(f"Invalid Markdown: missing closing delimiter {delimiter}")
        
        # 4. Create the new nodes
        split_nodes = []
        for i in range(len(parts)):
            if parts[i] == "":
                continue
            if i % 2 == 0:
                # Even indices are the surrounding text
                split_nodes.append(TextNode(parts[i], TextType.TEXT))
            else:
                # Odd indices are the text between delimiters
                split_nodes.append(TextNode(parts[i], text_type))
        
        new_nodes.extend(split_nodes)

    return new_nodes

def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches

def extract_markdown_links(text):
    matches = re.findall(r"\[([^\[\]]*)\]\(([^\(\)]*)\)",text)
    return matches


