import os
from config import MAX_CHARS
from dotenv import load_dotenv
from google import genai
from google.genai import types

def get_file_content(working_directory, file_path):
    full_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not full_file_path.startswith(os.path.abspath(working_directory)+os.sep):
        return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
    elif not os.path.isfile(full_file_path):
        return f'Error: File not found or is not a regular file: "{file_path}"'
    
    try:
        with open(full_file_path, "r") as f:
            file_content = f.read(MAX_CHARS)
            is_there_more_text = len(f.read(1))
    except Exception as e:
        return f'Error: {e}'
    
    if is_there_more_text:
        return file_content + f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
    else: 
        return file_content
    
schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description=f"Reads file content, up to {MAX_CHARS} characters, constrained to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to read, relative to the working directory.",
            ),
        },
    ),
)