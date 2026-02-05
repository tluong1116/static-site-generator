import unittest
from src.textnode import TextNode, TextType
from src.inline_markdown import (split_nodes_delimiter, extract_markdown_images, 
                                 extract_markdown_links, split_nodes_image, split_nodes_link,
                                 text_to_textnodes)

class TestSplitInlineDelimiter(unittest.TestCase):
    def test_split_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "This is text with a ")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)
        self.assertEqual(new_nodes[1].text, "code block")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[2].text, " word")
        self.assertEqual(new_nodes[2].text_type, TextType.TEXT)

    def test_split_bold(self):
        node = TextNode("I am **very bold** today", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "very bold")
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_italic(self):
        node = TextNode("Italicized *word* in a sentence", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "word")
        self.assertEqual(new_nodes[1].text_type, TextType.ITALIC)

    def test_no_delimiters(self):
        node = TextNode("Just a plain old sentence.", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just a plain old sentence.")
        self.assertEqual(new_nodes[0].text_type, TextType.TEXT)

    def test_no_closing_delimiter(self):
        node = TextNode("This is `invalid code", TextType.TEXT)
        with self.assertRaises(ValueError):
            split_nodes_delimiter([node], "`", TextType.CODE)

    def test_mixed_nodes(self):
        nodes = [
            TextNode("raw", TextType.TEXT),
            TextNode("already bold", TextType.BOLD)
        ]
        # If we split by something not present, it should just return the same nodes
        new_nodes = split_nodes_delimiter(nodes, "`", TextType.CODE)
        self.assertEqual(len(new_nodes), 2)

    def test_multiple_inline_code(self):
        node = TextNode("Check `this` and `that` out", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        
        # Expectation: [TEXT, CODE, TEXT, CODE, TEXT]
        self.assertEqual(len(new_nodes), 5)
        self.assertEqual(new_nodes[1].text, "this")
        self.assertEqual(new_nodes[1].text_type, TextType.CODE)
        self.assertEqual(new_nodes[3].text, "that")
        self.assertEqual(new_nodes[3].text_type, TextType.CODE)

class TestExtractMarkdown(unittest.TestCase):
    def test_extract_markdown_images(self):
        text = "This is text with an ![image](https://i.imgur.com/zcewU2n.png) and ![another](https://i.imgur.com/3sW7L91.png)"
        matches = extract_markdown_images(text)
        self.assertListEqual(
            [
                ("image", "https://i.imgur.com/zcewU2n.png"),
                ("another", "https://i.imgur.com/3sW7L91.png"),
            ],
            matches,
        )

    def test_extract_markdown_links(self):
        text = "This is text with a [link](https://www.example.com) and [another](https://www.example.com/another)"
        matches = extract_markdown_links(text)
        self.assertListEqual(
            [
                ("link", "https://www.example.com"),
                ("another", "https://www.example.com/another"),
            ],
            matches,
        )

    def test_extract_none(self):
        text = "This is just plain text with no images or links."
        images = extract_markdown_images(text)
        links = extract_markdown_links(text)
        self.assertEqual(len(images), 0)
        self.assertEqual(len(links), 0)

    def test_extract_markdown_images_simple(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

class TestSplitImages(unittest.TestCase):
    def test_split_image(self):
        # Scenario: Single image in the middle of text
        node = TextNode("Text ![img](url) more text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text_type, TextType.IMAGE)

    def test_split_images_multiple(self):
        # Scenario: Multiple images
        node = TextNode("![i1](u1) middle ![i2](u2)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text, "i1")
        self.assertEqual(new_nodes[2].text, "i2")

    def test_split_images_no_images(self):
        # Scenario: Plain text with no image markdown
        node = TextNode("Just plain text", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "Just plain text")

    def test_split_images_at_start(self):
        # Scenario: Image is the very first thing in the string
        node = TextNode("![only](url) text follows", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text_type, TextType.IMAGE)

    def test_split_images_only_image(self):
        # Scenario: The entire text is just one image
        node = TextNode("![alone](url)", TextType.TEXT)
        new_nodes = split_nodes_image([node])
        self.assertEqual(len(new_nodes), 1)
        self.assertEqual(new_nodes[0].text, "alone")

class TestSplitLinks(unittest.TestCase):
    def test_split_link(self):
        # Scenario: Basic single link
        node = TextNode("Check [boot dev](https://www.boot.dev) out", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[1].text, "boot dev")
        self.assertEqual(new_nodes[1].url, "https://www.boot.dev")

    def test_split_links_multiple(self):
        # Scenario: Two links separated by text
        node = TextNode("[first](u1) and [second](u2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 3)
        self.assertEqual(new_nodes[0].text_type, TextType.LINK)
        self.assertEqual(new_nodes[2].text_type, TextType.LINK)

    def test_split_links_consecutive(self):
        # Scenario: Two links with no text between them
        node = TextNode("[one](u1)[two](u2)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[0].text, "one")
        self.assertEqual(new_nodes[1].text, "two")

    def test_split_links_mixed_types(self):
        # Scenario: List contains both a TEXT node and a BOLD node
        # The BOLD node should be ignored and passed through as-is
        nodes = [
            TextNode("[link](url)", TextType.TEXT),
            TextNode("already bold", TextType.BOLD)
        ]
        new_nodes = split_nodes_link(nodes)
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[1].text_type, TextType.BOLD)

    def test_split_link_at_end(self):
        # Scenario: Link is at the very end of the text
        node = TextNode("Follow me [here](url)", TextType.TEXT)
        new_nodes = split_nodes_link([node])
        self.assertEqual(len(new_nodes), 2)
        self.assertEqual(new_nodes[1].text_type, TextType.LINK)

class TestTextToTextNodes(unittest.TestCase):
    def test_text_to_textnodes(self):
        text = "This is **text** with an _italic_ word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        nodes = text_to_textnodes(text)
        self.assertListEqual(
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
            nodes,
        )

if __name__ == "__main__":
    unittest.main()