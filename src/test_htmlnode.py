import unittest
from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        # Test that props are converted to the correct HTML string format
        node = HTMLNode(
            "a", 
            "Click me!", 
            None, 
            {"href": "https://www.google.com", "target": "_blank"}
        )
        self.assertEqual(
            node.props_to_html(), 
            ' href="https://www.google.com" target="_blank"'
        )

    def test_values(self):
        # Test that the constructor correctly assigns values
        node = HTMLNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_props_to_html_none(self):
        # Test that an empty string is returned when props is None
        node = HTMLNode("p", "Just text, no props", None, None)
        self.assertEqual(node.props_to_html(), "")

    def test_to_html_children(self):
        # Test that children are correctly assigned as a list of nodes
        child_node = HTMLNode("span", "child")
        parent_node = HTMLNode("div", None, [child_node])
        self.assertEqual(parent_node.children, [child_node])