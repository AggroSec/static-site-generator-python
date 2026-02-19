import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestParentNode(unittest.TestCase):

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_parent_with_props_and_children(self):
        # Create leaf nodes (children)
        leaf1 = LeafNode("b", "bold text")
        leaf2 = LeafNode("i", "italic text", {"class": "highlight"})
        leaf3 = LeafNode("a", "click me", {"href": "https://example.com"})

        # Create a nested parent node as one of the children
        nested_parent = ParentNode(
            "span",
            [LeafNode("em", "nested emphasis")],
            {"style": "color: blue;"}
        )

        # Create the main parent node with props
        parent = ParentNode(
            "div",
            [leaf1, leaf2, nested_parent, leaf3],
            {"class": "container", "id": "main"}
        )

        # Expected HTML output (props in any order, but usually alphabetical or insertion order)
        # Note: props_to_html() adds space before each prop and rstrip() removes trailing space
        expected = (
            '<div class="container" id="main">'
            '<b>bold text</b>'
            '<i class="highlight">italic text</i>'
            '<span style="color: blue;"><em>nested emphasis</em></span>'
            '<a href="https://example.com">click me</a>'
            '</div>'
        )

        actual = parent.to_html()

        self.assertEqual(
            actual,
            expected,
            f"ParentNode.to_html() mismatch with props and children\n"
            f"Actual:   {actual!r}\n"
            f"Expected: {expected!r}"
        )

    def test_parent_no_children_raises_error(self):
        # ParentNode requires children
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "children are required")

    def test_parent_no_tag_raises_error(self):
        child = LeafNode("span", "child")
        with self.assertRaises(ValueError) as cm:
            ParentNode(None, [child]).to_html()
        self.assertEqual(str(cm.exception), "tag is required")

    def test_parent_with_empty_children_raises_error(self):
        # Empty list is not allowed
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", []).to_html()
        self.assertEqual(str(cm.exception), "children are required")


    def test_parent_with_props_but_no_children_raises_error(self):
        with self.assertRaises(ValueError) as cm:
            ParentNode("div", [], {"class": "empty"}).to_html()
        self.assertEqual(str(cm.exception), "children are required")

    def test_parent_deeply_nested(self):
        deepest = LeafNode("span", "deep")
        level3 = ParentNode("div", [deepest])
        level2 = ParentNode("section", [level3])
        level1 = ParentNode("article", [level2])
        
        expected = "<article><section><div><span>deep</span></div></section></article>"
        self.assertEqual(level1.to_html(), expected)