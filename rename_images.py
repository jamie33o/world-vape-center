import os
import re

def format_string():
    """
    Format filenames in a specific folder.

    This function renames files in the specified folder by removing a portion
    of the filename and appending it to another part of the filename.

    The renaming is based on a specific pattern in the filenames.

    """
    folder_path = "media/vape_kits/"

    for filename in os.listdir(folder_path):
        pattern = re.compile(r'\d{6,}')
        if pattern.search(filename):
            full_path = os.path.join(folder_path, filename)
            if os.path.isfile(full_path):   
                dot_index = filename.find('.')
                hyphen_index = filename.rfind('-')
                new_name = filename[:hyphen_index] + filename[dot_index:]
                new_full_path = os.path.join(folder_path, new_name)
                if os.path.isfile(new_full_path):
                    os.remove(full_path)
                else:
                    os.rename(full_path, new_full_path)

format_string()
