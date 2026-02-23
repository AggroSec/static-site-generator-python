from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
import re


def text_node_to_html_node(text_node):
    match text_node.text_type:
        case TextType.TEXT:
            return LeafNode(None, text_node.text)
        case TextType.BOLD:
            return LeafNode("b", text_node.text)
        case TextType.ITALIC:
            return LeafNode("i", text_node.text)
        case TextType.CODE:
            return LeafNode("code", text_node.text)
        case TextType.LINK:
            return LeafNode("a", text_node.text, {"href": text_node.url})
        case TextType.IMAGE:
            return LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
        case _:
            raise ValueError("text type is not valid")

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            split_text = old_node.text.split(delimiter)
            if len(split_text) == 1:
                new_nodes.append(old_node)
            else:
                if len(split_text) % 2 == 0:
                    raise Exception("Not valid Markdown syntax")
                nodes_to_add = []
                for i in range(1, len(split_text) + 1):
                    if i % 2 == 0:
                        new_node = TextNode(split_text[i-1], text_type)
                        nodes_to_add.append(new_node)
                    else:
                        new_node = TextNode(split_text[i-1], TextType.TEXT)
                        nodes_to_add.append(new_node)
                new_nodes.extend(nodes_to_add)
    return new_nodes

def extract_markdown_images(text):
    extracted_text = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_text

def extract_markdown_links(text):
    extracted_text = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return extracted_text

def split_nodes_image(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            extracted_images = extract_markdown_images(old_node.text)
            split_text = []
            remaining_text = old_node.text
            for extracted_image in extracted_images:
                image_alt, image_link = extracted_image
                current_split = remaining_text.split(f"![{image_alt}]({image_link})", 1)
                split_text.append(current_split[0])
                split_text.append(f"![{image_alt}]({image_link})")
                if len(current_split) > 2:
                    raise Exception("Why do you have the same link in the same text? Invalid, please fix")
                if len(current_split) <= 1:
                    remaining_text =""
                else:
                    remaining_text = current_split[1]
            if remaining_text != "":
                split_text.append(remaining_text)
            nodes_to_add = []
            for i in range(1, len(split_text) + 1):
                if i % 2 != 0:
                    new_node = TextNode(split_text[i-1], TextType.TEXT)
                    nodes_to_add.append(new_node)
                else:
                    extracted = extract_markdown_images(split_text[i-1])
                    image_alt, image_link = extracted[0]
                    new_node = TextNode(image_alt, TextType.IMAGE, image_link)
                    nodes_to_add.append(new_node)
            new_nodes.extend(nodes_to_add)
    return new_nodes


            

def split_nodes_link(old_nodes):
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            new_nodes.append(old_node)
        else:
            extracted_links = extract_markdown_links(old_node.text)
            split_text = []
            remaining_text = old_node.text
            for extracted_link in extracted_links:
                link_text, link = extracted_link
                current_split = remaining_text.split(f"[{link_text}]({link})", 1)
                split_text.append(current_split[0])
                split_text.append(f"[{link_text}]({link})")
                if len(current_split) > 2:
                    raise Exception("Why do you have the same link in the same text? Invalid, please fix")
                if len(current_split) <= 1:
                    remaining_text =""
                else:
                    remaining_text = current_split[1]
            if remaining_text != "":
                split_text.append(remaining_text)
            nodes_to_add = []
            for i in range(1, len(split_text) + 1):
                if i % 2 != 0:
                    new_node = TextNode(split_text[i-1], TextType.TEXT)
                    nodes_to_add.append(new_node)
                else:
                    extracted = extract_markdown_links(split_text[i-1])
                    link_text, link = extracted[0]
                    new_node = TextNode(link_text, TextType.LINK, link)
                    nodes_to_add.append(new_node)
            new_nodes.extend(nodes_to_add)
    return new_nodes

def text_to_textnodes(text):
    text_to_node = TextNode(text, TextType.TEXT)
    new_nodes = split_nodes_image(
        split_nodes_link(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(
                        [text_to_node], 
                        "**", 
                        TextType.BOLD
                        ), 
                    "_", TextType.ITALIC
                    ), 
                "`", TextType.CODE
                )
            )
        )
    return new_nodes