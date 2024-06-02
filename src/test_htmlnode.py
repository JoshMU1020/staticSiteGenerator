import unittest
from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode("a", None, None, {"href": "https://www.google.com", "target": "_blank"})
        expected = " href=\"https://www.google.com\" target=\"_blank\""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)

        node = HTMLNode("a", None, None, None)
        expected = ""
        actual = node.props_to_html()
        self.assertEqual(expected, actual)

class TestLeafNode(unittest.TestCase):
    def test_to_html(self):
        node = LeafNode("p", "This is a paragraph of text.")
        expected = "<p>This is a paragraph of text.</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        expected = "<a href=\"https://www.google.com\">Click me!</a>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = LeafNode("a", None, {"href": "https://www.google.com"})
        self.assertRaises(ValueError, node.to_html)

        node = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        expected = "Click me!"
        actual = node.value
        self.assertEqual(expected, actual)


class TestParentNode(unittest.TestCase):
    def test_to_html(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                    ],
                )
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
                ParentNode(
                    "p",
                    [
                        LeafNode("b", "Bold text"),
                        LeafNode(None, "Normal text"),
                        LeafNode("i", "italic text"),
                        LeafNode(None, "Normal text"),
                        ParentNode(
                            "p",
                            [
                                LeafNode("b", "Bold text"),
                                LeafNode(None, "Normal text"),
                                LeafNode("i", "italic text"),
                                LeafNode(None, "Normal text"),
                                ParentNode(
                                    "p",
                                    [
                                        LeafNode("b", "Bold text"),
                                        LeafNode(None, "Normal text"),
                                        LeafNode("i", "italic text"),
                                        LeafNode(None, "Normal text"),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p></p></p></p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            None,
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode(
            "p",
            None,
        )
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode(
            "p",
            [],
        )
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
            ],
        )
        expected = "<p><b>Bold text</b></p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode(None, "Bold text"),
            ],
        )
        expected = "<p>Bold text</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode(None, None),
            ],
        )
        self.assertRaises(ValueError, node.to_html)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Click me!", {"href": "https://www.google.com"})
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i>Click me!</p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            ],
        )
        expected = "<p><b>Bold text</b>Normal text<i>italic text</i><a href=\"https://www.google.com\">Click me!</a></p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode("a", "Click me!", {"href": "https://www.google.com"})
            ],
            {"href": "https://www.google.com"},
        )
        expected = "<p href=\"https://www.google.com\"><b>Bold text</b>Normal text<i>italic text</i><a href=\"https://www.google.com\">Click me!</a></p>"
        actual = node.to_html()
        self.assertEqual(expected, actual)

if __name__ == "__main__":
    unittest.main()