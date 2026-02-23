import unittest
from textnode import TextNode, TextType
from conversion import split_nodes_delimiter

class TestSplitDelimiter(unittest.TestCase):

    def test_bold(self):
        old_node = TextNode("this is testing the **BOLD** delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertEqual(
            len(new_nodes),
            3
        )
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.BOLD
        )

    def test_italics(self):
        old_node = TextNode("this is testing _ITALIC_ delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "_", TextType.ITALIC)
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.ITALIC
        )

    def test_code(self):
        old_node = TextNode("testing `code` delimiter", TextType.TEXT)
        new_nodes = split_nodes_delimiter([old_node], "`", TextType.CODE)
        self.assertEqual(
            new_nodes[1].text_type,
            TextType.CODE
        )

    def test_different_delimiters(self):
        old_node = TextNode("now we have **bold** and _italics_", TextType.TEXT)
        first_nodes = split_nodes_delimiter([old_node], "**", TextType.BOLD)
        self.assertEqual(
            first_nodes[1].text_type,
            TextType.BOLD
        )
        second_nodes = split_nodes_delimiter(first_nodes, "_", TextType.ITALIC)
        self.assertEqual(
            second_nodes[1].text_type,
            TextType.BOLD
        )
        self.assertEqual(
            second_nodes[3].text_type,
            TextType.ITALIC
        )