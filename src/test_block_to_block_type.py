import unittest
from markdown_blocks import block_to_block_type, BlockType, markdown_to_blocks

class TestBlockToBlockType(unittest.TestCase):

    # === PASSING TESTS (one for each type) ===

    def test_paragraph(self):
        block = "This is a normal paragraph.\nIt can have multiple lines."
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_level_1(self):
        block = "# Main Title"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_heading_level_6(self):
        block = "###### Smallest heading"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_codeblock(self):
        block = "```\ncode here\nmore code\n```"
        self.assertEqual(block_to_block_type(block), BlockType.CODEBLOCK)

    def test_quote_single_line(self):
        block = "> This is a quote."
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_quote_multi_line(self):
        block = "> First line of quote\n> Second line"
        self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_unordered_list(self):
        block = "- Item one\n- Item two\n- Item three"
        self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_ordered_list(self):
        block = "1. First\n2. Second\n3. Third"
        self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    # === FAILURE / EDGE CASES (should return PARAGRAPH) ===

    def test_heading_no_space_after_hash(self):
        block = "#No space after hash"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_heading_too_many_hashes(self):
        block = "####### Seven hashes"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_codeblock_no_closing(self):
        block = "```\ncode here\nno closing"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_codeblock_closing_with_extra_text(self):
        block = "```\ncode\n``` extra"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_quote_not_all_lines_start_with_gt(self):
        block = "> First line\nSecond line without >"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_unordered_list_inconsistent(self):
        block = "- First\n* Second (wrong bullet)"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_wrong_numbering(self):
        block = "1. First\n3. Skipped two"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_ordered_list_starts_at_two(self):
        block = "2. Starts at two\n3. Three"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_empty_block(self):
        block = ""
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_just_hashes(self):
        block = "###"
        self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_mixed_markdown(self):
        block = "# Heading\n> Quote\n- List"
        self.assertEqual(block_to_block_type(block), BlockType.HEADING)