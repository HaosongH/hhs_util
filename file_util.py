import os
import shutil
from base_operation import *
# --------------------------------------file and directory utility ------------------------------------------
# Get all files in the folder
def get_all_files(folder_path):
    # List only the files in the given folder (one level deep)
    immediate_files = [
        os.path.join(folder_path, name)
        for name in os.listdir(folder_path)
        if os.path.isfile(os.path.join(folder_path, name))
    ]
    return immediate_files

# get all subfolders in the folder
def get_all_folders(folder_path):
    immediate_folders = [
        os.path.join(folder_path, name)
        for name in os.listdir(folder_path)
        if os.path.isdir(os.path.join(folder_path, name))
    ]
    return immediate_folders

# get basename of the path, with or without extension
# For example, C:/aaa/b.jpg will return b.jpg or b
def get_base_name(path):
    return os.path.basename(path).split(".")[0]

def get_base_name(path, ext):
    if ext:
        return os.path.basename(path)
    else: 
        return os.path.basename(path).split(".")[0]

# Return all files in the directory with a specific extension
def generate_file_list(dir, end):
    list = [os.path.join(dir,f) for f in os.listdir(dir) if f.endswith(end)]
    list.sort()
    return list

def generate_file_list_multiple_ext(dir, ends):
    result = []
    for end in ends:
        list = generate_file_list(dir, end)
        result = list_union(result, list)
    return result

# Modify the structure for future use
def copy_files_ext(source_dir, target_dir, file_ext_list):
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)

    subfolders = get_all_folders(source_dir)
    for case_num_path in subfolders:
        path = os.path.join(case_num_path,"results")
        files = get_all_files(path)
        case_num = get_base_name(case_num_path)
        for file in files:
            # Check for .hdr or .dat files
            if file.endswith(file_ext_list):
                src_file = file
                dst_file = os.path.join(target_dir, case_num + os.path.splitext(file)[1])
                # return 0
                # # Copy the file to the target directory
                shutil.copy2(src_file, dst_file)
                print(f"Copied: {src_file} -> {dst_file}")

