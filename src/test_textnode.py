import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
    
    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node3)

    def test_url_none(self):
        node3 = TextNode("This is a text node", TextType.ITALIC)
        self.assertEqual(node3.url, None)

    def test_text_not_match(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node4 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node4)


if __name__ == "__main__":
    unittest.main()