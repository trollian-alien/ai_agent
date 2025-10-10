import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_files_info(working_directory, directory="."):
    directory_full_path = os.path.abspath(os.path.join(working_directory, directory))
    working_directory_full_path = os.path.abspath(working_directory)
    if not directory_full_path.startswith(working_directory_full_path):
        return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'
    if not os.path.isdir(directory_full_path):
        return f'Error: "{directory}" is not a directory'    
    
    try:
        contents = [
            f"- {x}: file_size={os.path.getsize(os.path.join(directory_full_path, x))} bytes, is_dir={os.path.isdir(os.path.join(directory_full_path, x))}"
            for x in os.listdir(directory_full_path)
        ]
    except Exception as e:
        return f"Error: {e}"
    else:
        return "\n".join(contents)
    

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in the specified directory along with their sizes, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="The directory to list files from, relative to the working directory. If not provided, lists files in the working directory itself.",
            ),
        },
    ),
)