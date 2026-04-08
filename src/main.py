import os
import shutil

from .functions import copy_all_contents, generate_pages_recursive


dir_static = "./static"
dir_public = "./public"
dest_path = "./public"
content_path = "./content"
template_path = "./template.html"


def main():
        copy_all_contents(dir_static, dir_public)
        generate_pages_recursive(content_path, template_path, dest_path)


main()
