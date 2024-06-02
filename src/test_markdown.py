# Developer's Note: the far half of the test cases were not original, instead being taken from another source.
import unittest
from markdown import *
from markdown import (
    markdown_to_html_node,
    markdown_to_blocks,
    block_to_block_type,
    block_type_paragraph,
    block_type_heading,
    block_type_code,
    block_type_ordered_list,
    block_type_unordered_list,
    block_type_quote,
)

class TestCMarkdown(unittest.TestCase):
    def test_markdown_to_block(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item
"""
        expected = ['# This is a heading', 
                    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                    '* This is a list item\n* This is another list item']
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)

        markdown = """This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected = ['This is **bolded** paragraph', 
                    'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line', 
                    '* This is a list\n* with items']
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)

        markdown = """     # This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is a list item
* This is another list item      
"""
        expected = ['# This is a heading', 
                    'This is a paragraph of text. It has some **bold** and *italic* words inside of it.', 
                    '* This is a list item\n* This is another list item']
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)

        markdown = """
        
        
        
               This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        expected = ['This is **bolded** paragraph', 
                    'This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line', 
                    '* This is a list\n* with items']
        actual = markdown_to_blocks(markdown)
        self.assertEqual(expected, actual)

    def test_block_to_type(self):
        block = "# Heading Level 1"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = "## Heading Level 2"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = "### Heading Level 3"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = "#### Heading Level 4"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = "##### Heading Level 5"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = "###### Heading Level 6"
        expected = block_type_heading
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """```def example_function():
print("This is a code block")```"""
        expected = block_type_code
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """> This is a quote block.
> Every line in a quote block must start with a `>` character.
> It can span multiple lines if each starts with `>`."""
        expected = block_type_quote
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """* Item 1 in unordered list
* Item 2 in unordered list
* Item 3 in unordered list"""
        expected = block_type_unordered_list
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """- Another item in unordered list
- Yet another item in unordered list"""
        expected = block_type_unordered_list
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """1. First item in ordered list
2. Second item in ordered list
3. Third item in ordered list"""
        expected = block_type_ordered_list
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """This is a normal paragraph block. 
If none of the above conditions are met, the block should be treated as a paragraph.

It can contain multiple lines.

Just like this."""
        expected = block_type_paragraph
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        block = """1. First item in ordered list
4. Second item in ordered list
3. Third item in ordered list"""
        expected = block_type_paragraph
        actual = block_to_block_type(block)
        self.assertEqual(expected, actual)

        md = """
This is **bolded** paragraph

This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_markdown_to_blocks_newlines(self):
        md = """
This is **bolded** paragraph




This is another paragraph with *italic* text and `code` here
This is the same paragraph on a new line

* This is a list
* with items
"""
        blocks = markdown_to_blocks(md)
        self.assertEqual(
            blocks,
            [
                "This is **bolded** paragraph",
                "This is another paragraph with *italic* text and `code` here\nThis is the same paragraph on a new line",
                "* This is a list\n* with items",
            ],
        )

    def test_block_to_block_types(self):
        block = "# heading"
        self.assertEqual(block_to_block_type(block), block_type_heading)
        block = "```\ncode\n```"
        self.assertEqual(block_to_block_type(block), block_type_code)
        block = "> quote\n> more quote"
        self.assertEqual(block_to_block_type(block), block_type_quote)
        block = "* list\n* items"
        self.assertEqual(block_to_block_type(block), block_type_unordered_list)
        block = "1. list\n2. items"
        self.assertEqual(block_to_block_type(block), block_type_ordered_list)
        block = "paragraph"
        self.assertEqual(block_to_block_type(block), block_type_paragraph)

    def test_paragraph(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p></div>",
        )

    def test_paragraphs(self):
        md = """
This is **bolded** paragraph
text in a p
tag here

This is another paragraph with *italic* text and `code` here

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )

    def test_lists(self):
        md = """
- This is a list
- with items
- and *more* items

1. This is an `ordered` list
2. with items
3. and more items

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ul><li>This is a list</li><li>with items</li><li>and <i>more</i> items</li></ul><ol><li>This is an <code>ordered</code> list</li><li>with items</li><li>and more items</li></ol></div>",
        )

    def test_headings(self):
        md = """
# this is an h1

this is paragraph text

## this is an h2
"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>this is an h1</h1><p>this is paragraph text</p><h2>this is an h2</h2></div>",
        )

    def test_blockquote(self):
        md = """
> This is a
> blockquote block

this is paragraph text

"""

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a blockquote block</blockquote><p>this is paragraph text</p></div>",
        )


if __name__ == "__main__":
    unittest.main()

    