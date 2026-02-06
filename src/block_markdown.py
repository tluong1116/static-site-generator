from enum import Enum
from typing import List
import re
from src.htmlnode import HTMLNode
from src.parentnode import ParentNode
from src.leafnode import LeafNode
from src.textnode import TextType, TextNode, text_node_to_html_node
from src.inline_markdown import text_to_textnodes
from src.textnode import text_node_to_html_node

class BlockType(Enum):
    """
    Represents the various types of structural blocks allowed in our 
    Markdown parser.
    """
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered_list'
    ORDERED_LIST = 'ordered_list'

def markdown_to_blocks(markdown: str) -> List[str]:
    """
    Takes a raw Markdown string and splits it into a list of block strings.
    
    Each block is separated by one or more empty lines. Leading and 
    trailing whitespace is removed from each block, and empty blocks 
    are discarded.
    """

    # Break markdown into different lines and strip excess white spaces
    lines = [line.strip() for line in markdown.split('\n\n')]
    # 
    lines = [line for line in lines if line]

    return lines

def block_to_block_type(block: str) -> BlockType:
    """
    Return the BlockType for a single block (passed in as string).
    """
    
    if re.match(r'^#{1,6} ', block):
        return BlockType.HEADING
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    
    block_split = block.split('\n')
    if all(line.startswith('>') for line in block_split):
        return BlockType.QUOTE
    if all(line.startswith('- ') for line in block_split):
        return BlockType.UNORDERED_LIST
    
    is_ordered = True
    for i in range(len(block_split)):
        if not block_split[i].startswith(f"{i+1}. "):
            is_ordered = False
            break
    if is_ordered:
        return BlockType.ORDERED_LIST

    # Default
    return BlockType.PARAGRAPH

def extract_title(markdown: str) -> str:
    blocks = markdown_to_blocks(markdown)
    headers = []
    for block in blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.HEADING and block.startswith('# '):
            headers.append(block[2:].strip())

    if len(headers) == 0:
        raise ValueError("No H1 header found in the markdown")
    if len(headers) > 1:
        raise ValueError("Too many H1 headers in the file")
    return headers[0]
    

        
    