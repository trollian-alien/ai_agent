import os, subprocess

def run_python_file(working_directory, file_path, args=[]):

    full_file_path = os.path.abspath(os.path.join(working_directory,file_path))
    if not full_file_path.startswith(os.path.abspath(working_directory)+ os.sep):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
    elif not os.path.exists(full_file_path):
        return f'Error: File "{file_path}" not found.'
    elif not full_file_path.endswith(".py"):
        return f'Error: "{file_path}" is not a Python file.'
    
    a = ["python", full_file_path] + args
    try:
        completed_process = subprocess.run( a, stdout = subprocess.PIPE, stderr = subprocess.PIPE, text = True,timeout = 30, cwd=working_directory)
    except Exception as e:
        return f"Error: {e}"
    
    if completed_process.stdout != "":
        the_stdout = f"STDOUT: {completed_process.stdout}"
    else:
        the_stdout = "No output detected"
    the_stderr = f"STDERR: {completed_process.stderr}"
    if completed_process.returncode == 0:
        return_code = ""
    else: 
        return_code = f"Process exited with code {completed_process.returncode}"

    return "\n".join([the_stdout,the_stderr,return_code])
