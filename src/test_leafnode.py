import unittest
from src.htmlnode import HTMLNode
from src.leafnode import LeafNode

class TestLeafNode(unittest.TestCase):
    def test_values_no_props(self):
        # Test that the constructor correctly assigns values
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, None)

    def test_values_props(self):
        # Test that the constructor correctly assigns values
        node = LeafNode("p", "Hello, world!",{'href':'Click Here'})
        self.assertEqual(node.tag, "p")
        self.assertEqual(node.value, "Hello, world!")
        self.assertEqual(node.children, None)
        self.assertEqual(node.props, {'href':'Click Here'})

    def test_leaf_to_html_no_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!",{'href':'google.com'})
        self.assertEqual(node.to_html(), '<p href="google.com">Hello, world!</p>')

    def test_to_html_no_value(self):
        node = LeafNode("p", None)
        # This tells the test to expect a ValueError
        with self.assertRaises(ValueError):
            node.to_html()

    def test_to_html_no_tag(self):
        node = LeafNode(None, "abc")
        # This tells the test to expect a ValueError
        self.assertEqual(node.to_html(), "abc")

    def test_repr(self):
        node = LeafNode("p", "Hello")
        expected = "Tag: p\nValue: Hello\nProps: None"
        self.assertEqual(repr(node), expected)

if __name__ == "__main__":
    unittest.main()
