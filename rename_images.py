# import os

# def remove_numbers_from_filename(filename):
#     # name, extension = os.path.splitext(filename)
#     name, extension = os.path.splitext(filename)

#     # Find the last occurrence of hyphen ('-') and remove everything after it
#     cleaned_name  = name.rsplit('-', 1)[0]
#     cleaned_filename = f"{cleaned_name}{extension}"

#     return cleaned_filename

# def rename_files_in_folder(folder_path):
#     # Iterate through all files in the folder
#     for filename in os.listdir(folder_path):
#         # Construct the full path to the file
#         full_path = os.path.join(folder_path, filename)

#         # Check if it is a file (not a directory)
#         if os.path.isfile(full_path):
#             # Get the cleaned filename
#             cleaned_filename = remove_numbers_from_filename(filename)

#             # Construct the full path for the new filename
#             new_full_path = os.path.join(folder_path, cleaned_filename)

#             # Rename the file
#             os.rename(full_path, new_full_path)

# # Example usage
# folder_path = "media/"
# rename_files_in_folder(folder_path)


import os

def add_extension_to_filename(filename, new_extension):
    # Add the new extension to the filename
    filename_with_extension = f"{filename}.{new_extension}"
    return filename_with_extension

def add_extension_to_files_in_folder(folder_path, new_extension):
    # Iterate through all files in the folder
    for filename in os.listdir(folder_path):
        # Construct the full path to the file
        full_path = os.path.join(folder_path, filename)

        # Check if it is a file (not a directory)
        if os.path.isfile(full_path):
            # Get the new filename with the added extension
            new_filename = add_extension_to_filename(filename, new_extension)

            # Construct the full path for the new filename
            new_full_path = os.path.join(folder_path, new_filename)

            # Rename the file
            os.rename(full_path, new_full_path)

# Example usage
folder_path = "media"
new_extension = "avif"  # Replace with your desired extension
add_extension_to_files_in_folder(folder_path, new_extension)
