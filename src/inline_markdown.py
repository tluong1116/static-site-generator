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

def split_nodes_image(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # 1. Only split raw text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        image_parts = extract_markdown_images(original_text)
        
        if len(image_parts) == 0:
            new_nodes.append(node)
            continue

        for image in image_parts:
            image_alt = image[0]
            image_url = image[1]
            sections = original_text.split(f"![{image_alt}]({image_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, image section not found")
            
            # Add text before the image (if it's not empty)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(image_alt, TextType.IMAGE, image_url))
            original_text = sections[1]

        # After the loop, add any remaining text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes


def split_nodes_link(old_nodes):
    new_nodes = []

    for node in old_nodes:
        # 1. Only split raw text nodes
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
            continue
        
        original_text = node.text
        link_parts = extract_markdown_links(original_text)
        
        if len(link_parts) == 0:
            new_nodes.append(node)
            continue

        for link in link_parts:
            link_alt = link[0]
            link_url = link[1]
            sections = original_text.split(f"[{link_alt}]({link_url})", 1)

            if len(sections) != 2:
                raise ValueError("Invalid markdown, link section not found")
            
            # Add text before the link (if it's not empty)
            if sections[0] != "":
                new_nodes.append(TextNode(sections[0], TextType.TEXT))

            new_nodes.append(TextNode(link_alt, TextType.LINK, link_url))
            original_text = sections[1]

        # After the loop, add any remaining text
        if original_text != "":
            new_nodes.append(TextNode(original_text, TextType.TEXT))

    return new_nodes