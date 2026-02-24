from markdown_html_conversion import *
from htmlnode import *
from copier import copier
import os
import sys

def extract_title(markdown):
    split = markdown.splitlines()
    title = None
    for line in split:
        if line.startswith("# "):
            title = line.lstrip("# ")
            break
    if not title:
        raise Exception("no title found")
    return title

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    file = open(from_path, "r")
    content = file.read()
    file.close()
    temp = open(template_path, "r")
    template = temp.read()
    temp.close()
    html_node = markdown_to_html_node(content)
    html_str = html_node.to_html()
    title = extract_title(content)
    template = template.replace("{{ Title }}", title)
    template = template.replace("{{ Content }}", html_str)
    template = template.replace('href="/', f'href="{basepath}')
    template = template.replace('src="/', f'src="{basepath}')
    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
    new_file = open(dest_path, "w")
    new_file.write(template)
    new_file.close()

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    for item in os.listdir(dir_path_content):
        src_path = os.path.join(dir_path_content, item)
        dst_path = os.path.join(dest_dir_path, item)
        if not os.path.isfile(src_path):
            generate_pages_recursive(src_path, template_path, dst_path, basepath)
        else:
            generate_page(src_path, template_path, dst_path.replace(".md", ".html"), basepath)

def main():
    if sys.argv[1]:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    copier("static", "docs")
    generate_pages_recursive("content", "template.html", "docs", basepath)


if __name__ == "__main__":
    main()