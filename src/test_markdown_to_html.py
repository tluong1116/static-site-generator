import unittest
from src.markdown_to_html import markdown_to_html_node

class TestMarkdownToHTML(unittest.TestCase):
    def test_paragraph(self):
        md = "This is a simple paragraph."
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><p>This is a simple paragraph.</p></div>")

    def test_headings(self):
        md = "# Title\n\n## Subtitle"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><h1>Title</h1><h2>Subtitle</h2></div>")

    def test_blockquote(self):
        md = "> This is a quote"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertIn("<blockquote><p>This is a quote</p></blockquote>", html)

    def test_code_block(self):
        md = "```\nprint('hello')\n```"
        node = markdown_to_html_node(md)
        html = node.to_html()
        # Verify literal backticks/content weren't mangled
        self.assertIn("<pre><code>print('hello')\n</code></pre>", html)

    def test_lists(self):
        md = "- item 1\n- item 2"
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(html, "<div><ul><li>item 1</li><li>item 2</li></ul></div>")