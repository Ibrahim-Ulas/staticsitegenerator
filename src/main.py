import os
import shutil
import sys

from .functions import copy_all_contents, generate_pages_recursive


dir_static = "./static"
dir_public = "./docs"
dest_path = "./docs"
content_path = "./content"
template_path = "./template.html"

basepath = "/"

if len(sys.argv) > 1:
        basepath = sys.argv[1]



def main():
        copy_all_contents(dir_static, dir_public)
        generate_pages_recursive(content_path, template_path, dest_path, basepath)
main()