import os
from pathlib import Path
from src.markdown_to_html import markdown_to_html_node
from src.block_markdown import extract_title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path}")
    # Read files
    with open(from_path,'r',encoding="utf-8") as f:
        from_markdown = f.read()
    with open(template_path,'r',encoding="utf-8") as f:
        template = f.read()

    content = markdown_to_html_node(from_markdown).to_html()
    title = extract_title(from_markdown)

    final_html = (template.
                    replace("{{ Title }}", title).
                    replace("{{ Content }}", content).
                    replace('href="/',f'href="{basepath}').
                    replace('src="/',f'src="{basepath}'))
    

    # Make sure destination dir exists
    dest_dir = os.path.dirname(dest_path)
    if dest_dir != "":
        os.makedirs(dest_dir, exist_ok=True)

    with open(dest_path, "w",encoding="utf-8") as f:
        f.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path,basepath):
    print(f"Generating page from {dir_path_content} to {dest_dir_path}")
    # Iterate over all entries in the content directory
    for filename in os.listdir(dir_path_content):
        from_path = os.path.join(dir_path_content, filename)
        dest_path = os.path.join(dest_dir_path, filename)

        # Case 1: It's a file - check if it's markdown
        if os.path.isfile(from_path):
            if filename.endswith(".md"):
                # Change the destination extension to .html
                dest_html_path = Path(dest_path).with_suffix(".html")
                # Call your existing generate_page function
                generate_page(from_path, template_path, dest_html_path,basepath)
        
        # Case 2: It's a directory - recurse!
        else:
            generate_pages_recursive(from_path, template_path, dest_path,basepath)
        


    