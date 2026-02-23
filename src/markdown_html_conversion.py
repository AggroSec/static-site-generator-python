from markdown_blocks import *
from textnode import *
from htmlnode import *
from conversion import *
from enum import Enum

block_to_tag = {
    BlockType.PARAGRAPH:        "p",
    BlockType.HEADING:          "h1",
    BlockType.CODEBLOCK:        "pre",
    BlockType.QUOTE:            "blockquote",
    BlockType.UNORDERED_LIST:   "ul",
    BlockType.ORDERED_LIST:     "ol"
}


def markdown_to_html_node(markdown):
    blocks = markdown_to_blocks(markdown)
    html_blocks = []
    for block in blocks:
        block_type = block_to_block_type(block)
        block_tag = get_block_tag(block_type)
        if block_tag == "h1":
            block_tag = correct_heading(block)
        html_blocks.append(handle_markdown_html_conversion(block, block_type, block_tag))
    return ParentNode("div", html_blocks)

        

def get_block_tag(block_type):
    return block_to_tag[block_type]

def correct_heading(block):
    count = len(block) - len(block.lstrip("#"))
    return f"h{count}"

def strip_markings(block, block_type):
    match block_type:
        case BlockType.HEADING:
            return block.lstrip("#").strip()
        case BlockType.PARAGRAPH:
            return block.replace("\n", " ").strip()
        case BlockType.CODEBLOCK:
            return code_is_special(block)
        case BlockType.QUOTE:
            return "\n".join(line.lstrip().lstrip(">").lstrip() for line in block.splitlines())
        case BlockType.UNORDERED_LIST:
            return "\n".join(line.lstrip("- ").strip() for line in block.splitlines())
        case BlockType.ORDERED_LIST:
            return "\n".join(line.split(".", 1)[1].strip() if "." in line else line.strip() for line in block.splitlines())
        case _:
            raise Exception("Not valid block type")

def code_is_special(block):
    lines = block.splitlines()
    if len(lines) == 2:
        return ""
    code_lines = lines[1:-1]
    code_string = "\n".join(code_lines)
    code_string += "\n"
    return code_string

def handle_codeblock_conversion(text):
    content = LeafNode(None, text)
    code_parent = ParentNode("code", [content])
    pre_parent = ParentNode("pre", [code_parent])
    return pre_parent

def handle_markdown_html_conversion(block, block_type, block_tag):
    #creating text to make into textnodes
    stripped_text = strip_markings(block, block_type)
    text_nodes = []
    children_html_nodes = []
    if block_type == BlockType.CODEBLOCK:
        return handle_codeblock_conversion(stripped_text)
    elif block_type == BlockType.UNORDERED_LIST:
        return handle_unordered_conversion(stripped_text)
    elif block_type == BlockType.ORDERED_LIST:
        return handle_ordered_conversion(stripped_text)
    else:
        text_nodes.extend(text_to_textnodes(stripped_text))
    if not text_nodes:
        raise Exception("something went wrong with text node conversion, block was not codeblock either")
    for text_node in text_nodes:
        children_html_nodes.append(text_node_to_html_node(text_node))
    block_html = ParentNode(block_tag, children_html_nodes)
    return block_html
    
def handle_unordered_conversion(text):
    lines = text.splitlines()
    li_nodes = []
    
    for line in lines:
        item_text = line.strip()  # already stripped marker in strip_markings
        if not item_text:
            continue
        
        # Parse inline Markdown
        text_nodes = text_to_textnodes(item_text)
        
        # Convert TextNodes → HTMLNodes
        item_children = [text_node_to_html_node(tn) for tn in text_nodes]
        
        # Create <li> as ParentNode with inline children
        li_node = ParentNode("li", item_children)
        li_nodes.append(li_node)
    
    return ParentNode("ul", li_nodes)


def handle_ordered_conversion(text):
    lines = text.splitlines()
    li_nodes = []
    
    for line in lines:
        # If the numbering wasn't stripped earlier, do it here
        if ". " in line:
            item_text = line.split(". ", 1)[1].strip()
        else:
            item_text = line.strip()
        
        if not item_text:
            continue
        
        text_nodes = text_to_textnodes(item_text)
        item_children = [text_node_to_html_node(tn) for tn in text_nodes]
        
        li_node = ParentNode("li", item_children)
        li_nodes.append(li_node)
    
    return ParentNode("ol", li_nodes)