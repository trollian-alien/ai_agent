import os
from dotenv import load_dotenv
from google import genai
from google.genai import types

def write_file(working_directory, file_path, content):
    if type(content) != str:
        return f'Error: content must be a string'
    full_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not full_file_path.startswith(os.path.abspath(working_directory)+ os.sep):
        return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'
    
    parent_dir = os.path.dirname(full_file_path)
    try: 
        os.makedirs(parent_dir, exist_ok = True)
        with open(full_file_path, "w") as f:
            f.write(content)
        
    except Exception as e:
        return f'Error: {e}'
    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'

schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes specified content in a file. If the file does not exist, also create said file, constrained to the working directory",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "content": types.Schema(
                type=types.Type.STRING,
                description="the content to be added to the file",
            ),
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="The path of the file to write on, relative to the working directory. Creates the file if it does not exist.",
            ),
        },
    ),
)