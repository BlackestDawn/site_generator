import os
import shutil
from pathlib import Path
from block_markdown import markdown_to_html_node


last_slash = os.path.dirname(__file__).rfind("/")
base_dir = __file__[:last_slash]
static_dir = base_dir + "/static"
public_dir = base_dir + "/public"
content_dir = base_dir + "/content"


def main():
    copy_static_source()
    generate_pages_recursive(content_dir, base_dir + "/template.html", public_dir)


def copy_static_source():
    if os.path.exists(public_dir):
        shutil.rmtree(public_dir)
    shutil.copytree(static_dir, public_dir)


def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:]
    raise ValueError("Title not found")


def generate_page(from_path, template_path, dest_path):
    print(f"Generating page:\n\tsource: {from_path}\n\tdestination: {dest_path}\n\ttemplate: {template_path}")

    source_file = open(from_path, "r")
    source_content = source_file.read()
    source_file.close()
    template_file = open(template_path, "r")
    template_content = template_file.read()
    template_file.close()

    html_nodes = markdown_to_html_node(source_content)
    title_content = extract_title(source_content)
    template_content = template_content.replace("{{ Title }}", title_content)
    template_content = template_content.replace("{{ Content }}", html_nodes.to_html())

    target_dir = os.path.dirname(dest_path)
#    print(f"DEBUG:: dest dir: {target_dir}")
    Path(target_dir).mkdir(parents=True, exist_ok=True)
    target_file = open(dest_path, "w")
    target_file.write(template_content)
    target_file.close()


def generate_pages_recursive(dir_path_content, template_path, dest_dir_path):
    dir_contents = os.listdir(dir_path_content)
    for entry in dir_contents:
        if os.path.isdir(f"{dir_path_content}/{entry}"):
            generate_pages_recursive(f"{dir_path_content}/{entry}", template_path, f"{dest_dir_path}/{entry}")
        if os.path.isfile(f"{dir_path_content}/{entry}") and entry.endswith(".md"):
            generate_page(f"{dir_path_content}/{entry}", template_path, f"{dest_dir_path}/{entry.replace(".md", ".html")}")


if __name__ == "__main__":
    main()
