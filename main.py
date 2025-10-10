import os, sys
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.get_files_info import schema_get_files_info
from functions.get_files_content import schema_get_file_content
from functions.write_file import schema_write_file
from functions.run_python import schema_run_python_file
from functions.call_function import call_function
import time
from google.genai.errors import ClientError

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
print("API key present:", bool(api_key))

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")
    if len(sys.argv) < 2:
        print("Error, no prompt provided. Usage: python3 main.py your_prompt")
        sys.exit(1)

    user_prompt = " ".join(sys.argv[1:])
    system_prompt = """
    You are a helpful AI coding agent.

    When a user asks a question or makes a request, make a function call plan. You can perform the following operations:

    - List files and directories
    - Read file contents
    - Execute Python files with optional arguments
    - Write or overwrite files

    All paths you provide should be relative to the working directory. You do not need to specify the working directory in your function calls as it is automatically injected for security reasons.
    """

    available_functions = types.Tool(
        function_declarations=[
            schema_get_files_info,
            schema_get_file_content,
            schema_run_python_file,
            schema_write_file
        ]
    )

    messages = [
    types.Content(role="user", parts=[types.Part(text=user_prompt)]),
    ]

    for _ in range(0,20):
        try:
            try:
                response = client.models.generate_content(
                model='gemini-2.0-flash-001', 
                contents=messages,
                config=types.GenerateContentConfig(
                    tools=[available_functions], system_instruction=system_prompt
                    )
                )
            except ClientError as e:
                # handle 429 with exponential backoff
                if "RESOURCE_EXHAUSTED" in str(e):
                    delay = min(30, 2 ** _)  # cap the wait
                    time.sleep(delay)
                    continue
                else:
                    raise

            if response.candidates:
                for candidate in response.candidates:
                    if candidate and candidate.content:
                        messages.append(candidate.content) 

            usage = response.usage_metadata
            verbose = False
            if sys.argv[-1] == "--verbose":
                print(f"User prompt: {user_prompt}")
                print(f"Prompt tokens: {usage.prompt_token_count}")
                print(f"Response tokens: {usage.candidates_token_count}")
                verbose = True
            # print(f"Calling function: {response.function_calls.name}({response.function_calls.args})")
            
            if response.function_calls:
                fc = response.function_calls[0]
                print(f"Calling function: {fc.name}({fc.args})")
                
                function_call_result = call_function(fc, verbose)
                print(type(function_call_result))
                tool_part = function_call_result.parts[0]  # contains function_response
                messages.append(
                    types.Content(role="user", parts=[tool_part])
                )
                print(f"-> {tool_part.function_response.response}")
                    
                if not response.function_calls and response.text:
                    print("Final response:")
                    print(response.text)
                    break
            print(response.text)
        except Exception as e:
                    raise Exception(e)
    



if __name__ == "__main__":
    main()
