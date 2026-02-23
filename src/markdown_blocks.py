from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODEBLOCK = "codeblock"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"

def markdown_to_blocks(markdown):
    blocks = markdown.split("\n\n")
    return [block.strip() for block in blocks if block.strip()]

def block_to_block_type(block):
    prefixes = ["# ", "## ", "### ", "#### ", "##### ", "###### "]

    if any(block.startswith(p) for p in prefixes):
        return BlockType.HEADING
    if block.startswith("```\n"):
        lines = block.splitlines()
        if lines[-1] == "```":
            return BlockType.CODEBLOCK
    if block.startswith(">"):
        lines = block.splitlines()
        full_quote = True
        for line in lines:
            if not line.startswith(">"):
                full_quote = False
        if full_quote:
            return BlockType.QUOTE
    if block.startswith("- "):
        lines = block.splitlines()
        is_list = True
        for line in lines:
            if not line.startswith("- "):
                is_list = False
        if is_list:
            return BlockType.UNORDERED_LIST
    if block.startswith("1. "):
        lines = block.splitlines()
        number = 1
        is_numbered = True
        for line in lines:
            if not line.startswith(f"{number}. "):
                is_numbered = False
            number += 1
        if is_numbered:
            return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
    # write tests for each and failure cases. write one case to test each type, then write failure cases which should default to paragraph cause people are weird


    
    
    