import unittest

from htmlnode import HTMLNode, LeafNode

class TestLeafNode(unittest.TestCase):

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_with_props(self):
        node = LeafNode("a", "link", {"href": "google.com"})
        self.assertEqual(node.to_html(), '<a href="google.com">link</a>', f"Actual: {node.to_html()}")

    def test_leaf_repr_overload(self):
        node = LeafNode("b", "BOLD")
        repr_str = node.__repr__()
        self.assertEqual(repr_str, "LeafNode(b, BOLD, None)")