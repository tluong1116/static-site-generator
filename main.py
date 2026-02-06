from src.textnode import TextNode, TextType
from src.static_to_public import recursive_copy
from src.generate_page import generate_page, generate_pages_recursive
import sys
import shutil
import os

def main():
    basepath = sys.argv[1] if len(sys.argv) > 1 else "/"

    if os.path.exists("./docs"):
        shutil.rmtree("./docs")

    print("Copying static files to public directory...")
    recursive_copy('./static', './docs')
    
    print("Generating pages...")
    # This one line handles index.md, contact/index.md, and all blog posts!
    generate_pages_recursive('content/', 'template.html', 'docs/')

main()