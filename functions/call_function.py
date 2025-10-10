from google.genai import types
from functions.get_files_info import get_files_info
from functions.get_files_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file

apply_func = {
    "get_files_info": get_files_info,
    "get_file_content": get_file_content,
    "write_file": write_file,
    "run_python_file": run_python_file
}

def call_function(function_call_part, verbose=False):
    if verbose:
        print(f"Calling function: {function_call_part.name}({function_call_part.args})")
    else:
        print(f" - Calling function: {function_call_part.name}")
    
    function_name = function_call_part.name
    if function_name not in apply_func:
        return types.Content(
            role="tool",
            parts=[
                types.Part.from_function_response(
                    name=function_name,
                    response={"error": f"Unknown function: {function_name}"},
                )
            ],
        )
    merged_args = dict(function_call_part.args)
    merged_args["working_directory"] = "./calculator"
    result = apply_func[function_name](**merged_args)
    return types.Content(
        role="tool",
        parts=[
            types.Part.from_function_response(
                name=function_name,
                response={"result": result},
                )
            ],
        )