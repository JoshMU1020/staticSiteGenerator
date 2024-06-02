import unittest
from textnode import TextNode
from htmlnode import LeafNode
from converter import *

from textnode import (
    TextNode,
    text_type_text,
    text_type_bold,
    text_type_italic,
    text_type_code,
    text_type_image,
    text_type_link,
)

class TestConverterNode(unittest.TestCase):
    def test_converter(self):
        test_cases = [
            TextNode("Simple text", "text"),
            TextNode("Bold text", "bold"),
            TextNode("Italic text", "italic"),
            TextNode("print('Hello, world!')", "code"),
            TextNode("Google", "link", "https://www.google.com"),
            TextNode("An image", "img", "https://example.com/image.jpg")
        ]
        
        for i, text_node in enumerate(test_cases):
            if i == 0:
                expected = LeafNode(None, text_node.text)
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
            elif i == 1:
                expected = LeafNode("b", text_node.text)
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
            elif i == 2:
                expected = LeafNode("i", text_node.text)
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
            elif i == 3:
                expected = LeafNode("code", text_node.text)
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
            elif i == 4:
                expected = LeafNode("a", text_node.text, {"href": text_node.url})
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
            elif i == 5:
                expected = LeafNode("img", "", {"src":text_node.url, "alt": text_node.text})
                actual = text_node_to_html_node(text_node)
                self.assertEqual(expected, actual)
    
    def test_split(self):
        types = {
            "text_type_text": "text",
            "text_type_bold": "bold",
            "text_type_italic": "italic",
            "text_type_code": "code",
        }

        node = TextNode("This is text with a `code block` word", types["text_type_text"])
        expected = [
            TextNode("This is text with a ", types["text_type_text"]),
            TextNode("code block", types["text_type_code"]),
            TextNode(" word", types["text_type_text"]),
        ]
        actual = split_nodes_delimiter([node], "`", types["text_type_code"])
        self.assertEqual(expected, actual)

        node = TextNode("This is text with a **bold block** word", types["text_type_text"])
        expected = [
            TextNode("This is text with a ", types["text_type_text"]),
            TextNode("bold block", types["text_type_bold"]),
            TextNode(" word", types["text_type_text"]),
        ]
        actual = split_nodes_delimiter([node], "**", types["text_type_bold"])
        self.assertEqual(expected, actual)

        node = TextNode("This is text with a *italic block* word", types["text_type_text"])
        expected = [
            TextNode("This is text with a ", types["text_type_text"]),
            TextNode("italic block", types["text_type_italic"]),
            TextNode(" word", types["text_type_text"]),
        ]
        actual = split_nodes_delimiter([node], "*", types["text_type_italic"])
        self.assertEqual(expected, actual)

        node = TextNode("`This` is text with a `code block` word", types["text_type_text"])
        expected = [
            TextNode("This", types["text_type_code"]),
            TextNode(" is text with a ", types["text_type_text"]),
            TextNode("code block", types["text_type_code"]),
            TextNode(" word", types["text_type_text"]),
        ]
        actual = split_nodes_delimiter([node], "`", types["text_type_code"])
        self.assertEqual(expected, actual)

        node = TextNode("This is text with a code block` word", types["text_type_text"])
        with self.assertRaises(Exception):
            actual = split_nodes_delimiter([node], "`", types["text_type_code"])

        node = TextNode("`This` is text with a `code `block` word", types["text_type_text"])
        with self.assertRaises(Exception):
            actual = split_nodes_delimiter([node], "`", types["text_type_code"])

    def test_re(self):

        text = "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and ![another](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png)"
        expected = [("image", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"), ("another", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/dfsdkjfd.png")]
        actual = extract_markdown_images(text)
        self.assertEqual(expected, actual)

        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        expected = [("link", "https://www.example.com"), ("another", "https://www.example.com/another")]
        actual = extract_markdown_links(text)
        self.assertEqual(expected, actual)

    def test_split_img(self):
        node = TextNode(
            "This is text with an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
                        TextNode("This is text with an ", "text"),
                        TextNode("image", "img", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and another ", "text"),
                        TextNode("second image", "img", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                    ]
        actual = split_nodes_image([node])
        self.assertEqual(expected, actual)

        node = TextNode(
            "![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another ![second image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
                        TextNode("image", "img", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and another ", "text"),
                        TextNode("second image", "img", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                    ]
        actual = split_nodes_image([node])
        self.assertEqual(expected, actual)

    def test_split_link(self):
        node = TextNode(
            "This is text with an [link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
                        TextNode("This is text with an ", "text"),
                        TextNode("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and another ", "text"),
                        TextNode("second link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                    ]
        actual = split_nodes_link([node])
        self.assertEqual(expected, actual)

        node = TextNode(
            "[link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and another [second link](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png)",
            "text",
        )
        expected = [
                        TextNode("link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and another ", "text"),
                        TextNode("second link", "link", "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/3elNhQu.png"),
                    ]
        actual = split_nodes_link([node])
        self.assertEqual(expected, actual)

    def test_text_to_textnode(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![image](https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png) and a [link](https://boot.dev)"
        expected = [
                        TextNode("This is ", text_type_text),
                        TextNode("text", text_type_bold),
                        TextNode(" with an ", text_type_text),
                        TextNode("italic", text_type_italic),
                        TextNode(" word and a ", text_type_text),
                        TextNode("code block", text_type_code),
                        TextNode(" and an ", text_type_text),
                        TextNode("image", text_type_image, "https://storage.googleapis.com/qvault-webapp-dynamic-assets/course_assets/zjjcJKZ.png"),
                        TextNode(" and a ", text_type_text),
                        TextNode("link", text_type_link, "https://boot.dev"),
                    ]
        actual = text_to_textnodes(text)
        self.assertEqual(expected, actual)


if __name__ == "__main__":
    unittest.main()
    