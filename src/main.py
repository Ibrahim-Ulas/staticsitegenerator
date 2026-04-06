import os
import shutil


dir_static = "./static"
dir_public = "./public"

def main():
        copy_all_contents(dir_static, dir_public)

def copy_all_contents(source_directory, destination_directory):
        if os.path.exists(destination_directory):
                shutil.rmtree(destination_directory)
        os.mkdir(destination_directory)
        file_list = os.listdir(source_directory)
        for file in file_list:
                full_source_path = os.path.join(source_directory, file)
                full_dest_path = os.path.join(destination_directory, file)
                if os.path.isfile(full_source_path):
                        shutil.copy(full_source_path, full_dest_path)
                else:
                        copy_all_contents(full_source_path, full_dest_path)
        return destination_directory


main()
