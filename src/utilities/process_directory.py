# import os
# import shutil


# class ProcessDirectory:
#     def __init__(self):
#         pass

#     def create_directory(self, directory_path: str):
#         """
#             Create a directory if it does not exist.

#             Parameters:
#                 directory_path (str): The path of the directory to be created.
#         """
#         if not os.path.exists(directory_path):
#             os.makedirs(directory_path)
            
#     def remove_directory(self, directory_path: str):
#         """
#             Removes the specified directory.

#             Parameters:
#                 directory_path (str): The path of the directory to be removed.

#             Raises:
#                 OSError: If an error occurs during the directory removal process.

#             Returns:
#                 None
#         """
#         if os.path.exists(directory_path):
#             try:
#                 shutil.rmtree(directory_path)
#                 print(
#                         f"The directory '{directory_path}' has been successfully removed.")
#             except OSError as e:
#                 print(f"Error: {e}")
#         else:
#             print(f"The directory '{directory_path}' does not exist.")
        