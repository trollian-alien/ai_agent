import os

def get_files_info(working_directory, directory="."):
    directory_full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_full_path = os.path.abspath(working_directory)
    if os.path.isdir(directory_full_path) == False:
        return f'Error: "{directory}" is not a directory'
    if not directory_full_path.startswith(working_directory_full_path+os.sep):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    
    try:
        contents = [
            f"- {x}: file_size={os.path.getsize(os.path.join(directory_full_path, x))} bytes, is_dir={os.path.isdir(os.path.join(directory_full_path, x))}"
            for x in os.listdir(directory_full_path)
        ]
    except Exception as e:
        return f"Error: {e}"
    else:
        return "\n".join(contents)