import unittest
from src.textnode import (
    TextNode, 
    TextType, 
    text_node_to_html_node
)


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_false(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.ITALIC)
        self.assertNotEqual(node, node2)

    def test_eq_false2(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a different text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_repr(self):
        node = TextNode("This is a text node", TextType.TEXT, "https://www.boot.dev")
        self.assertEqual(
            "TextNode(This is a text node, normal text, https://www.boot.dev)", repr(node)
        )

class TestTextNodeToHTMLNode(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_image(self):
        node = TextNode("This is alt text", TextType.IMAGE, "https://www.google.com/image.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, "")
        self.assertEqual(
            html_node.props,
            {"src": "https://www.google.com/image.png", "alt": "This is alt text"},
        )

    def test_bold(self):
        node = TextNode("This is bold", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is bold")

# class TestSplitInlineDelimiter(unittest.TestCase):
#     def test_split_code(self):
#         node = TextNode("This is text with a `code block` word", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#         self.assertEqual(len(new_nodes), 3)
#         self.assertEqual(new_nodes[0].text, "This is text with a ")
#         self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
#         self.assertEqual(new_nodes[1].text, "code block")
#         self.assertEqual(new_nodes[1].text_type, TextType.CODE)
#         self.assertEqual(new_nodes[2].text, " word")
#         self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

#     def test_split_bold(self):
#         node = TextNode("I am **very bold** today", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
#         self.assertEqual(len(new_nodes), 3)
#         self.assertEqual(new_nodes[1].text, "very bold")
#         self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

#     def test_split_italic(self):
#         node = TextNode("Italicized *word* in a sentence", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
#         self.assertEqual(len(new_nodes), 3)
#         self.assertEqual(new_nodes[1].text, "word")
#         self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

#     def test_no_delimiters(self):
#         node = TextNode("Just a plain old sentence.", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
#         self.assertEqual(len(new_nodes), 1)
#         self.assertEqual(new_nodes[0].text, "Just a plain old sentence.")
#         self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

#     def test_no_closing_delimiter(self):
#         node = TextNode("This is `invalid code", TextType.TEXT)
#         with self.assertRaises(ValueError):
#             split_nodes_delimiter([node], "`", TextType.CODE)

#     def test_mixed_nodes(self):
#         nodes = [
#             TextNode("raw", TextType.TEXT),
#             TextNode("already bold", TextType.BOLD)
#         ]
#         # If we split by something not present, it should just return the same nodes
#         new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
#         self.assertEqual(len(new_nodes), 2)

#     def test_multiple_inline_code(self):
#         node = TextNode("Check `this` and `that` out", TextType.TEXT)
#         new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
#         # Expectation: [TEXT, CODE, TEXT, CODE, TEXT]
#         self.assertEqual(len(new_nodes), 5)
#         self.assertEqual(new_nodes[1].text, "this")
#         self.assertEqual(new_nodes[1].text_type, TextType.CODE)
#         self.assertEqual(new_nodes[3].text, "that")
#         self.assertEqual(new_nodes[3].text_type, TextType.CODE)

# class TestExtractMarkdown(unittest.TestCase):
#     def test_extract_markdown_images(self):
#         text = "This is text with an ![image](https://i.imgur.com/zcewU2n.png) and ![another](https://i.imgur.com/3sW7L91.png)"
#         matches = extract_markdown_images(text)
#         self.assertListEqual(
#             [
#                 ("image", "https://i.imgur.com/zcewU2n.png"),
#                 ("another", "https://i.imgur.com/3sW7L91.png"),
#             ],
#             matches,
#         )

#     def test_extract_markdown_links(self):
#         text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
#         matches = extract_markdown_links(text)
#         self.assertListEqual(
#             [
#                 ("link", "https://www.example.com"),
#                 ("another", "https://www.example.com/another"),
#             ],
#             matches,
#         )

#     def test_extract_none(self):
#         text = "This is just plain text with no images or links."
#         images = extract_markdown_images(text)
#         links = extract_markdown_links(text)
#         self.assertEqual(len(images), 0)
#         self.assertEqual(len(links), 0)

#     def test_extract_markdown_images_simple(self):
#         matches = extract_markdown_images(
#             "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
#         )
#         self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()