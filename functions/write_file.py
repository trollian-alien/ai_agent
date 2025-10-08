import os

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