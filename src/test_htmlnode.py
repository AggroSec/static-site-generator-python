import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):

    def test_base_htmlnode_to_html(self):
        node = HTMLNode()
        with self.assertRaises(NotImplementedError, msg="method should not be implemented in base"):
            node.to_html()

    def test_repr_returns_string_with_none(self):
        node = HTMLNode()

        result = node.__repr__()
        self.assertIsInstance(result, str, "repr() must return a string")
        self.assertEqual(
            result,
            "HTMLNode(None, None, None, None)",
            "repr() format is incorrect for all-None node"
        )
    
    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})

        result = node.props_to_html()
        self.assertEqual(result, 'href="https://www.google.com" target="_blank"')