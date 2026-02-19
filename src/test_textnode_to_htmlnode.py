import unittest
from conversion import text_node_to_html_node
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode

class TestTextToHtml(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")
    
    def test_bold(self):
        node = TextNode("this is bolded", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), "<b>this is bolded</b>")

    def test_link(self):
        node = TextNode("link here", TextType.LINK, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<a href="google.com">link here</a>')

    def test_image(self):
        node = TextNode("alttext", TextType.IMAGE, "google.com")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.to_html(), '<img src="google.com" alt="alttext"></img>')