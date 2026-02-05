import re
from typing import List
from src.textnode import TextType,TextNode, text_node_to_html_node
from src.parentnode import ParentNode
from src.leafnode import LeafNode
from src.inline_markdown import text_to_textnodes
from src.block_markdown import markdown_to_blocks,block_to_block_type, BlockType

def text_to_children(text: str) -> List[LeafNode]:
    text_nodes = text_to_textnodes(text)
    return [text_node_to_html_node(node) for node in text_nodes]
    
def markdown_to_html_node(markdown: str) -> ParentNode:
    """
    Converts a full markdown document into a single parent HTMLNode. 
    That one parent HTMLNode contains many child HTMLNode objects representing 
    the nested elements.
    """
    blocks = markdown_to_blocks(markdown)
    block_nodes = []
    for block in blocks:
        block_type = block_to_block_type(block)
        # Paragraph Nodes
        if block_type == BlockType.PARAGRAPH:
            child_nodes = text_to_children(block)
            block_nodes.append(ParentNode("p", child_nodes))
        
        # Heading Nodes
        elif block_type == BlockType.HEADING:
            count = len(re.match(r'^#+', block).group())
            tag = f'h{count}'

            # Remove the hashes and the single space that follows them
            text = block[count + 1:]
            block_nodes.append(ParentNode(tag, text_to_children(text)))
        
        elif block_type == BlockType.QUOTE:
            lines = [re.sub(r'^>\s?', '', line) for line in block.split('\n')]
            # Preserve multi-line quote as newlines (or use ' ' if you prefer)
            content = "\n".join(lines).strip()
            # Typical markdown HTML: blockquote contains a paragraph
            p_node = ParentNode("p", text_to_children(content))
            block_nodes.append(ParentNode('blockquote', [p_node]))

        elif block_type == BlockType.UNORDERED_LIST:
            lines = [re.sub(r'^[*-]\s', '', line) for line in block.split('\n')]
            lines = [ParentNode('li',text_to_children(line)) for line in lines]
            block_nodes.append(ParentNode('ul',lines))

        elif block_type == BlockType.ORDERED_LIST:
            lines = [re.sub(r'^\d+\.\s', '', line) for line in block.split('\n')]
            lines = [ParentNode('li',text_to_children(line)) for line in lines]
            block_nodes.append(ParentNode('ol',lines))

        elif block_type == BlockType.CODE:
            code = block[4:-3]
            code_node = text_node_to_html_node(TextNode(code,TextType.CODE))
            block_nodes.append(ParentNode('pre',[code_node]))

    return ParentNode('div',block_nodes)