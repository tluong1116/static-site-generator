import unittest
from src.htmlnode import HTMLNode
from src.parentnode import ParentNode
from src.leafnode import LeafNode

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")
    
    def test_to_html_many_children(self):
        node = ParentNode(
            "p",
            [
                LeafNode("b", "Bold text"),
                LeafNode(None, "Normal text"),
                LeafNode("i", "italic text"),
                LeafNode(None, "Normal text"),
            ],
        )
        self.assertEqual(node.to_html(), "<p><b>Bold text</b>Normal text<i>italic text</i>Normal text</p>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_headings(self):
        node = ParentNode(
            "h2",
            [
                LeafNode("b", "Bold title"),
                LeafNode(None, " and plain text"),
            ],
        )
        self.assertEqual(node.to_html(), "<h2><b>Bold title</b> and plain text</h2>")

    def test_to_html_with_props(self):
        node = ParentNode(
            "div",
            [LeafNode("span", "child")],
            {"class": "wrapper", "id": "main"}
        )
        # Note: dictionary order can vary in older Python, but usually matches input
        self.assertEqual(node.to_html(), '<div class="wrapper" id="main"><span>child</span></div>')

    def test_to_html_no_tag(self):
        # Wrap the initialization, because that's where the error is raised now
        with self.assertRaises(ValueError):
            node = ParentNode(None, [LeafNode("b", "child")])
            
    def test_to_html_no_children(self):
        with self.assertRaises(ValueError):
            node = ParentNode("div", None)

    def test_to_html_deeply_nested(self):
        # div > section > p > span > b > "deep"
        node = ParentNode(
            "div",
            [
                ParentNode(
                    "section",
                    [
                        ParentNode(
                            "p",
                            [
                                ParentNode(
                                    "span",
                                    [
                                        LeafNode("b", "deep"),
                                    ],
                                )
                            ],
                        )
                    ],
                )
            ],
        )
        expected = "<div><section><p><span><b>deep</b></span></p></section></div>"
        self.assertEqual(node.to_html(), expected)

if __name__ == "__main__":
    unittest.main()