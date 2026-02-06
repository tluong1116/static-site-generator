from src.textnode import TextNode, TextType
from src.static_to_public import recursive_copy
from src.generate_page import generate_page, generate_pages_recursive

def main():

    print("Copying static files to public directory...")
    recursive_copy('./static', './public')
    
    print("Generating pages...")
    # This one line handles index.md, contact/index.md, and all blog posts!
    generate_pages_recursive('content/', 'template.html', 'public/')

main()